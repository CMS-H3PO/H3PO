"""
Find HTCondor jobs whose *latest* status (according to their user log files)
matches one or more given statuses, optionally change their memory request
and/or requirements, and resubmit them.

Supported statuses (--status, several may be given):
  aborted          job was aborted (removed), e.g. by condor_rm
  nonzero          job terminated normally with a non-zero return value
  return=N         job terminated with return value N (also accepted:
                   'N', 'rv=N', 'return value N')
  signal           job terminated abnormally by any signal
  signal=N         job terminated abnormally by signal N

Examples
--------
  # Dry run: jobs that were aborted or failed with return value 132
  python resubmitJobsByStatus.py "${CONDOR_OUTPUT}/*${TIMESTAMP}/" -s aborted 'return value 132' --dry-run

  # Resubmit all jobs with a non-zero return value, with more memory, on a given machine
  python resubmitJobsByStatus.py "${CONDOR_OUTPUT}/*${TIMESTAMP}/" -s nonzero -m 10000 \
      --requirements 'machine == "lorientree05.hep.zef.irb.hr"'

Quote the path if it contains wildcards so that Python expands it (this also
enables '**' for arbitrarily deep matching).


Credits: Claude AI
"""

import argparse
import glob
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

# Mapping from log file to job description file, mirroring
#   sed 's|logs/tmp-|jobs/job_desc-|g' | sed 's|\.log|\.txt|g'
LOG_TAG, DESC_TAG = "logs/tmp-", "jobs/job_desc-"

# HTCondor user log event header, e.g. "005 (1234.000.000) 2024-05-01 12:00:00 Job terminated."
EVENT_RE = re.compile(r"^(\d{3}) \((\d+)\.(\d+)\.\d+\)")
EVENT_END = "..."
SUBMIT, TERMINATED, ABORTED, HELD, RELEASED = "000", "005", "009", "012", "013"
RETURN_RE = re.compile(r"\(return value (-?\d+)\)", re.IGNORECASE)
SIGNAL_RE = re.compile(r"\(signal (\d+)\)", re.IGNORECASE)

QUEUE_RE = re.compile(r"^\s*queue\b", re.IGNORECASE | re.MULTILINE)


def attr_regex(name_pattern):
    """Regex matching a submit-file assignment, including '\\' continuation lines."""
    return re.compile(rf"^(\s*(?:{name_pattern})\s*=[ \t]*)((?:.*\\\n)*.*)$",
                      re.IGNORECASE | re.MULTILINE)


MEMORY_RE = attr_regex(r"request_?memory")
REQUIREMENTS_RE = attr_regex(r"requirements")


# --------------------------------------------------------------------------
# Status specification
# --------------------------------------------------------------------------

def parse_status(spec):
    """Turn a --status value into (kind, value); value None means 'any'."""
    s = " ".join(spec.strip().lower().split())
    if s in ("aborted", "abort", "removed"):
        return ("aborted", None)
    if s in ("nonzero", "non-zero", "failed"):
        return ("return", None)
    if s == "signal":
        return ("signal", None)
    m = re.fullmatch(r"(?:return[ _-]?value|return|rv)?\s*[=:]?\s*(-?\d+)", s)
    if m:
        return ("return", int(m.group(1)))
    m = re.fullmatch(r"signal\s*[=: ]?\s*(\d+)", s)
    if m:
        return ("signal", int(m.group(1)))
    raise argparse.ArgumentTypeError(
        f"invalid status '{spec}' (use: aborted, nonzero, return=N, signal, signal=N)")


def status_matches(state, specs):
    kind, value = state
    for s_kind, s_value in specs:
        if kind != s_kind:
            continue
        if s_value is None:
            if kind != "return" or value != 0:   # 'nonzero' excludes return value 0
                return True
        elif value == s_value:
            return True
    return False


def describe(state):
    kind, value = state
    return {
        "aborted": "aborted",
        "return": f"return value {value}",
        "signal": f"signal {value}",
        "held": "held",
        "queued": "idle/running (no final status yet)",
        "unknown": "no events found",
    }[kind]


# --------------------------------------------------------------------------
# Log parsing
# --------------------------------------------------------------------------

