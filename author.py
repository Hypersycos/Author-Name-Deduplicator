import difflib


class Author:

    def __init__(self, name: str):
        self.name: Name = Name(name)
        self.alternatives: set[Name] = set()
        self.disambiguators: dict[str, str] = {}
        self.strengths: dict[str, int] = {}

    def merge(self, other: "Author", combine_strengths=True):
        # take name of "strongest" author, and add weaker to alternatives
        if sum(self.strengths.values()) >= sum(other.strengths.values()):
            self.alternatives.add(self.name)
            self.name = other.name
        else:
            self.alternatives.add(other.name)

        self.alternatives = self.alternatives.union(other.alternatives)
        # Add all other disambiguators. If keys are shared they should never be different.
        # TODO: enforce no changes?
        for key in other.disambiguators:
            self.disambiguators[key] = other.disambiguators[key]

        # If combining strengths, add them together, otherwise take the greatest for each key
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

    def get_distance(self, other: "Author"):
        # TODO: Allow customisation of scoring values
        for key in set(self.disambiguators.keys()).union(set(other.disambiguators.keys())):
            if self.disambiguators[key] != other.disambiguators[key]:
                # if they have different disambiguators, cannot be the same
                return 10000
        minimum = 10000
        # get the smallest distance between every possible name
        for name1 in self.alternatives.union({self.name}):
            for name2 in other.alternatives.union({other.name}):
                minimum = min(minimum, name1.get_distance(name2))
        return minimum


class Name:

    def __init__(self, full: str):
        self.full = full

        # first name is only ever ended by comma
        delimiters = ","
        split = []
        start = 0
        i = 0
        while i < len(full):
            # grab name
            while i < len(full) and full[i] not in delimiters:
                i += 1
            split.append(full[start:i])

            # uses , . as delimiters for all other names
            delimiters = ", ."
            # skip over all delimiters until we get a letter, prevents blank "names"
            while i < len(full) and full[i] in delimiters:
                i += 1
            start = i
        self.last = split[0]
        self.others = split[1:]

    def __str__(self):
        return self.full

    def get_distance(self, other: "Name"):
        # TODO: allow customisation of scoring
        # gets indel score / distance for the last names
        difference = sum([i[0] != ' ' for i in difflib.ndiff(self.last, other.last)])
        # compares other names, e.g. comparing smith j. to smith a. j.
        return difference + recursive_compare(self.others, other.others)


def score(name1, name2):
    # ensure name1 is shorter than name2
    if len(name1) > len(name2):
        name2, name1 = name1, name2

    if len(name1) == 1:
        # don't allow mismatched initials (assuming initials are never typo-d)
        # if name1 is inital and name2 isn't, then just check that that first letter of the full name is the same
        # this won't work if first letter of name is incorrect, e.g. smith a. vs smith llen
        return 0 if name1[0] == name2[0] else 10000
    else:
        # otherwise both names, just get distance
        return sum([i[0] != ' ' for i in difflib.ndiff(name1, name2)])


def recursive_compare(names1: list[str], names2: list[str]):
    def worker(names1: list[str], names2: list[str], skips1: int, skips2: int):
        # if out of names for at least one spelling
        if min(len(names1), len(names2)) == 0:
            # skip remaining names if able (or return 0 if out of names for both)
            if len(names1) <= skips1 and len(names2) <= skips2:
                return (len(names1) + len(names2)) * 2
            else:
                return 10000

        scores = [10000]

        # consume one name from both
        scores.append(score(names1[0], names2[0]) + worker(names1[1:], names2[1:], skips1, skips2))

        # skip one from name 1
        if skips1 > 0:
            scores.append(2 + worker(names1[1:], names2, skips1-1, skips2))

        # skip one from name 2
        if skips2 > 0:
            scores.append(2 + worker(names1, names2[1:], skips1, skips2-1))

        return min(scores)

    # don't allow every name from one spelling to be skipped
    return worker(names1, names2, len(names1)-1, len(names2)-1)
