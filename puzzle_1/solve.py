import utils.utils as utils

fileName = "puzzle_1/input.txt"


def solve():
    print("Solving puzzle 1 of Advent of Code 2024")
    lines = utils.readFileLines(fileName)
    lines = [list(map(int, line.split("   "))) for line in lines]
    # Part 1
    print(distance(lines))
    # Part 2
    print(similarity(lines))


def distance(lines):
    '''Creates and orders the two columns of int, then returns the sum of their disances ordered'''
    l1 = []
    l2 = []
    for x1, x2 in lines:
        l1.append(int(x1))
        l2.append(int(x2))
    l1.sort()
    l2.sort()
    return sum([abs(x1-x2) for x1, x2 in zip(l1, l2)])


def similarity(lines):
    '''Counts the occurences of each of the numbers in the second column, then calculate the similarity with the first column'''
    list1 = [a for a, b in lines]
    occurences = {a: 0 for a, b in lines}
    for a, b in lines:
        if b in occurences:
            occurences[b] += 1
    return sum([number*occurences[number] for number in list1])
