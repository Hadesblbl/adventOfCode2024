import utils.utils as utils

fileName = "puzzle_1/input.txt"


def solve():
    print("Solving puzzle 1 of Advent of Code 2024")
    lines = utils.readFileLines(fileName)
    print(distance(lines))
    print(similarity(lines))


def distance(lines):
    l1 = []
    l2 = []
    for line in lines:
        if (len(line) < 3):
            continue
        a, b = line.split("  ")
        l1.append(int(a))
        l2.append(int(b))
    l1.sort()
    l2.sort()
    somme = 0
    for i in range(len(l1)):
        somme += abs(l1[i]-l2[i])
    return somme


def similarity(lines):
    l1 = []
    l2 = {}
    for line in lines:
        if (len(line) < 3):
            continue
        a, b = map(int, line.split("  "))
        l1.append(a)
        if (not a in l2):
            l2[a] = 0
        if (b in l2):
            l2[b] = l2[b]+1
        else:
            l2[b] = 1
    simil = 0
    for l in l1:
        simil += l*l2[l]
    return simil
