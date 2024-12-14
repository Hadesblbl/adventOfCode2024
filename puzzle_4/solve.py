import utils.utils as utils
import re

fileName = "puzzle_4/input.txt"
testName = "puzzle_4/test.txt"

def solve():
    print("Solving puzzle 4 of Advent of Code 2024")
    lines = utils.readFileLines(fileName)
    
    lineSize = len(lines[0])
    #Ajout de padding pour pouvoir check les diagonales sans overflow
    padding="J"*140
    concat = padding.join(lines)
    
    nbXmas = nbPatterns(concat,["XMAS","SAMX","X[A-Z]{279}M[A-Z]{279}A[A-Z]{279}S","S[A-Z]{279}A[A-Z]{279}M[A-Z]{279}X","X[A-Z]{280}M[A-Z]{280}A[A-Z]{280}S","S[A-Z]{280}A[A-Z]{280}M[A-Z]{280}X","X[A-Z]{278}M[A-Z]{278}A[A-Z]{278}S","S[A-Z]{278}A[A-Z]{278}M[A-Z]{278}X"])
    
    print(nbXmas)
    nbXmas = nbPatterns(concat,["M.S[A-Z]{278}A[A-Z]{278}M.S","S.M[A-Z]{278}A[A-Z]{278}S.M","M.M[A-Z]{278}A[A-Z]{278}S.S","S.S[A-Z]{278}A[A-Z]{278}M.M"])
    
    print(nbXmas)
    
def nbPattern(txt,pattern):
    nb=0
    index=0
    while index< len(txt):
        nextFound = re.search(pattern, txt[index:])
        if nextFound == None:
            break
        nb+=1
        index+=nextFound.start()+1
    return nb

def nbPatterns(txt,patterns):
    somme=0
    for pattern in patterns:
        somme+=nbPattern(txt,pattern)
    return somme