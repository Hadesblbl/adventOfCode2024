import utils.utils as utils
import sys

fileName = "puzzle_2/input.txt"

def solve():
    print("Solving puzzle 2 of Advent of Code 2024")
    lines = utils.readFileLines(fileName)
    print(getNbSafer(lines))
    print(getNbSafe(lines))
    
def getNbSafer(lines):
    somme=0;
    for line in lines:
        somme+=isSafer(line)
    return somme

def getNbSafe(lines):
    somme=0;
    for line in lines:
        somme+=isSafe(line)
    return somme
    
    
def isSafer(line):
    splitted=list(map(int,line.split(" ")))
    order=splitted[1]-splitted[0]
    for i in range(len(splitted)-1):
        diff=splitted[i+1]-splitted[i]
        if diff*order < 0:
            return 0
        if diff > 3 or diff < -3 or diff==0:
            return 0
    return 1

def isSafe(line):
    if(isSafer(line)): return 1
    splitted=list(map(int,line.split(" ")))
    for i in range(len(splitted)):
        oneLess=splitted[0:i]+splitted[i+1:]
        if(isSafer(" ".join(map(str,oneLess)))):
            return 1
    return 0