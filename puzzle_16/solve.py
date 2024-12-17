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
        posVisiting = utils.getPos(x, y)
        visited[posVisiting] = [cost, direction]
        # stop condition
        if (maze[y][x] == "E"):
            minEnd = cost
            spotToSit.add(utils.getPos(x, y))
            for pos in path:
                spotToSit.add(pos)
        # check every direction
        for directionEnum in Direction:
            movex, movey = directionEnum.value
            newx, newy = x+movex, y+movey
            if maze[newy][newx] == "#":
                continue
            posToVisit = utils.getPos(newx, newy)
            costToVisit = cost+1
            if (directionEnum.value != direction):
                costToVisit += 1000
            # Take into account the fact that there can be an avoided turn next step for the same position
            if posToVisit not in visited or (visited[posToVisit][0] >= costToVisit-1000 and costToVisit <= minEnd):
                newPath = path[:]
                newPath.append(posVisiting)
                heapq.heappush(
                    toVisit, [costToVisit, newx, newy, directionEnum.value, newPath])
    # Part 1
    print(minEnd)

    # Part 2
    print(len(spotToSit))

#


def getPosStart(maze, start):
    '''Pos = cost, x, y, direction, path so that cost is taken as the heap value'''
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == start:
                return [0, j, i, Direction.RIGHT.value, []]
    return [0, -1, -1, Direction.RIGHT.value, []]


def getPosEnd(maze, end):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == end:
                return utils.getPos(j, i)
    return utils.getPos(-1, -1)


class Direction(Enum):
    UP = [0, -1]
    RIGHT = [1, 0]
    DOWN = [0, 1]
    LEFT = [-1, 0]
