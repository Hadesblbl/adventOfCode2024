import utils.utils as utils
from collections import deque
import functools
import math

fileName = "puzzle_21/input.txt"


def solve():
    print("Solving puzzle 21 of Advent of Code 2024")
    codes = utils.readFileLines(fileName)
    numPad = [["7", "8", "9"], ["4", "5", "6"],
              ["1", "2", "3"], ["#", "0", "A"]]
    numPad = tuple(map(tuple, numPad))
    keyPad = [["#", "^", "A"], ["<", "v", ">"]]
    keyPad = tuple(map(tuple, keyPad))

    # Part 1
    print(getComplexity(codes, numPad, keyPad, 2))
    # Part 2
    print(getComplexity(codes, numPad, keyPad, 25))


def getComplexity(codes, numPad, keyPad, nbKeyPads):
    '''Calculate complexity for each code (= code * its final instruction min length)'''
    somme = 0
    for c in codes:
        num = int(c[:-1])
        shortest = getShortestSequence(c, numPad, keyPad, nbKeyPads)
        somme += shortest*num
    return somme


def getShortestSequence(code, numPad, keyPad, nbKeyPads):
    '''Returns the size of the shortest sequence for a given code, with 1 numPad and nbKeyPads keyPad. 
    For that purpose, transforms the code into moves (example: go from A to 0) because each move is independent at the next level, being separated by an A press at all time'''
    initialMoves = getMoves("A"+code)
    possibleMoves = getNextMoves(initialMoves, numPad)
    return min([sum([minLength(move, keyPad, nbKeyPads)*nbMove for move, nbMove in moves.items() if nbMove > 0]) for moves in possibleMoves])


def getMoves(c):
    '''Get moves. Group characters that have the same length and same outcome'''
    moves = {"AA": 0, "<v": 0, "v<": 0, "v^": 0, "^v": 0, "><": 0,
             "^<": 0,
             "<>": 0,
             "<^": 0, "<A": 0,
             "A<": 0, "vA": 0,
             ">^": 0,
             "^>": 0,
             "Av": 0}
    for i in range(len(c)-1):
        move = c[i:i+2]
        if move in {"AA", "vv", "^^", "<<", ">>"}:
            moves["AA"] += 1
        elif move in {"<v", "v>", "^A"}:
            moves["<v"] += 1
        elif move in {"v<", ">v", "A^"}:
            moves["v<"] += 1
        elif move in {"v^", ">A"}:
            moves["v^"] += 1
        elif move in {"^v", "A>"}:
            moves["^v"] += 1
        elif move in moves:
            moves[move] += 1
        else:
            moves[move] = 1
    return moves


def getNextMoves(moves, keyPad):
    '''Returns a set of possible moves for next step'''
    possibleMoves = [{}]
    for move in moves:
        numberOfMove = moves[move]
        if numberOfMove == 0:
            continue
        start, end = list(move)
        nextMoves = getNextMove(move, keyPad)
        nextMoves = [{k: v*numberOfMove for k, v in p.items()}
                     for p in nextMoves]
        newPossibleMoves = []
        for p in possibleMoves:
            for c in nextMoves:
                newPossibleMoves.append(utils.addDicts(p, c))
        possibleMoves = newPossibleMoves
    return possibleMoves


@functools.cache
def getNextMove(move, keyPad):
    '''Returns next possible moves for a single move'''
    start, end = list(move)
    return [getMoves("A"+c) for c in getShortests(keyPad, start, end)]


@functools.cache
def minLength(move, keyPad, depth):
    '''Returns min length of instruction to execute a move from a certain depth'''
    if depth == 0:
        return 1
    minSomme = math.inf
    for nextMove in getNextMove(move, keyPad):
        somme = 0
        for p, nbMove in nextMove.items():
            if nbMove == 0:
                continue
            somme += minLength(p, keyPad, depth-1) * nbMove
        if somme < minSomme:
            minSomme = somme
    return minSomme


@functools.cache
def getShortests(pad, charStart, charEnd):
    '''Returns the shortests path for pressing a char(only those with the most repeating chars).
    Note: There is an empty space in pads, it cannot go there, so we check for this too.'''
    if charStart == charEnd:
        return ["A"]
    paths = []
    startx, starty = getPos(pad, charStart)
    targetx, targety = getPos(pad, charEnd)

    dx = targetx - startx
    dy = targety - starty
    dirx = "<"
    if dx > 0:
        dirx = ">"
    diry = "^"
    if dy > 0:
        diry = "v"
    bestPaths = [dirx*abs(dx)+diry*abs(dy)]
    if dirx != "<":
        bestPaths.append(diry*abs(dy) + dirx*abs(dx))
    bestPaths = [diry*abs(dy) + dirx*abs(dx), dirx*abs(dx)+diry*abs(dy)]
    forbiddenx, forbiddeny = 0, 0
    if isNumPad(pad):
        forbiddeny = 3
    # exclude paths that goes out of bounds
    result = set({})
    for path in bestPaths:
        isCorrect = True
        x, y = startx, starty
        for c in path:
            movex, movey = utils.moves[c]
            x, y = x+movex, y+movey
            if x == forbiddenx and y == forbiddeny:
                isCorrect = False
        if isCorrect:
            result.add(path+"A")
    if (len(result) == 2 and (dx == 0 or dy == 0)):
        return [diry*abs(dy) + dirx*abs(dx)]
    return result


def getPos(pad, char):
    '''Get the position of a character in the pad'''
    for y in range(len(pad)):
        for x in range(len(pad[0])):
            if pad[y][x] == char:
                return [x, y]
    raise RuntimeError("Character "+char+" not found in pad")


def isNumPad(pad):
    return pad[0][0] == "7"
