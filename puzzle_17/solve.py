import utils.utils as utils
import functools

fileName = "puzzle_17/input.txt"


def solve():
    print("Solving puzzle 17 of Advent of Code 2024")
    # Read input
    registersStr, instructionsStr = utils.readLinesSeparatedByEmptyLines(
        fileName)
    registers = [int(line.split(": ")[1]) for line in registersStr]
    instructionsStr = instructionsStr[0].split(": ")[1]
    instructions = list(map(int, instructionsStr.split(",")))

    # Part 1
    a, b, c = registers
    output = getOutput(instructions, a, b, c)
    print(",".join(output))

    # Part 2
    searchPart2(instructions, registers)


def searchPart2(instructions, registers):
    """By observation:
    len(output) = log8(a) + 1 for input.txt
    len(output) = log2(a) + 1 for test2.txt

    Also by observation:
    Every digit changes only when a increments by pow(8,indexDigit) for input.txt
    For test2.txt, the same is true for pow(2,indexDigit)

    So, we need to find every multiple of the 8^index that satisfies the condition for each index
    Then we deduce the list of all the As that makes the instruction outputs itself, and choose the min of them.

    To find what digit we need to put under the power, we search the first increment of number of digits. (works for test2.txt and input.txt)
    """
    basePow = getBasePow(instructions)
    powerMax = len(instructions) - 1
    a = pow(basePow, powerMax)

    # search every possible A that can output instructions
    listPossibleA = [a]
    nextPossibleA = []

    output = getOutput(instructions, a, 0, 0)
    for i in range(len(output)):
        index = powerMax - i
        for possibleA in listPossibleA:
            for nbPow in range(basePow):
                nextA = possibleA + nbPow*pow(basePow, index)
                output = getOutput(instructions, nextA, 0, 0)
                if output[index] == str(instructions[index]):
                    nextPossibleA.append(nextA)
        listPossibleA = nextPossibleA
        nextPossibleA = []

    print(min(listPossibleA))  # then just like that, we find the solution


def execute(instruction, registers, operand, pointer, output):
    """Execute an instruction, changing registers, pointer and/or output according to the instruction"""

    combo = getCombo(operand, registers)
    a, b, c = registers
    if instruction == 0:
        registers[0] = a >> combo
    elif instruction == 1:
        registers[1] = operand ^ b
    elif instruction == 2:
        registers[1] = combo % 8
    elif instruction == 3:
        if a != 0:
            return operand
    elif instruction == 4:
        registers[1] = b ^ c
    elif instruction == 5:
        output.append(str(combo % 8))
    elif instruction == 6:
        registers[1] = a >> combo
    elif instruction == 7:
        registers[2] = a >> combo
    return pointer+2


def getCombo(operand, registers):
    """Get combo operand from itself or registers"""
    if operand <= 3:
        return operand
    else:
        return registers[operand-4]


@functools.cache
def getNext(instructionsStr, a, b, c, pointer):
    """Get next output from instructions, registers values and pointer index. Use cache to reduce usage if we need to get full output multiple times"""

    registers = [a, b, c]
    instructions = list(map(int, instructionsStr.split(",")))
    output = []
    while pointer < len(instructions) and len(output) == 0:
        instruction, operand = instructions[pointer:pointer+2]
        pointer = execute(instruction, registers, operand, pointer, output)
    nextOutput = ""
    if len(output) > 0:
        nextOutput = output[0]
    return [registers, pointer, nextOutput]


def getOutput(instructions, a, b, c):
    """Get output from instructions and registers values"""

    instructionsStr = ",".join(map(str, instructions))
    output = []
    pointer = 0
    while pointer < len(instructions):
        registers, pointer, nextOutput = getNext(
            instructionsStr, a, b, c, pointer)
        a, b, c = registers
        if nextOutput != "":
            output.append(nextOutput)
    return output


def getBasePow(instructions):
    """Search first increment of the size of output"""
    basePow = 0
    output = getOutput(instructions, basePow, 0, 0)
    while len(output) < 2:
        basePow += 1
        output = getOutput(instructions, basePow, 0, 0)
    return basePow
