import argparse

from author import Author
from merger import Merger


class DistanceMerger(Merger):
    name = "distance"

    def __init__(self, args: list[str], parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-d", "--distance", dest="distance", default=4, type=int)
        parsed_args, remaining = parser.parse_known_args()
        self.distance = parsed_args.distance

    def run(self, authors: list[Author]) -> list[tuple[str, str]]:
        authors.sort(key=lambda x: x.name.last)
        i = 1
        while i < len(authors):
            if authors[i-1].compare(authors[i]) <= self.distance:
                authors[i-1].merge(authors[i])
            else:
                i += 1
        to_return = []
        for author in authors:
            for alternative in author.alternatives:
                to_return.append((alternative.full, author.name.full, alternative.compare(author.name)))
        to_return.sort(key=lambda x: x[2])
        return list(map(lambda x: (x[0], x[1]), to_return))
