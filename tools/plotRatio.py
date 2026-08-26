import ROOT as r
import copy
import fnmatch
from argparse import ArgumentParser

#---------------------------------------------------------------------
# set plot style
r.gROOT.SetStyle("Plain")

# suppress the statistics box
r.gStyle.SetOptStat(0)

# more detailed statistics box
#r.gStyle.SetOptStat(1111111)

# suppress the histogram title
#r.gStyle.SetOptTitle(0)

r.gStyle.SetPadTickX(1)  # to get the tick marks on the opposite side of the frame
r.gStyle.SetPadTickY(1)  # to get the tick marks on the opposite side of the frame

# set nicer fonts
r.gStyle.SetTitleFont(42, "")
r.gStyle.SetTitleFont(42, "XYZ")
r.gStyle.SetLabelFont(42, "XYZ")
r.gStyle.SetTextFont(42)
r.gStyle.SetStatFont(42)
r.gROOT.ForceStyle()
#---------------------------------------------------------------------

def pattern_present(names):
    for n in names:
        if "*" in n:
            return True


def matching_names(f, n):
    name_list = []
    for key in f.GetListOfKeys():
        name_list.append(key.GetName())

    return fnmatch.filter(name_list, n)


def get_histo(info, f, names):
    # check if there are any name patterns provided
    if pattern_present(names):
        name_list = []
        for n in names:
            if "*" in n:
                name_list.extend(matching_names(f, n))
            else:
                name_list.append(n)
    else:
        name_list = names

    print(f"List of {info} histograms:", name_list)

    histo = f.Get(name_list[0])
    if len(name_list) > 1:
        for i in range(1, len(name_list)):
            histo.Add(f.Get(name_list[i]))
    
    return histo


def main():
    # usage example
    Description = "Example: %(prog)s -i test.root"
    
    # input parameters
    parser = ArgumentParser(description=Description)

    parser.add_argument("-i", "--input", dest="input",
                        help="Input file",
                        metavar="INPUT",
                        required=True
                        )
    parser.add_argument("-n", "--num", help="Space-separated list of histogram names or name patterns to be added and used as numerator",
                        nargs="*",
                        dest="num",
                        required=True
                        )
    parser.add_argument("-d", "--den", help="Space-separated list of histogram names or name patterns to be added and used as denominator",
                        nargs="*",
                        dest="den",
                        required=True
                        )
    parser.add_argument("-o", "--output", dest="output",
                        help="Output file",
                        )
    parser.add_argument("--fmt", dest="fmt",
                        help="Output format  (default: %(default)s)",
                        default='png'
                        )
    parser.add_argument("--batch", dest="batch", action='store_true',
                        help="Switch for batch mode and disabling interactive prompt",
                        default=False)
    parser.add_argument("--save_histo", dest="save_histo", action='store_true',
                        help="Save the final ratio histogram",
                        default=False)
    parser.add_argument("--binomial", dest="binomial", action='store_true',
                        help="Compute binomial errors",
                        default=False)

    (options, args) = parser.parse_known_args()

    if options.batch:
        # enable batch mode (prevents canvases from popping up)
        r.gROOT.SetBatch()

    # input file
    inputFile = r.TFile.Open(options.input)

    num = get_histo("numerator", inputFile, options.num)

    den = get_histo("denominator", inputFile, options.den)

    ratio = copy.deepcopy(num)
    if options.output:
        ratio.SetNameTitle(options.output, options.output)
    else:
        ratio.SetTitle("ratio")

    if options.binomial:
        ratio.Divide(num, den, 1., 1., "B")
    else:
        ratio.Divide(den)

    # create canvas
    c = r.TCanvas("c", "",1200,800)
    c.cd()

    ratio.Draw("COLZTEXT")
    c.Update() # forces the canvas to repaint. Otherwise, you might get an empty canvas displayed in the interacive mode

    if options.output:
        c.SaveAs( options.output + '.' + options.fmt )

        if options.save_histo:
            ratio.SaveAs( options.output + '.root' )
            # Create the output ROOT file
            fout = r.TFile(options.output + '.root', "RECREATE")

            # Update names and titles
            name = options.output + '_num'
            num.SetNameTitle(name, name)
            name = options.output + '_den'
            den.SetNameTitle(name, name)

            # Write all histograms to it
            num.Write()
            den.Write()
            ratio.Write()

            # Close the file
            fout.Close()

    if not options.batch:
        input('Press enter to exit...')


if __name__ == '__main__':
    main() 
