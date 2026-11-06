"""
Find HTCondor jobs that have been held exactly N times (according to their
user log files), remove them from the queue if they are still there,
optionally raise their memory request, and resubmit them.

Examples
--------
  # Dry run: show jobs held once, and what would be done with them
  python resubmitHeldJobs.py "${CONDOR_OUTPUT}/*${TIMESTAMP}/" -n 1 -m 10000 --dry-run

  # Actually resubmit jobs held twice with 16 GB of memory
  python resubmitHeldJobs.py "${CONDOR_OUTPUT}/*${TIMESTAMP}/" -n 2 -m 20000

  # Force resubmitted jobs onto a specific machine
  python resubmitHeldJobs.py "${CONDOR_OUTPUT}/*${TIMESTAMP}/" -n 1 \
      --requirements 'machine == "lorientree05.hep.zef.irb.hr"'

Quote the path if it contains wildcards so that Python expands it (this also
enables '**' for arbitrarily deep matching). Unquoted paths expanded by the
shell work too, since several paths may be given.


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

# HTCondor user log event header, e.g. "012 (1234.000.000) 2024-05-01 12:00:00 Job was held."
EVENT_RE = re.compile(r"^(\d{3}) \((\d+)\.(\d+)\.\d+\)")
SUBMIT, TERMINATED, ABORTED, HELD, RELEASED = "000", "005", "009", "012", "013"

QUEUE_RE = re.compile(r"^\s*queue\b", re.IGNORECASE | re.MULTILINE)


def attr_regex(name_pattern):
    """Regex matching a submit-file assignment, including '\\' continuation lines."""
    return re.compile(rf"^(\s*(?:{name_pattern})\s*=[ \t]*)((?:.*\\\n)*.*)$",
                      re.IGNORECASE | re.MULTILINE)


MEMORY_RE = attr_regex(r"request_?memory")
REQUIREMENTS_RE = attr_regex(r"requirements")


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
    """Return (number of hold events, job id of the last hold, state after it).

    state is one of:
      None      - never held
      'held'    - still held in the queue (needs condor_rm before resubmission)
      'removed' - held and then removed (can be resubmitted directly)
      'handled' - released, resubmitted or finished after the last hold
    """
    events = []
    with open(path, errors="replace") as f:
        for line in f:
            m = EVENT_RE.match(line)
            if m:
                events.append((m.group(1), f"{int(m.group(2))}.{int(m.group(3))}"))

    held_idx = [i for i, (code, _) in enumerate(events) if code == HELD]
    if not held_idx:
        return 0, None, None

    last = held_idx[-1]
    job_id = events[last][1]
    after = {code for code, _ in events[last + 1:]}
    if after & {SUBMIT, RELEASED, TERMINATED}:
        state = "handled"
    elif ABORTED in after:
        state = "removed"
    else:
        state = "held"
    return len(held_idx), job_id, state


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


def still_in_queue(job_id):
    ok, out = run(["condor_q", job_id, "-af", "JobStatus"])
    return ok and out != ""


def main():
    parser = argparse.ArgumentParser(
        description="Resubmit HTCondor jobs that were held exactly N times.")
    parser.add_argument("paths", nargs="+",
                        help="Path(s) searched recursively for *.log files; wildcards allowed (quote them)")
    parser.add_argument("-m", "--memory", type=int,
                        help="New RequestMemory in MB (default: leave job descriptions unchanged)")
    parser.add_argument("-r", "--requirements",
                        help="New 'requirements' expression, replacing any existing one, e.g. "
                             "'machine == \"lorientree05.hep.zef.irb.hr\"' "
                             "(default: leave requirements unchanged)")
    parser.add_argument("-n", "--times-held", type=int, default=1,
                        help="Resubmit only jobs held exactly this many times (default: 1)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only print the jobs that would be resubmitted")
    args = parser.parse_args()

    if args.times_held < 1:
        parser.error("--times-held must be >= 1")

    logs = find_logs(args.paths)
    if not logs:
        sys.exit("No log files found.")

    infos = [(log, *analyse_log(log)) for log in logs]

    counts = Counter(n for _, n, _, _ in infos if n > 0)
    print(f"Scanned {len(logs)} log files.")
    if not counts:
        print("No held jobs found.")
        return
    for n in sorted(counts):
        print(f"  held {n}x: {counts[n]} job(s)")

    selected = [i for i in infos if i[1] == args.times_held]
    to_resubmit = [i for i in selected if i[3] in ("held", "removed")]
    for log, _, job_id, _ in (i for i in selected if i[3] == "handled"):
        print(f"Skipping {log} (job {job_id}): already released/resubmitted/finished after last hold")

    if not to_resubmit:
        print(f"No jobs held exactly {args.times_held} time(s) need resubmission.")
        return

    prefix = "[DRY RUN] " if args.dry_run else ""
    print(f"\n{prefix}{len(to_resubmit)} job(s) held exactly {args.times_held} time(s) to resubmit:")

    failures = 0
    for log, _, job_id, state in to_resubmit:
        desc = job_desc_for(log)
        print(f"\n{log}\n  job {job_id} ({state}) -> {desc}")
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
            if state == "held":
                print(f"  {prefix}condor_rm {job_id}")
            for change in changes:
                print(f"  {prefix}{change}")
            print(f"  {prefix}condor_submit {desc}")
            continue

        # 1) remove the held job from the queue
        if state == "held":
            ok, out = run(["condor_rm", job_id])
            if ok:
                print(f"  removed job {job_id}")
            elif still_in_queue(job_id):
                print(f"  ERROR: could not remove job {job_id}, skipping:\n    {out}", file=sys.stderr)
                failures += 1
                continue
            else:
                print(f"  job {job_id} is no longer in the queue")

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
