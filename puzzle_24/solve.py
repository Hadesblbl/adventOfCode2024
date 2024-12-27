import utils.utils as utils
from collections import ChainMap
from functools import cache

fileName = "puzzle_24/input.txt"


def solve() -> None:
    print("Solving puzzle 24 of Advent of Code 2024")
    wireValues, gateConnections = utils.readLinesSeparatedByEmptyLines(
        fileName)
    wireValues = translateWireValues(wireValues)
    gateConnections = gatesToDict(gateConnections)
    # Part 1
    print(getZ(wireValues, gateConnections))
    # Part 2
    print(getSwapsForFix(gateConnections, wireValues))


def getSwapsForFix(gateConnections: dict[str, str], wireValues: dict[str, int]) -> str:
    '''
    Step 1: prepare expected operations by index (for addition)
    Step 2: get gates operations by index
    Step 3: make them comparable
    Step 4: for each swap, needs to fix a digit operation so we can go to the next (digit 2^n depends on digit 2^n-1 and so on because addition carries over)

    z00 carries over if x00 and y00
    z01 carries over if x01 and y01 or (carry0 and x01 or y01)
    z02 carries over if x02 and y02 or (carry1 and x02 or y02)
    '''
    expected = getExpectedOperations(int(len(wireValues)/2))
    expectedDepth = getExpectedDepth(expected)
    indexDiff = getIndexDiff(expected, expectedDepth, gateConnections, 0)
    swaps = []
    for swapNum in range(4):
        gateResults = gatesSwappable(gateConnections, indexDiff)
        for i, j in getSwapsPos(len(gateResults)):
            a, b = gateResults[i], gateResults[j]
            if a in swaps or b in swaps:
                continue
            newConnections = swap([a, b], gateConnections)
            newDiff = getIndexDiff(
                expected, expectedDepth, newConnections, indexDiff)
            if newDiff > indexDiff:
                swaps += [a, b]
                gateConnections = newConnections
                indexDiff = newDiff
                break
            if newDiff == -1:
                swaps += [a, b]
                gateConnections = newConnections
                indexDiff = newDiff
                swaps.sort()
                return ",".join(swaps)
    swaps.sort()
    return ",".join(swaps)


def gatesSwappable(gateConnections, indexDiff):
    gatesToNotSwap: set = set({})
    for i in range(indexDiff):
        z = f'z{i:0>2}'
        gatesToNotSwap.update(getGatesUsedFor(
            gateConnections, z, len(gateConnections)))
    return [k for k in gateConnections.keys() if k not in gatesToNotSwap]


def getGatesUsedFor(gateConnections, code, depth):
    if code not in gateConnections:
        return set({})
    if depth <= 0:
        return set({})
    v1, ope, v2 = gateConnections[code].split(" ")
    allGates = getGatesUsedFor(gateConnections, v1, depth-1)
    allGates.update(getGatesUsedFor(gateConnections, v2, depth-1))
    allGates.add(code)
    return allGates


def getExpectedOperations(length: int) -> list[str]:
    expected = []
    carry = None
    for i in range(length-1):
        x = f'x{i:0>2}'
        y = f'y{i:0>2}'
        operation = newOpe('XOR', x, y)
        newCarry = newOpe('AND', x, y)
        if carry is not None:
            operation = newOpe('XOR', operation, carry)
            newCarry = newOpe('OR', newOpe('AND', x, y), newOpe(
                'AND', carry, newOpe('XOR', x, y)))
        carry = newCarry
        expected.append(operation)
    expected.append(carry)
    return expected


def getExpectedDepth(expectedOps: list[str]) -> list[int]:
    return [getDepth(expected) for expected in expectedOps]


def getActualOperations(gateConnections, code, maxDepth):
    if not code in gateConnections:
        return code
    if maxDepth < 0:
        return None
    a, operation, b = gateConnections[code].split(" ")
    opeA, opeB = getActualOperations(
        gateConnections, a, maxDepth-1), getActualOperations(gateConnections, b, maxDepth-1)
    if opeA is None or opeB is None:
        return None
    return [operation, [opeA, opeB]]


