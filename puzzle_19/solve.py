import utils.utils as utils
import functools

fileName = "puzzle_19/input.txt"


def solve():
    print("Solving puzzle 19 of Advent of Code 2024")
    patterns, designs = utils.readLinesSeparatedByEmptyLines(fileName)
    # using tuple to make it hashable for cache
    patterns = tuple(patterns[0].split(", "))

    print(sum([isPossible(design, patterns) for design in designs]))
    print(sum([nbOfArrangementsPossible(design, patterns)
          for design in designs]))


@functools.cache
def isPossible(design, patterns):
    if len(design) == 0:
        return True
    for pattern in patterns:
        if design.startswith(pattern) and isPossible(design[len(pattern):], patterns):
            return True
    return False


@functools.cache
def nbOfArrangementsPossible(design, patterns):
    if len(design) == 0:
        return 1
    nbArrangements = 0
    for pattern in patterns:
        if design.startswith(pattern) and isPossible(design[len(pattern):], patterns):
            nbArrangements += nbOfArrangementsPossible(
                design[len(pattern):], patterns)
    return nbArrangements
