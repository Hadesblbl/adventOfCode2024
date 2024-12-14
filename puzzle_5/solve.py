import utils.utils as utils

fileName = "puzzle_5/input.txt"

def solve():
    print("Solving puzzle 5 of Advent of Code 2024")
    order, lines = utils.readLinesSeparatedByEmptyLines(fileName)
    biggerThan = getBiggerThanMap(order)
    somme=0
    for line in lines:
        liste=line.split(",")
        if(not isOrdered(liste,biggerThan)):
            continue
        somme += getMiddleInt(liste)
    print(somme)
    
    somme=0
    for line in lines:
        liste=line.split(",")
        if(isOrdered(liste,biggerThan)):
            continue
        liste = sort(liste,biggerThan)
        somme += getMiddleInt(liste)
    print(somme)

# It's not transitive !!
def getBiggerThanMap(orders):
    biggerThanMap = {}
    for order in orders:
        less,more=order.split("|")
        if (more not in biggerThanMap):
            biggerThanMap[more]={less}
        else:
            biggerThanMap[more].add(less)
    return biggerThanMap

def isBigger(i,j,biggerThanMap):
    return biggerThanMap[i] != None and j in biggerThanMap[i]

def isOrdered(liste, biggerThanMap):
    for i in range(len(liste)):
        # Verification de tous les chiffres à gauche
        for j in range(i):
            # Si un chiffre à gauche est plus grand, ce n'est pas ordonné
            if isBigger(liste[j],liste[i],biggerThanMap):
                return False
    return True

def getMiddleInt(liste):
    middleIndex=int((len(liste)-1)/2)
    return int(liste[middleIndex])


# Special sort because bigger is not transitive !
def sort(liste,biggerThan):
    while(not isOrdered(liste,biggerThan)):
        # compare the indexes and swap those that are not ordered until it's good
        for firstIndex in range(len(liste)):
            for secondIndex in range(firstIndex+1,len(liste)):
                if isBigger(liste[firstIndex],liste[secondIndex],biggerThan):
                    utils.swap(liste,firstIndex,secondIndex)
    return liste