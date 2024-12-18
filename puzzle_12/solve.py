import utils.utils as utils
from collections import deque

fileName = "puzzle_12/input.txt"


def solve():
    print("Solving puzzle 12 of Advent of Code 2024")
    lines = utils.readFileLines(fileName)
    # first, get groups
    groups = getGroups(lines)
    # Part 1 - get area*perimeter for each group
    print(sum([len(group) * getPerimeter(group) for group in groups]))
    # Part 2 - get area*number of sides for each group
    print(sum([len(group) * getNbSides(group) for group in groups]))


def getGroups(lines):
    '''Find every groups of letter'''
    visited = set({})
    groups = []
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if utils.getPos(x, y) in visited:
                continue
            groups.append(getGroup(lines, x, y, visited))
    return groups


def getGroup(lines, x, y, visited):
    '''Find the group of letter tied to the position x,y and fill the visited set with all positions pertaining to that group'''
    maxx = len(lines[0])
    maxy = len(lines)
    group = []
    letter = lines[y][x]
    toVisit = deque()
    toVisit.append([x, y])
    while len(toVisit) > 0:
        visitx, visity = toVisit.popleft()
        if utils.getPos(visitx, visity) in visited or lines[visity][visitx] != letter:
            continue
        visited.add(utils.getPos(visitx, visity))
        group.append([visitx, visity])
        for newx, newy in utils.getAdjacent(visitx, visity):
            if utils.outOfBounds(newx, newy, maxx, maxy) or utils.getPos(newx, newy) in visited or lines[newy][newx] != letter:
                continue
            toVisit.append([newx, newy])
    return group


def getPerimeter(group):
    '''Counts every side that leads outside of the group, which adds up to the perimeter'''
    groupSet = set({utils.getPos(x, y) for x, y in group})
    side = 0
    for x, y in group:
        for nextx, nexty in utils.getAdjacent(x, y):
            if utils.getPos(nextx, nexty) not in groupSet:
                side += 1
    return side


def getNbSides(group):
    '''Search sides. When a side is found, check its start and end then add it to the set.
    Returns the total number of horizontal and vertical sides found'''
    groupSet = set({utils.getPos(x, y) for x, y in group})
    sidesX = set({})
    sidesY = set({})
    for x, y in group:
        for nextx, nexty in utils.getAdjacent(x, y):
            if utils.getPos(nextx, nexty) not in groupSet:
                if nexty == y:
                    # check horizontal side
                    miny, maxy = y, y
                    while utils.getPos(x, miny) in groupSet and utils.getPos(nextx, miny) not in groupSet:
                        miny -= 1
                    while utils.getPos(x, maxy) in groupSet and utils.getPos(nextx, maxy) not in groupSet:
                        maxy += 1
                    sidesX.add(getSide(x, nextx, miny, maxy))
                elif nextx == x:
                    # check vertical side
                    minx, maxx = x, x
                    while utils.getPos(minx, y) in groupSet and utils.getPos(minx, nexty) not in groupSet:
                        minx -= 1
                    while utils.getPos(maxx, y) in groupSet and utils.getPos(maxx, nexty) not in groupSet:
                        maxx += 1
                    sidesY.add(getSide(y, nexty, minx, maxx))
    return len(sidesX)+len(sidesY)


def getSide(inside, outside, start, end):
    '''Returns a hashable representation of a side'''
    return str(inside)+":"+str(outside)+":"+str(start)+":"+str(end)
