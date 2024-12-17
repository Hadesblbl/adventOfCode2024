import utils.utils as utils

fileName = "puzzle_9/input.txt"


def solve():
    print("Solving puzzle 9 of Advent of Code 2024")
    numStr = utils.readFile(fileName)
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
    '''Gets the array representation of the file layout'''
    result = []
    isFile = True
    numFile = 0
    for digit in digitList:
        if isFile:
            result += [numFile]*digit
            numFile += 1
        else:
            result += ["."]*digit
        isFile = not isFile
    return result


def checksum(numStr):
    '''Calculates the checksum of a file system'''
    return sum([int(numStr[i])*i for i in range(len(numStr)) if numStr[i] != "."])


def rearrange(numStr):
    '''Rearranges character by character from the last to the first.
    Every time an empty character is found to the left of a file, swaps them'''
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
    '''Rearranges block by block from the last to the first. 
    For that purpose, keeps track of the list of empty block and how much of each of them is filled. 
    File blocks are never empty so empty blocks never need to be concatenated.
    For each file, search an empty spot large enough then swaps it with it when found'''
    fill = [0 for i in range(len(numList))]
    indexBlock = len(numStr)-1
    fileId = numStr[indexBlock]
    while (fileId > 0):
        sizeBlock = numList[fileId*2]
        indexEmpty = 0
        for i in range(len(numList)):
            if indexEmpty > indexBlock:
                break
            # if empty block with enough space, swaps its empty space with file
            # then stop searching empty area for that file
            if i % 2 == 1 and numList[i] - fill[i] >= sizeBlock:
                indexEmpty += fill[i]
                for j in range(sizeBlock):
                    utils.swap(numStr, indexBlock-j, indexEmpty+j)
                fill[i] += sizeBlock
                break
            indexEmpty += numList[i]
        # skip to next file block
        indexBlock -= sizeBlock+numList[fileId*2-1]
        fileId -= 1
