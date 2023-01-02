import difflib


class Author:

    def __init__(self, name: str):
        self.name: Name = Name(name)
        self.alternatives: set[Name] = set()
        self.disambiguators: dict[str, str] = {}
        self.strengths: dict[str, int] = {}

    def merge(self, other: "Author", combine_strengths=True):
        if sum(self.strengths.values()) >= sum(other.strengths.values()):
            self.alternatives.add(self.name)
            self.name = other.name

        self.alternatives = self.alternatives.union(other.alternatives)
        for key in other.disambiguators:
            self.disambiguators[key] = other.disambiguators[key]
        if combine_strengths:
            for key in other.disambiguators:
                self.disambiguators[key] = other.disambiguators[key] + self.disambiguators.get(key, 0)
        else:
            for key in set(self.strengths.keys()).union(set(other.strengths.keys())):
                if key in self.strengths:
                    self.strengths[key] = max(self.strengths[key], other.strengths.get(key, 0))
                else:
                    self.strengths[key] = other.strengths[key]

    def __str__(self):
        return str(self.name)

    def compare(self, other: "Author"):
        for key in set(self.disambiguators.keys()).union(set(other.disambiguators.keys())):
            if self.disambiguators[key] != other.disambiguators[key]:
                return 10000
        minimum = 10000
        for name1 in self.alternatives.union({self.name}):
            for name2 in other.alternatives.union({other.name}):
                minimum = min(minimum, name1.compare(name2))
        return minimum


class Name:

    def __init__(self, full: str):
        self.full = full

        delimiters = ", ."
        split = []
        start = 0
        i = 0
        while i < len(full):
            while i < len(full) and full[i] not in delimiters:
                i += 1
            end = i - 1
            split.append(full[start:end])
            while i < len(full) and full[i] in delimiters:
                i += 1
            start = i
        self.last = split[0]
        self.others = split[1:]

    def __str__(self):
        return self.full

    def compare(self, other: "Name"):
        difference = sum([i[0] != ' ' for i in difflib.ndiff(self.last, other.last)])
        return difference + recursive_compare(self.others, other.others)


def score(name1, name2):
    if len(name1) > len(name2):
        name2, name1 = name1, name2

    if len(name1) == 1:
        return 1 - int(name1[0] == name2[0])
    else:
        return sum([i[0] != ' ' for i in difflib.ndiff(name1, name2)])


def recursive_compare(names1: list[str], names2: list[str]):
    if min(len(names1), len(names2)) == 0:
        if len(names1) + len(names2) != 0:
            return 10000
        else:
            return 0
    equal_score = score(names1[0], names2[0]) + recursive_compare(names1[1:], names2[1:])
    #skip 1
    skip_1_score = 1 + recursive_compare(names1[1:], names2)
    #skip 2
    skip_2_score = 1 + recursive_compare(names1, names2[1:])
    return min(equal_score, skip_1_score, skip_2_score)

