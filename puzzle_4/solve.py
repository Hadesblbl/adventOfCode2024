import utils.utils as utils
import re

fileName = "puzzle_4/input.txt"


def solve():
    print("Solving puzzle 4 of Advent of Code 2024")
    lines = utils.readFileLines(fileName)
    # Padding to check diagonals without overflow - with letter to ease regex usage
    padding = "J"*140
    concat = padding.join(lines)

    # Part 1 - XMAS
    nbXmas = nbPatterns(concat, ["XMAS", "SAMX", "X[A-Z]{279}M[A-Z]{279}A[A-Z]{279}S", "S[A-Z]{279}A[A-Z]{279}M[A-Z]{279}X", "X[A-Z]{280}M[A-Z]{280}A[A-Z]{280}S",
                        "S[A-Z]{280}A[A-Z]{280}M[A-Z]{280}X", "X[A-Z]{278}M[A-Z]{278}A[A-Z]{278}S", "S[A-Z]{278}A[A-Z]{278}M[A-Z]{278}X"])

    print(nbXmas)
    # Part 2 - MAS in X
    nbXmas = nbPatterns(concat, ["M.S[A-Z]{278}A[A-Z]{278}M.S", "S.M[A-Z]{278}A[A-Z]{278}S.M",
                        "M.M[A-Z]{278}A[A-Z]{278}S.S", "S.S[A-Z]{278}A[A-Z]{278}M.M"])

    print(nbXmas)


def nbPattern(txt, pattern):
    '''Get the number of occurence of the pattern in txt'''
    regex = re.compile(pattern)
    nb = 0
    found = regex.search(txt)
    while found != None:
        nb += 1
        found = regex.search(txt, found.start()+1)
    return nb


def nbPatterns(txt, patterns):
    '''Gets the number of all the patterns in txt'''
    return sum([nbPattern(txt, pattern) for pattern in patterns])
