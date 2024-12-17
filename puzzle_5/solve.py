import utils.utils as utils

fileName = "puzzle_5/input.txt"


def solve():
    print("Solving puzzle 5 of Advent of Code 2024")
    orders, lines = utils.readLinesSeparatedByEmptyLines(fileName)
    orders = [order.split("|") for order in orders]
    lines = [line.split(",") for line in lines]
    biggerThan = getBiggerThanMap(orders)

    ordered, unordered = getSumsOrderedUnordered(lines, biggerThan)
    # Part 1
    print(ordered)

    # Part 2
    print(unordered)


def getSumsOrderedUnordered(lines, biggerThan):
    '''Sums the middle integer of all ordered lines'''
    sumOrdered = 0
    sumUnordered = 0
    for line in lines:
        if (isOrdered(line, biggerThan)):
            sumOrdered += getMiddleInt(line)
        else:
            line = sort(line, biggerThan)
            sumUnordered += getMiddleInt(line)
    return [sumOrdered, sumUnordered]


def sort(liste, biggerThan):
    '''Swaps every unordered elements until the list is sorted. 
    A normal sort is impossible here because the comparator is not transitive ! '''
    while (not isOrdered(liste, biggerThan)):
        for firstIndex in range(len(liste)):
            for secondIndex in range(firstIndex+1, len(liste)):
                if isBigger(liste[firstIndex], liste[secondIndex], biggerThan):
                    utils.swap(liste, firstIndex, secondIndex)
    return liste


def isOrdered(liste, biggerThanMap):
    '''Checks if the list is ordered, that is, if every element is only followed by bigger numbers than itself, according to the map of relation'''
    for i in range(len(liste)):
        for j in range(i):
            if isBigger(liste[j], liste[i], biggerThanMap):
                return False
    return True


def isBigger(i, j, biggerThanMap):
    '''Checks in the map of relation if i is bigger than j'''
    return biggerThanMap[i] != None and j in biggerThanMap[i]


def getBiggerThanMap(orders):
    '''Gets the map of relation between numbers from a list of relation.
    Note: it's not transitive !!! '''
    biggerThanMap = {}
    for less, more in orders:
        if (more not in biggerThanMap):
            biggerThanMap[more] = {less}
        else:
            biggerThanMap[more].add(less)
    return biggerThanMap


def getMiddleInt(liste):
    '''Gets the middle of the list as an integer'''
    middleIndex = int((len(liste)-1)/2)
    return int(liste[middleIndex])