def getIndexDiff(expectedList, expectedDepth, gatesConnection, startIndex):
    for i in range(startIndex, len(expectedList)):
        expected = expectedList[i]
        actual = getActualOperations(
            gatesConnection, f'z{i:0>2}', len(gatesConnection))
        if (getDepth(actual) != expectedDepth[i]):
            return i
        if not isEqual(expected, actual):
            return i
    return -1


def isEqual(op1, op2):
    if type(op1) != type(op2):
        return False
    if isinstance(op1, str):
        return op1 == op2
    if getDepth(op1) != getDepth(op2):
        return False
    operator1, vars1 = op1
    operator2, vars2 = op2
    if operator1 != operator2 and (operator1 == "AND" or operator2 == "AND"):
        return False
    a1, b1 = vars1
    a2, b2 = vars2
    return (isEqual(a1, a2) and isEqual(b1, b2)) or (isEqual(a1, b2) and isEqual(b1, a2))


def getDepth(l):
    if not isinstance(l, list):
        return 0
    return max([getDepth(i) for i in l]) + 1


def swap(swaps: list[str], gateConnections: dict[str, str]) -> dict[str, str]:
    newConnections = ChainMap({}, gateConnections)
    for i in range(0, len(swaps), 2):
        a, b = swaps[i], swaps[i+1]
        newConnections[a], newConnections[b] = gateConnections[b], gateConnections[a]
    return newConnections


def getSwapsPos(length: int) -> list[list[int]]:
    for i in range(length):
        for j in range(i+1, length):
            yield i, j


def newOpe(operator, left, right):
    '''return new level of operation'''
    return [operator, [left, right]]


# ======================
# Everything useful to get Z value from a setup is under there

def getZ(wireDict: dict[str, int], gateConnections: dict[str, str]) -> str:
    '''Calculate Z from gates and wire values'''
    calculatedValues = ChainMap({}, wireDict)
    totalLengthExpected = len(wireDict)+len(gateConnections)
    previousLength = len(wireDict)-1
    while len(calculatedValues) < totalLengthExpected:
        for g in gateConnections.items():
            addNewValue(g, calculatedValues)
        if len(calculatedValues) == previousLength:
            return None
        previousLength = len(calculatedValues)
    return getValue(calculatedValues, "z")


def addNewValue(gate: tuple, wireValues: dict[str, int]) -> None:
    '''Calculate a gate value if possible and adds it to the dict of values'''
    result, operation = gate
    if result in wireValues:
        return
    wire1, binaryOp, wire2 = operation.split(" ")
    wire1, wire2 = wireValues.get(wire1), wireValues.get(wire2)
    if wire1 == None or wire2 == None:
        return
    if binaryOp == "OR":
        wireValues[result] = wire1 | wire2
    elif binaryOp == "AND":
        wireValues[result] = wire1 & wire2
    elif binaryOp == "XOR":
        wireValues[result] = wire1 ^ wire2


def getBitValue(wireValues: dict[str, int], letter: str) -> str:
    '''Returns the list of bitValues in index order'''
    letterWires = {k: v for k, v in wireValues.items() if k[0] == letter}

    wires = list(letterWires.keys())
    wires.sort()

    return "".join([str(letterWires[wire]) for wire in wires])


def getValue(wireValues: dict[str, int], letter: str) -> int:
    '''Transforms a reversed bit array into an int'''
    return int(getBitValue(wireValues, letter)[::-1], 2)


def translateWireValues(wireValues: list[str]) -> dict[str, int]:
    '''Transform wires into a dict of values per wire'''
    translated = {}
    for v in wireValues:
        wire, value = v.split(": ")
        translated[wire] = int(value)
    return translated


def gatesToDict(gateConnections: list[str]) -> dict[str, str]:
    '''Transform gates into a dict of result per operation'''
    resultDict = {}
    for gate in gateConnections:
        operation, result = gate.split(" -> ")
        resultDict[result] = operation
    return resultDict
