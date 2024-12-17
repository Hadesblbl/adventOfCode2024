import utils.utils as utils
from collections import deque
fileName = "puzzle_10/input.txt"


def solve():
    print("Solving puzzle 10 of Advent of Code 2024")
    mountain = utils.readGridOfInts(fileName)
    maxX = len(mountain[0])
    maxY = len(mountain)

    toVisit = startingPoints(mountain)
    summitPerStart = {startPos: set({}) for x, y, value, startPos in toVisit}

    nbTrails = 0
    while len(toVisit) > 0:
        x, y, value, startPos = toVisit.popleft()
        if value == 9:
            nbTrails += 1
            summitPerStart[startPos].add(utils.getPos(x, y))
            continue
        for newX, newY in utils.getAdjacent(x, y):
            if utils.outOfBounds(newX, newY, maxX, maxY):
                continue
            if mountain[newY][newX] == value+1:
                toVisit.append([newX, newY, value+1, startPos])

    # Part 1
    print(sum([len(summitPerStart[start]) for start in summitPerStart]))
    # Part 2
    print(nbTrails)


def startingPoints(mountain):
    '''Returns a queue of all the starting points, to visit them later'''
    starts = deque()
    maxX = len(mountain[0])
    maxY = len(mountain)
    for y in range(maxY):
        for x in range(maxX):
            if mountain[y][x] == 0:
                starts.append([x, y, 0, utils.getPos(x, y)])
    return starts
