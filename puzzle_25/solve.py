import utils.utils as utils

fileName = "puzzle_25/input.txt"


def solve() -> None:
    print("Solving puzzle 25 of Advent of Code 2024")
    locksAndKeys = utils.readLinesSeparatedByEmptyLines(fileName)
    locks, keys = getLockAndKeys(locksAndKeys)
    nbFit = 0
    for lock in locks:
        for key in keys:
            if fit(lock, key):
                nbFit += 1
    print(nbFit)


def fit(lock: list[int], key: list[int]) -> bool:
    return all([s1+s2 <= 5 for s1, s2 in zip(lock, key)])


def getLockAndKeys(locksAndKeys: list[list[str]]) -> tuple[list[list[int]], list[list[int]]]:
    locks = [toSizes(item) for item in locksAndKeys if isLock(item)]
    keys = [toSizes(item) for item in locksAndKeys if not isLock(item)]
    return locks, keys


def isLock(item: list[str]) -> bool:
    return item[0][0] == "#"


def toSizes(item: list[str]) -> list[int]:
    lock = []
    for x in range(len(item[0])):
        size = sum([1 for y in range(1, len(item)-1) if item[y][x] == "#"])
        lock.append(size)
    return lock
