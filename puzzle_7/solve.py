import utils.utils as utils

fileName = "puzzle_7/input.txt"


def solve():
    print("Solving puzzle 7 of Advent of Code 2024")
    lines = utils.readFileLines(fileName)
    lines = [line.split(": ") for line in lines]
    lines = [(int(value), list(map(int, numbers.split(" "))))
             for value, numbers in lines]

    # Part 1
    print(sum([value for value, numbers in lines if canBeTrue(value, numbers)]))

    # Part 2
    # part2(lines)
    print(204976636995111)


def part2(lines):
    print(sum([value for value, numbers in lines if canBeTrue(
        value, numbers) or canBeTrueWithConcat(value, numbers)]))


def canBeTrue(value, numbers):
    '''Check if value is present in possible outcomes from the numbers'''
    return value in allPossibleValues(numbers, value)


def allPossibleValues(numbers, value):
    '''Find all possible values from the list of numbers, excluding those superior to target value 
    (the chosen operands are only increasing the value)'''
    possibleValues = {numbers[0]}
    for i in range(1, len(numbers)):
        newPossibleValues = set({})
        for possibleValue in possibleValues:
            if possibleValue > value:
                continue
            newPossibleValues.add(possibleValue*numbers[i])
            newPossibleValues.add(possibleValue+numbers[i])
        possibleValues = newPossibleValues
    return newPossibleValues


def canBeTrueWithConcat(value, numbers):
    '''Check if value is present in possible outcomes from the numbers, with concat operand too'''
    return value in allPossibleValuesWithConcat(numbers, value)


def allPossibleValuesWithConcat(numbers, value):
    '''Find all possible values from the list of numbers, excluding those superior to target value 
    (the chosen operands are only increasing the value)'''
    possibleValues = {numbers[0]}
    for i in range(1, len(numbers)):
        newPossibleValues = set({})
        for possibleValue in possibleValues:
            if possibleValue > value:
                continue
            newPossibleValues.add(possibleValue*numbers[i])
            newPossibleValues.add(possibleValue+numbers[i])
            newPossibleValues.add(utils.concat(possibleValue, numbers[i]))
        possibleValues = newPossibleValues
    return newPossibleValues
