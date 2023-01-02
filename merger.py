import argparse
from abc import ABC, abstractmethod
import author


class Merger(ABC):
    name = None

    @abstractmethod
    def __init__(self, args: list[str], parser: argparse.ArgumentParser) -> None:
        pass

    @abstractmethod
    def run(self, authors: list[author.Author]) -> list[tuple[str, str]]:
        pass
