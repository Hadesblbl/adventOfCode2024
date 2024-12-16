import utils.utils as utils

fileName = "puzzle_7/input.txt"


def solve():
    print("Solving puzzle 7 of Advent of Code 2024")
    lines = utils.readFileLines(fileName)

    somme = 0
    for line in lines:
        value, numbers = line.split(": ")
        if canBeTrue(int(value), list(map(int, numbers.split(" ")))):
            somme += int(value)
    print(somme)

    # checkWithConcatToBigNumbers(lines)
    print(204976636995111)


def checkWithConcatToBigNumbers(lines):
    somme = 0
    for line in lines:
        value, numbers = line.split(": ")
        if canBeTrueWithConcat(int(value), list(map(int, numbers.split(" ")))):
            somme += int(value)
    print(somme)

# can be optimized by exiting once found


def canBeTrue(value, numbers):
    return value in allPossibleValues(numbers)

# with left to right operations


def allPossibleValues(numbers):
    if (len(numbers) == 1):
        return {numbers[-1]}
    possibleValues = allPossibleValues(numbers[:-1])
    newPossibleValues = set({})
    for possibleValue in possibleValues:
        newPossibleValues.add(possibleValue*numbers[-1])
        newPossibleValues.add(possibleValue+numbers[-1])
    return newPossibleValues

# can be optimized by exiting once found


def canBeTrueWithConcat(value, numbers):
    return value in allPossibleValuesWithConcat(numbers)

# concat is all left vs all right


def allPossibleValuesWithConcat(numbers):
    if (len(numbers) == 1):
        return {numbers[-1]}
    possibleValues = allPossibleValuesWithConcat(numbers[:-1])
    newPossibleValues = set({})
    for possibleValue in possibleValues:
        newPossibleValues.add(possibleValue*numbers[-1])
        newPossibleValues.add(possibleValue+numbers[-1])
        newPossibleValues.add(int(str(possibleValue)+str(numbers[-1])))
    return newPossibleValues
