import utils.utils as utils
import sys

fileName = "puzzle_2/input.txt"


def solve():
    print("Solving puzzle 2 of Advent of Code 2024")
    lines = utils.readFileLines(fileName)
    lines = [list(map(int, line.split(" "))) for line in lines]
    # Part 1
    print(getNbSafer(lines))
    # Part 2
    print(getNbSafe(lines))


def getNbSafer(lines):
    return sum([isSafer(line) for line in lines])


def getNbSafe(lines):
    return sum([isSafe(line) for line in lines])


def isSafer(line):
    '''Checks if the line is sorted (asc or desc), with a change of 1,2 or 3 every time'''
    order = line[1]-line[0]
    for i in range(len(line)-1):
        diff = line[i+1]-line[i]
        if diff*order <= 0 or diff > 3 or diff < -3:
            return 0
    return 1


def isSafe(line):
    '''Checks if the line is sorted (asc or desc), with a change of 1,2 or 3 every time, or can be by removing one of the steps'''
    if (isSafer(line)):
        return 1
    for i in range(len(line)):
        oneLess = line[0:i]+line[i+1:]
        if (isSafer(oneLess)):
            return 1
    return 0
