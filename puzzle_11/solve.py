import utils.utils as utils
import functools


fileName = "puzzle_11/input.txt"


def solve():
    print("Solving puzzle 11 of Advent of Code 2024")
    stones = utils.readFile(fileName)
    stones = list(map(int, stones.split(" ")))
    stones = toDict(stones)

    nbBlink = 25

    for i in range(nbBlink):
        stones = blink(stones)

    somme = 0
    for stone in stones:
        somme += stones[stone]
    print(somme)
    # blink 50 times more for 75
    nbBlink = 50

    for i in range(nbBlink):
        stones = blink(stones)

    somme = 0
    for stone in stones:
        somme += stones[stone]
    print(somme)


def blink(stones):
    newStoneNb = {}
    for stone in stones:
        result = change(stone)
        for r in result:
            if r in newStoneNb:
                newStoneNb[r] += stones[stone]
            else:
                newStoneNb[r] = stones[stone]
    return newStoneNb


def toDict(stones):
    dictStone = {}
    for stone in stones:
        if stone in dictStone:
            dictStone[stone] += 1
        else:
            dictStone[stone] = 1
    return dictStone


@functools.cache
def change(stone):
    if (stone == 0):
        return [1]
    stoneStr = str(stone)
    if (len(stoneStr) % 2 == 0):
        middle = int(len(stoneStr)/2)
        return [int(stoneStr[:middle]), int(stoneStr[middle:])]
    else:
        return [stone*2024]
