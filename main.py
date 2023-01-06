import argparse
import author
import collator
import merger
import sys
from collators.list_collator import ListCollator
from mergers.distance_merger import DistanceMerger


# Shows help / usage when given invalid arguments, useful since different parsers might have different arguments
class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


# TODO: Grab all from ./collators and ./mergers, rather than hardcode
all_collators = [ListCollator]
all_mergers = [DistanceMerger]

collator_names = set(map(lambda x: x.name, all_collators))
string_to_collator = {collator.name: collator for collator in all_collators}

merger_names = set(map(lambda x: x.name, all_mergers))
string_to_merger = {collator.name: collator for collator in all_mergers}

parser = DefaultHelpParser()
parser.add_argument("collator", metavar="C", choices=collator_names,
                    help="The file format to grab names from. Valid options are: " + ', '.join(collator_names))
parser.add_argument("merger", metavar="M", choices=merger_names,
                    help="The method used to merge names together. Valid options are: " + ', '.join(merger_names))
parser.add_argument("-o", "--output", dest="output", default="./thesaurus.txt", type=argparse.FileType("w"),
                    help="The path to save the thesaurus at. Default: ./thesaurus.txt")

# TODO: Run interactively if given no arguments?
init_args, remaining = parser.parse_known_args()

# apply collator
selected_collator: collator.Collator = string_to_collator[init_args.collator](remaining, parser)
authors: list[author.Author] = selected_collator.run()

# apply merger
selected_merger: merger.Merger = string_to_merger[init_args.merger](remaining, parser)
results: list[tuple[str, str]] = selected_merger.run(authors)

# save file
results.insert(0, ("label", "replace by", "score"))
init_args.output.writelines(map(lambda x: "\t".join(x) + "\n", results))
