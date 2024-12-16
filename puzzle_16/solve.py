import utils.utils as utils
from enum import Enum
import heapq
import math

fileName = "puzzle_16/input.txt"


def solve():
    print("Solving puzzle 16 of Advent of Code 2024")
    maze = utils.readGridOfChars(fileName)

    visited = {}
    toVisit = [getPosStart(maze, "S")]
    posEnd = getPosEnd(maze, "E")
    minEnd = math.inf
    spotToSit = set({})
    # using heapq to use lower values first
    heapq.heapify(toVisit)

    while (len(toVisit) != 0):
        cost, x, y, direction, path = heapq.heappop(toVisit)
        posVisiting = getPos(x, y)
        visited[posVisiting] = [cost, direction]
        # stop condition
        if (maze[y][x] == "E"):
            minEnd = cost
            spotToSit.add(getPos(x, y))
            for pos in path:
                spotToSit.add(pos)
        # check every direction
        for directionEnum in Direction:
            movex, movey = directionEnum.value
            newx, newy = x+movex, y+movey
            if maze[newy][newx] == "#":
                continue
            posToVisit = getPos(newx, newy)
            costToVisit = cost+1
            if (directionEnum.value != direction):
                costToVisit += 1000
            if posToVisit not in visited or (visited[posToVisit][0] >= costToVisit-1000 and costToVisit <= minEnd):
                newPath = path[:]
                newPath.append(posVisiting)
                heapq.heappush(
                    toVisit, [costToVisit, newx, newy, directionEnum.value, newPath])
    print(minEnd)

    for spot in spotToSit:
        x, y = list(map(int, spot.split(":")))
        maze[y][x] = "O"
    print(len(spotToSit))

# POS = cost, x, y, direction, path so that cost is taken as the heap value


def getPosStart(maze, start):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == start:
                return [0, j, i, Direction.RIGHT.value, []]
    return [0, -1, -1, Direction.RIGHT.value, []]


def getPosEnd(maze, end):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == end:
                return getPos(j, i)
    return getPos(-1, -1)


def getPos(x, y):
    return str(x)+":"+str(y)


class Direction(Enum):
    UP = [0, -1]
    RIGHT = [1, 0]
    DOWN = [0, 1]
    LEFT = [-1, 0]
