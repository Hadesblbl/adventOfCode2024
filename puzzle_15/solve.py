import utils.utils as utils
import time

fileName = "puzzle_15/input.txt"

moves = {"^": [0, -1], "v": [0, 1], ">": [1, 0], "<": [-1, 0]}


def solve():
    print("Solving puzzle 15 of Advent of Code 2024")
    maze, moves = utils.readLinesSeparatedByEmptyLines(fileName)
    maze = list(map(list, maze))  # to list of list of chars
    x, y = utils.findItem(maze, "@")
    for move in list("".join(moves)):  # to list of chars
        x, y = moveMaze(maze, x, y, move)
    somme = 0
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "O":
                somme += gpsCoordinates(j, i)
    print(somme)

    # PART2
    maze, moves = utils.readLinesSeparatedByEmptyLines(fileName)
    maze = scaleUp(maze)
    maze = list(map(list, maze))  # to list of list of chars
    x, y = utils.findItem(maze, "@")
    for move in list("".join(moves)):  # to list of chars
        x, y = moveScaledupMaze(maze, x, y, move)

    maxX = len(maze[0])
    maxY = len(maze)
    somme = 0
    for i in range(maxY):
        for j in range(maxX):
            if maze[i][j] == "[":
                somme += gpsCoordinates(j, i)
    print(somme)


def gpsCoordinates(x, y):
    '''Returns coordinates score'''
    return y*100+x


def moveMaze(maze, x, y, move):
    '''Move once in a direction in a normal maze'''
    nextEmptySpot = getEmptySpotIndex(maze, x, y, move)
    if (nextEmptySpot == -1):
        return [x, y]
    movex, movey = moves[move]
    # push = robot becomes empty, next becomes robot, last spot after becomes box if there is one
    maze[y][x] = "."
    maze[y+movey][x+movex] = "@"
    if (nextEmptySpot > 1):
        maze[y+movey*nextEmptySpot][x+movex*nextEmptySpot] = "O"
    return [x+movex, y+movey]


def moveScaledupMaze(maze, x, y, move):
    '''Move once in a direction in a scaled up maze'''
    movex, movey = moves[move]
    # Horizontal move, push the boxes by 1
    if (movey == 0):
        nextEmptySpot = getEmptySpotIndex(maze, x, y, move)
        if (nextEmptySpot == -1):
            return [x, y]
        maze[y][x] = "."
        maze[y][x+movex] = "@"
        box = "["
        if movex < 0:
            box = "]"
        for i in range(1, nextEmptySpot):
            maze[y][x+movex+i*movex] = box
            # alternate
            if (box == "["):
                box = "]"
            else:
                box = "["
    # if empty, just go
    elif maze[y+movey][x] == ".":
        maze[y][x] = "."
        maze[y+movey][x] = "@"
    # if wall or cannot push you cannot move
    elif maze[y+movey][x] == "#" or not canPush(maze, x, y, movey):
        return [x, y]
    else:
        push(maze, x, y, movey)
        maze[y][x] = "."
        maze[y+movey][x] = "@"
    return [x+movex, y+movey]


def getEmptySpotIndex(maze, x, y, move):
    '''Returns the distance to the next empty spot in the direction of the move'''
    movex, movey = moves[move]
    nextCase = ""
    nbPush = 1
    while nextCase != "#":
        nextCase = maze[y+movey*nbPush][x+movex*nbPush]
        if (nextCase == "."):
            return nbPush
        nbPush += 1
    return -1


def scaleUp(maze):
    '''Returns a scaled up maze'''
    for y in range(len(maze)):
        row = maze[y]
        row = row.replace(".", "..")
        row = row.replace("O", "[]")
        row = row.replace("@", "@.")
        row = row.replace("#", "##")
        maze[y] = row
    return maze


def canPush(maze, x, y, movey):
    '''Checks if a vertical push is possible in a scaled up maze'''
    x1, x2 = x, x+1
    if maze[y+movey][x] == "]":
        x1, x2 = x-1, x
    if (maze[y+movey*2][x1] == "#" or maze[y+movey*2][x2] == "#"):
        return False
    if (maze[y+movey*2][x1] == "." and maze[y+movey*2][x2] == "."):
        return True
    if (maze[y+movey*2][x1] == "[" and maze[y+movey*2][x2] == "]"):
        return canPush(maze, x1, y+movey, movey)
    canPushBool = True
    if maze[y+movey*2][x1] == "]" and not canPush(maze, x1, y+movey, movey):
        canPushBool = False
    if maze[y+movey*2][x2] == "[" and not canPush(maze, x2, y+movey, movey):
        canPushBool = False
    return canPushBool


def push(maze, x, y, movey):
    '''Push vertically in a scaled up maze. Needs to check with canPush before using'''
    if (maze[y+movey][x] == "."):
        return
    x1, x2 = x, x+1
    if maze[y+movey][x] == "]":
        x1, x2 = x-1, x
    obstacleLeft = maze[y+movey*2][x1]
    obstacleRight = maze[y+movey*2][x2]
    # no obstacle = go
    if (obstacleLeft == "." and obstacleRight == "."):
        pass
    # obstacle aligned = push it the same
    elif (obstacleLeft == "[" and obstacleRight == "]"):
        push(maze, x1, y+movey, movey)
    else:
        # one or 2 obstacles misaligned = push them too
        if obstacleLeft == "]":
            push(maze, x1-1, y+movey, movey)
        if obstacleRight == "[":
            push(maze, x2, y+movey, movey)
    # in every situation, finish by pushing actual box
    utils.swapGrid(maze, x1, y+movey, x1, y+movey*2)
    utils.swapGrid(maze, x2, y+movey, x2, y+movey*2)
