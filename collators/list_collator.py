import argparse
import csv
from io import TextIOWrapper

from author import Author
from collator import Collator


class ListCollator(Collator):
    name = "authorlist"

    def __init__(self, args: list[str], parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-f", "--file", dest="file", type=argparse.FileType("r"), default="authors.txt",
                            help="The file to read author names from. Default: authors.txt")
        parsed_args, remaining = parser.parse_known_args()
        self.file: TextIOWrapper = parsed_args.file

    def run(self) -> list[Author]:
        authors: list[Author] = []
        reader = csv.reader(self.file, delimiter="\t")
        reader.__next__()  # skip headers
        for row in reader:
            name = row[1]
            documents = int(row[2])
            author = Author(name)
            author.strengths["count"] = documents
            authors.append(author)
        return authors
