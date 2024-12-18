import utils.utils as utils
from collections import deque

fileName = "puzzle_18/input.txt"


def solve():
    print("Solving puzzle 18 of Advent of Code 2024")
    posToFill = utils.readFileLines(fileName)
    posToFill = [list(map(int, pos.split(","))) for pos in posToFill]
    grid = prepareGrid(posToFill, 1024)

    print(len(getPathToEnd(grid)))

    print(getByteBlockingExit(grid,posToFill))


def getGrid(x, y):
    return [["." for i in range(x)] for j in range(y)]


def prepareGrid(posToFill, nbCorruptedBytes):
    '''Prepares the grid described by the file'''
    grid = getGrid(71, 71)
    for i in range(nbCorruptedBytes):
        x, y = posToFill[i]
        grid[y][x] = "#"
    return grid

def getPathToEnd(grid):
    x, y = 0, 0
    targetx, targety = 70, 70
    grid[0][0] = "@"
    grid[70][70] = "E"

    visited = set({})
    toVisit = deque()
    toVisit.append([0, 0, []])
    while len(toVisit) > 0:
        visitx, visity, path = toVisit.popleft()
        if visitx == targetx and visity == targety:
            return path
        for nextX, nextY in utils.getAdjacent(visitx, visity):
            if utils.outOfBounds(nextX, nextY, 71, 71) or utils.getPos(nextX, nextY) in visited or grid[nextY][nextX] == "#":
                continue
            toVisit.append([nextX, nextY, path+[[visitx, visity]]])
            visited.add(utils.getPos(nextX, nextY))
    return []


def getByteBlockingExit(grid,posToFill):
    posInPath = {utils.getPos(x,y) for x,y in getPathToEnd(grid)}
    for i in range(1024,len(posToFill)):
        x,y = posToFill[i]
        grid[y][x] = "#"
        if utils.getPos(x,y) not in posInPath:
            continue
        else:
            posInPath = {utils.getPos(x,y) for x,y in getPathToEnd(grid)}
            if len(posInPath) == 0:
                return str(x)+","+str(y)
    return "0,0"
