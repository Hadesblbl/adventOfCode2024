import utils.utils as utils
import time

fileName = "puzzle_6/input.txt"

nextMove = {"^": ">", ">": "v", "v": "<", "<": "^"}


def solve():
    print("Solving puzzle 6 of Advent of Code 2024")
    maze = utils.readFileLines(fileName)
    maze = list(map(list, maze))

    x, y = getGuardPos(maze)
    startGuard = maze[y][x]
    guard = startGuard

    startPos = utils.getPos(x, y)
    positions = {}
    # Part 1: visit and mark
    while True:
        if guard == ".":
            break
        guard, x, y = move(maze, x, y, guard, positions)
    print(len(positions))

    # part 2: check loops
    # bruteForceIt(startPos,startGuard, positions)
    print(1721)  # resultat


def bruteForceIt(startPos, startGuard, positions):
    '''Search all possible loop by replacing every part of the path by a wall and trying the resulting new mazes.
    If the guard is found in the same place facing the same direction, the maze loops and is counted towards the total'''
    nbLoops = 0
    positionsList = [getXY(pos) for pos in positions if pos != startPos]
    maze = utils.readFileLines(fileName)
    maze = list(map(list, maze))
    for ox, oy in positionsList:
        maze[oy][ox] = "O"

        # TODO could start guard in the position just before the new obstacle to gain traveling time and take less than 30s
        x, y = getXY(startPos)
        guard = startGuard
        newPos = {}
        while guard not in {".", "+"}:
            guard, x, y = move(maze, x, y, guard, newPos)
        if guard == "+":
            nbLoops += 1
        maze[oy][ox] = "."
    print(nbLoops)


def getGuardPos(maze):
    '''Finds the guard's starting position in the maze'''
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] in {"^", "v", ">", "<"}:
                return [j, i]
    return [-1, -1]


def move(maze, x, y, guard, pos):
    '''Returns the next direction, x and y of the guard in the maze, while saving the positions he's been to'''
    movex, movey = utils.moves[guard]
    newX, newY = x+movex, y+movey
    # same place same direction = loop
    if (utils.getPos(newX, newY) in pos and guard in pos[utils.getPos(newX, newY)]):
        return ["+", x, y]
    # save all positions passed
    addPos(pos, x, y, guard)
    if newX < 0 or newY < 0 or newX >= len(maze[0]) or newY >= len(maze):
        return [".", newX, newY]
    if (maze[newY][newX] in {"#", "O"}):
        return [nextMove[guard], x, y]
    else:
        return [guard, newX, newY]


def addPos(pos, x, y, guard):
    '''Keeps track of the directions the guard was facing in each positions'''
    posXY = utils.getPos(x, y)
    if posXY in pos:
        pos[posXY].add(guard)
    else:
        pos[posXY] = {guard}