def natural_key(s):
    """Sort key equivalent to 'sort -V'."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", str(s))]


def find_logs(patterns):
    logs = set()
    for pattern in patterns:
        pattern = os.path.expandvars(os.path.expanduser(pattern))
        matches = glob.glob(pattern, recursive=True)
        if not matches:
            print(f"WARNING: nothing matches '{pattern}'", file=sys.stderr)
        for match in matches:
            p = Path(match)
            if p.is_dir():
                logs.update(f for f in p.rglob("*.log") if f.is_file())
            elif p.is_file() and p.suffix == ".log":
                logs.add(p)
    return sorted(logs, key=natural_key)


def analyse_log(path):
    """Return (job_id, state) describing the latest status of the job.

    state is (kind, value) with kind one of 'aborted', 'return', 'signal',
    'held', 'queued' or 'unknown'. A submit event after a final event
    (i.e. the job was already resubmitted) resets the state to 'queued'.
    """
    job_id, state = None, ("unknown", None)
    current = None          # event code of the block being read
    with open(path, errors="replace") as f:
        for line in f:
            m = EVENT_RE.match(line)
            if m:
                current = m.group(1)
                event_id = f"{int(m.group(2))}.{int(m.group(3))}"
                if current == SUBMIT:
                    job_id, state = event_id, ("queued", None)
                elif current == ABORTED:
                    job_id, state = event_id, ("aborted", None)
                elif current == HELD:
                    job_id, state = event_id, ("held", None)
                elif current == RELEASED:
                    job_id, state = event_id, ("queued", None)
                elif current == TERMINATED:
                    job_id = event_id
                continue
            if line.startswith(EVENT_END):
                current = None
                continue
            if current == TERMINATED:
                rv = RETURN_RE.search(line)
                if rv:
                    state = ("return", int(rv.group(1)))
                    current = None
                    continue
                sig = SIGNAL_RE.search(line)
                if sig:
                    state = ("signal", int(sig.group(1)))
                    current = None
    return job_id, state


# --------------------------------------------------------------------------
# Job description editing and Condor commands
# --------------------------------------------------------------------------

def job_desc_for(log_path):
    s = str(log_path).replace(LOG_TAG, DESC_TAG)
    return Path(re.sub(r"\.log$", ".txt", s))


def set_attribute(text, regex, name, value):
    """Set an attribute in a submit description; returns (new_text, old_value).

    Every existing assignment matched by regex is replaced; if there is none,
    'name = value' is inserted before the first 'queue' statement.
    """
    m = regex.search(text)
    if m:
        old = re.sub(r"\\\n\s*", " ", m.group(2)).strip()
        return regex.sub(lambda mm: f"{mm.group(1)}{value}", text), old
    line = f"{name} = {value}\n"
    q = QUEUE_RE.search(text)
    if q:
        return text[:q.start()] + line + text[q.start():], None
    return text.rstrip("\n") + "\n" + line, None


def run(cmd):
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        print(f"ERROR: command '{cmd[0]}' not found", file=sys.stderr)
        return False, ""
    out = (res.stdout + res.stderr).strip()
    return res.returncode == 0, out


def queued_job_ids():
    """Set of 'cluster.proc' ids currently in the queue, or None if condor_q fails."""
    ok, out = run(["condor_q", "-af", "ClusterId", "ProcId"])
    if not ok:
        return None
    return {".".join(line.split()) for line in out.splitlines() if line.strip()}


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Resubmit HTCondor jobs based on their latest status.",
        epilog="Statuses: aborted, nonzero, return=N (or 'return value N'), signal, signal=N",
    )
    parser.add_argument("paths", nargs="+",
                        help="Path(s) searched recursively for *.log files; wildcards allowed (quote them)")
    parser.add_argument("-s", "--status", nargs="+", type=parse_status, required=True,
                        metavar="STATUS",
                        help="Status(es) of jobs to resubmit (see below)")
    parser.add_argument("-m", "--memory", type=int,
                        help="New RequestMemory in MB (default: leave job descriptions unchanged)")
    parser.add_argument("-r", "--requirements",
                        help="New 'requirements' expression, replacing any existing one, e.g. "
                             "'machine == \"lorientree05.hep.zef.irb.hr\"' "
                             "(default: leave requirements unchanged)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only print the jobs that would be resubmitted")
    args = parser.parse_args()

    logs = find_logs(args.paths)
    if not logs:
        sys.exit("No log files found.")

    infos = [(log, *analyse_log(log)) for log in logs]

    print(f"Scanned {len(logs)} log files. Latest job statuses:")
    counts = Counter(describe(state) for _, _, state in infos)
    for label in sorted(counts, key=natural_key):
        print(f"  {label}: {counts[label]} job(s)")

    to_resubmit = [i for i in infos if status_matches(i[2], args.status)]
    wanted = ", ".join(describe((k, v)) if v is not None else
                       {"aborted": "aborted", "return": "non-zero return value",
                        "signal": "any signal"}[k]
                       for k, v in args.status)
    if not to_resubmit:
        print(f"\nNo jobs with status [{wanted}] found; nothing to resubmit.")
        return

    prefix = "[DRY RUN] " if args.dry_run else ""
    print(f"\n{prefix}{len(to_resubmit)} job(s) with status [{wanted}] to resubmit:")

    in_queue = set()
    if not args.dry_run:
        in_queue = queued_job_ids()
        if in_queue is None:
            print("WARNING: condor_q failed; cannot check for leftover jobs in the queue",
                  file=sys.stderr)
            in_queue = set()

    failures = 0
    for log, job_id, state in to_resubmit:
        desc = job_desc_for(log)
        print(f"\n{log}\n  job {job_id} ({describe(state)}) -> {desc}")
        if not desc.is_file():
            print(f"  ERROR: job description {desc} not found, skipping", file=sys.stderr)
            failures += 1
            continue

        text = desc.read_text()
        new_text, changes = text, []
        for value, regex, name in ((args.memory, MEMORY_RE, "RequestMemory"),
                                   (args.requirements, REQUIREMENTS_RE, "requirements")):
            if value is not None:
                new_text, old = set_attribute(new_text, regex, name, value)
                changes.append(f"{name}: {old or '(not set)'} -> {value}")

        if args.dry_run:
            for change in changes:
                print(f"  {prefix}{change}")
            print(f"  {prefix}condor_submit {desc}")
            continue

        # 1) finished/aborted jobs are normally gone, but remove any leftover
        #    (e.g. jobs kept in the queue with leave_in_queue)
        if job_id in in_queue:
            ok, out = run(["condor_rm", job_id])
            if not ok:
                print(f"  ERROR: could not remove job {job_id}, skipping:\n    {out}",
                      file=sys.stderr)
                failures += 1
                continue
            print(f"  removed leftover job {job_id} from the queue")

        # 2) update memory request / requirements
        if new_text != text:
            desc.write_text(new_text)
        for change in changes:
            print(f"  {change}")

        # 3) resubmit
        ok, out = run(["condor_submit", str(desc)])
        if ok:
            print(f"  {out.splitlines()[-1] if out else 'submitted'}")
        else:
            print(f"  ERROR: condor_submit failed:\n    {out}", file=sys.stderr)
            failures += 1

    if failures:
        sys.exit(f"\n{failures} job(s) could not be resubmitted.")


if __name__ == "__main__":
    main()
