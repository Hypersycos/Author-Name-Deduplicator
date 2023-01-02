import collator, merger, author, argparse, csv, importlib

from collators.list_collator import ListCollator
from mergers.distance_merger import DistanceMerger

all_collators = [ListCollator]
string_to_collator = {collator.name: collator for collator in all_collators}
all_mergers = [DistanceMerger]
string_to_merger = {collator.name: collator for collator in all_mergers}

parser = argparse.ArgumentParser()
parser.add_argument("collator", metavar="C", choices=set(map(lambda x: x.name, all_collators)))
parser.add_argument("merger", metavar="M", choices=set(map(lambda x: x.name, all_mergers)))
parser.add_argument("-o", "--output", dest="output", default="thesaurus.txt", type=argparse.FileType("w"))

init_args, remaining = parser.parse_known_args()

# if no arguments, run interactively

# select collator
# apply collator arguments
selected_collator: collator.Collator = string_to_collator[init_args.collator](remaining, parser)
# apply collator
authors: list[author.Author] = selected_collator.run()

# select merger
# apply merger arguments
selected_merger: merger.Merger = string_to_merger[init_args.merger](remaining, parser)
# apply merger
results: list[tuple[str, str]] = selected_merger.run(authors)

# save file
results.insert(0, ("label", "replace by"))
with open(init_args.output, "w", encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='\t')
    for row in results:
        writer.writerow(row)