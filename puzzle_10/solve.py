import utils.utils as utils
from collections import deque
fileName = "puzzle_10/input.txt"


def solve():
    print("Solving puzzle 10 of Advent of Code 2024")
    mountain = utils.readGridOfInts(fileName)
    maxX = len(mountain[0])
    maxY = len(mountain)

    toVisit = startingPoints(mountain)
    summitPerStart = {}
    nbTrails = 0

    while len(toVisit) > 0:
        x, y, value, startPos = toVisit.popleft()
        if value == 9:
            nbTrails += 1
            if startPos in summitPerStart:
                summitPerStart[startPos].add(getPos(x, y))
            else:
                summitPerStart[startPos] = {getPos(x, y)}
            continue
        for move in utils.moves:
            movex, movey = utils.moves[move]
            newX, newY = x+movex, y+movey
            if outOfBounds(newX, newY, maxX, maxY):
                continue
            if mountain[newY][newX] == value+1:
                toVisit.append([newX, newY, value+1, startPos])
    nb9 = 0
    for start in summitPerStart:
        nb9 += len(summitPerStart[start])
    print(nb9)
    print(nbTrails)


def startingPoints(mountain):
    starts = deque()
    maxX = len(mountain[0])
    maxY = len(mountain)
    for y in range(maxY):
        for x in range(maxX):
            if mountain[y][x] == 0:
                starts.append([x, y, 0, getPos(x, y)])
    return starts


def outOfBounds(x, y, maxX, maxY):
    return x < 0 or y < 0 or x >= maxX or y >= maxY


def getPos(x, y):
    return str(x)+":"+str(y)
