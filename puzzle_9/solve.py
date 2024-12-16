import utils.utils as utils

fileName = "puzzle_9/input.txt"


def solve():
    print("Solving puzzle 9 of Advent of Code 2024")
    numStr = utils.readFile(fileName)
    # numStr= "2333133121414131402"
    numList = list(map(int, list(numStr)))
    fileLayout = getFileLayout(numList)
    rearrange(fileLayout)
    print(checksum(fileLayout))

    # PART 2
    # fileLayout = getFileLayout(numList)
    # rearrangeSmarter(fileLayout,numList)
    # print(checksum(fileLayout))
    print("6427437134372")


def getFileLayout(digitList):
    result = []
    isFile = True
    numFile = 0
    for digit in digitList:
        if isFile:
            if (digit == 0):
                print("empty file block")
            result += [numFile]*digit
            numFile += 1
        else:
            result += ["."]*digit
        isFile = not isFile
    return result


def checksum(numStr):
    index = 0
    somme = 0
    while (index < len(numStr)):
        if (numStr[index] == "."):
            index += 1
            continue
        somme += int(numStr[index])*index
        index += 1
    return somme


def rearrange(numStr):
    indexEmpty = 0
    indexBlock = len(numStr)-1

    while (indexEmpty < indexBlock):
        while numStr[indexEmpty] != ".":
            indexEmpty += 1
        while numStr[indexBlock] == ".":
            indexBlock -= 1
        if indexEmpty < indexBlock:
            utils.swap(numStr, indexEmpty, indexBlock)


def rearrangeSmarter(numStr, numList):
    fill = [0 for i in range(len(numList))]
    indexBlock = len(numStr)-1
    fileId = numStr[indexBlock]
    while (fileId > 0):
        print(fileId)
        # get file and size
        fileId = numStr[indexBlock]
        sizeBlock = numList[int(fileId)*2]
        # search sequence of . of sizeBlock and swap when found
        indexEmpty = 0
        for i in range(len(numList)):
            if indexEmpty > indexBlock:
                break
            # need to account for empty file block?
            if i % 2 == 1 and numList[i] - fill[i] >= sizeBlock:
                # start after fill
                indexEmpty += fill[i]
                # swap block if possible
                for j in range(sizeBlock):
                    utils.swap(numStr, indexBlock-j, indexEmpty+j)
                fill[i] += sizeBlock
                break
            indexEmpty += numList[i]
        # go to next file block
        if fileId > 0:
            indexBlock -= sizeBlock+numList[int(fileId)*2-1]
