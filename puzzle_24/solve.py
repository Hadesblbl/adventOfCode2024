import utils.utils as utils
from collections import ChainMap

fileName = "puzzle_24/input.txt"


def solve() -> None:
    print("Solving puzzle 24 of Advent of Code 2024")
    wireValues, gateConnections = utils.readLinesSeparatedByEmptyLines(
        fileName)
    wireValues = translateWireValues(wireValues)
    gateConnections = gatesToDict(gateConnections)
    # Part 1
    print(getZ(wireValues, gateConnections))


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
