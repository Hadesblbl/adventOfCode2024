import utils.utils as utils

fileName = "puzzle_23/input.txt"


def solve():
    print("Solving puzzle 23 of Advent of Code 2024")
    connections = utils.readFileLines(fileName)
    connectionsMap = getConnectionsMap(connections)

    # Part 1
    print(getNbSetsOf3WithT(connectionsMap))

    # Part 2
    l = list(next(iter(getMaxSet(connectionsMap))))
    l.sort()
    print(",".join(l))


def getConnectionsMap(connections):
    '''Returns a map representing all the connections'''
    connectionsMap = {}
    for c in connections:
        start, end = c.split("-")
        if start in connectionsMap:
            connectionsMap[start].add(end)
        else:
            connectionsMap[start] = {end}
        # not directional so we add reverse too
        if end in connectionsMap:
            connectionsMap[end].add(start)
        else:
            connectionsMap[end] = {start}
    return connectionsMap


def getNbSetsOf3WithT(connectionsMap):
    '''Returns the length of all separate groups of 3 distinct with a computer starting with "t"'''
    setsOf3 = set({})
    for start, ends in connectionsMap.items():
        # not directional, so we can only care about start and middle
        if start.startswith("t"):
            # 2nd item
            for end in ends:
                # 3rd item
                for third in connectionsMap[end]:
                    if third == start:
                        continue
                    if third not in ends:
                        continue
                    if third == end:
                        continue
                    setsOf3.add(getOrderedConnection([start, end, third]))
        else:
            for end in ends:
                if end.startswith("t"):
                    for third in connectionsMap[end]:
                        if third == start:
                            continue
                        if third not in ends:
                            continue
                        if third == end:
                            continue
                        setsOf3.add(getOrderedConnection([start, end, third]))
    return len(setsOf3)


def getMaxSet(connectionsMap):
    '''Starts from groups of 2 until it gets the biggest grouping possible, adding 1 by 1'''
    combinationsMax = {getOrderedConnection([start, end])
                       for start, ends in connectionsMap.items() for end in ends}
    while True:
        newCombinationsMax = set({})
        for combinations in combinationsMax:
            possibleNext = connectionsMap[combinations[0]]
            if len(possibleNext) == len(combinations):
                continue  # no more to add there
            # search bigger set by 1 -can be limited to the first connections
            for connection in possibleNext:
                if connection in combinations:
                    continue
                if all(s in connectionsMap[connection] for s in combinations):
                    newCombinationsMax.add(getOrderedConnection(
                        list(combinations)+[connection]))
        if len(newCombinationsMax) == 0:
            return combinationsMax
        combinationsMax = newCombinationsMax


def getOrderedConnection(connectionList):
    '''Order a list and put it in a tuple to order by list of same elements'''
    connectionList.sort()
    return tuple(connectionList)
