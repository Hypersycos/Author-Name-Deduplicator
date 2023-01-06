import argparse

from author import Author
from merger import Merger


class DistanceMerger(Merger):
    name = "distance"

    def __init__(self, args: list[str], parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-d", "--distance", dest="distance", type=int, required=True,
                            help="The maximum distance between names to be combined")
        parser.add_argument("-a", action='store_true', dest="sort_alphabetically", help="Sort thesaurus alphabetically")
        parsed_args, remaining = parser.parse_known_args()
        self.distance = parsed_args.distance
        self.sort_alphabetically = parsed_args.sort_alphabetically

    def run(self, authors: list[Author]) -> list[tuple[str, str]]:
        # assumes all variations will be next to each other alphabetically to reduce runtime to O(n)
        # TODO: add window?
        authors.sort(key=lambda x: x.name.last)
        change_made = True
        while change_made:
            i = 1
            change_made = False
            while i < len(authors):
                # merge names if within the distance threshold
                if authors[i-1].get_distance(authors[i]) <= self.distance:
                    authors[i-1].merge(authors[i])
                    del authors[i]
                    change_made = True
                else:
                    i += 1

        to_return = []
        for author in authors:
            for alternative in author.alternatives:
                to_return.append((alternative.full, author.name.full, alternative.get_distance(author.name)))
        if self.sort_alphabetically:
            to_return.sort(key=lambda x: x[1])
        else:
            to_return.sort(key=lambda x: x[2])

        return list(map(lambda x: (x[0], x[1], str(x[2])), to_return))
