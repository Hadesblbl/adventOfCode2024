import utils.utils as utils
import time

fileName = "puzzle_6/input.txt"

nextMove = {"^": ">", ">": "v", "v": "<", "<": "^"}


def solve():
    print("Solving puzzle 6 of Advent of Code 2024")
    maze = utils.readFileLines(fileName)
    maze = list(map(list, maze))  # to list of list of chars

    x, y = getGuardPos(maze)
    startGuard = maze[y][x]
    guard = startGuard

    startPos = getPos(x, y)
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

# takes 15ms x 4826 = 1min


def bruteForceIt(startPos, startGuard, positions):
    nbLoops = 0
    # for each X except start, create maze with O instead
    # if reaches O a second time => loop OK
    positions.pop(startPos)
    positionsList = list(positions)
    # brute forcing all positions cause why not
    for pos in positions:
        x, y = getXY(startPos)
        guard = startGuard
        maze = utils.readFileLines(fileName)
        maze = list(map(list, maze))  # to list of list of chars
        ox, oy = getXY(pos)
        newPos = {}
        maze[oy][ox] = "O"
        while True:
            if guard == ".":
                break
            if guard == "+":
                nbLoops += 1
                break
            guard, x, y = move(maze, x, y, guard, newPos)
    print(nbLoops)


def getGuardPos(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] in {"^", "v", ">", "<"}:
                return [j, i]
    return [-1, -1]


def move(maze, x, y, guard, pos):
    movex, movey = utils.moves[guard]
    newX, newY = x+movex, y+movey
    if newX < 0 or newY < 0 or newX >= len(maze[0]) or newY >= len(maze):
        addPos(pos, x, y, guard)
        return [".", newX, newY]
    nextCase = maze[newY][newX]
    if (getPos(newX, newY) in pos and guard in pos[getPos(newX, newY)]):
        return ["+", x, y]
    if (nextCase in {"#", "O"}):
        newGuard = nextMove[guard]
        addPos(pos, x, y, guard)
        maze[y][x] = newGuard
        return [newGuard, x, y]
    else:
        addPos(pos, x, y, guard)
        maze[newY][newX] = guard
        return [guard, newX, newY]


def addPos(pos, x, y, guard):
    posXY = getPos(x, y)
    if posXY in pos:
        pos[posXY].add(guard)
    else:
        pos[posXY] = {guard}


def getPos(x, y):
    return str(x)+":"+str(y)


def getXY(pos):
    return list(map(int, pos.split(":")))
