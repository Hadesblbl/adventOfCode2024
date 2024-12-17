import utils.utils as utils
from collections import deque

fileName = "puzzle_12/input.txt"


def solve():
    print("Solving puzzle 12 of Advent of Code 2024")
    lines = utils.readFileLines(fileName)
    # first, get groups
    visited = set({})
    groups = []
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if getPos(x, y) in visited:
                continue
            groups.append(getGroup(lines, x, y, visited))

    # then calculate area and perimeter for each group
    somme = 0
    for group in groups:
        area = len(group)
        perimeter = getPerimeter(group)
        somme += area * perimeter
    print(somme)
    somme = 0
    for group in groups:
        area = len(group)
        sides = getNbSides(group)
        somme += area * sides
    print(somme)


def getGroup(lines, x, y, visited):
    maxx = len(lines[0])
    maxy = len(lines)
    group = []
    letter = lines[y][x]
    toVisit = deque()
    toVisit.append([x, y])
    while len(toVisit) > 0:
        visitx, visity = toVisit.popleft()
        if getPos(visitx, visity) in visited or lines[visity][visitx] != letter:
            continue
        visited.add(getPos(visitx, visity))
        group.append([visitx, visity])
        for newx, newy in utils.getAdjacent(visitx, visity):
            if isOutOfBounds(newx, newy, maxx, maxy) or getPos(newx, newy) in visited or lines[newy][newx] != letter:
                continue
            toVisit.append([newx, newy])
    return group


def isOutOfBounds(x, y, maxx, maxy):
    return x < 0 or y < 0 or x >= maxx or y >= maxy


# count number of sides
def getPerimeter(group):
    groupSet = set({getPos(x, y) for x, y in group})
    side = 0
    for x, y in group:
        for nextx, nexty in utils.getAdjacent(x, y):
            if getPos(nextx, nexty) not in groupSet:
                side += 1
    return side


def getNbSides(group):
    groupSet = set({getPos(x, y) for x, y in group})
    sidesX = set({})
    sidesY = set({})
    # search sides
    # when a side is found, check its start and end then add it to the set
    # could be optimized to not check again if we know it's already identified
    for x, y in group:
        for nextx, nexty in utils.getAdjacent(x, y):
            if getPos(nextx, nexty) not in groupSet:
                if nexty == y:
                    # check horizontal side
                    miny, maxy = y, y
                    while getPos(x, miny) in groupSet and getPos(nextx, miny) not in groupSet:
                        miny -= 1
                    while getPos(x, maxy) in groupSet and getPos(nextx, maxy) not in groupSet:
                        maxy += 1
                    sidesX.add(getSide(x, nextx, miny, maxy))
                elif nextx == x:
                    # check vertical side
                    minx, maxx = x, x
                    while getPos(minx, y) in groupSet and getPos(minx, nexty) not in groupSet:
                        minx -= 1
                    while getPos(maxx, y) in groupSet and getPos(maxx, nexty) not in groupSet:
                        maxx += 1
                    sidesY.add(getSide(y, nexty, minx, maxx))
    return len(sidesX)+len(sidesY)


def getPos(x, y):
    return str(x)+":"+str(y)


def getSide(inside, outside, start, end):
    return str(inside)+":"+str(outside)+":"+str(start)+":"+str(end)
