import argparse
import author
from abc import ABC, abstractmethod


class Collator(ABC):
    name = None

    @abstractmethod
    def __init__(self, args: list[str], parser: argparse.ArgumentParser) -> None:
        pass

    @abstractmethod
    def run(self) -> list[author.Author]:
        pass
