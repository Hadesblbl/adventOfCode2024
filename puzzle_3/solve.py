import utils.utils as utils
import re

fileName = "puzzle_3/input.txt"

def solve():
    print("Solving puzzle 3 of Advent of Code 2024")
    file = utils.readFile(fileName)
    mults = re.findall("mul\(\d+,\d+\)", file)
    somme = 0
    for mult in mults:
        digits = list(map(int, mult[4:-1].split(",")))
        somme += digits[0] * digits[1]
    print(somme)
    
    instructions = re.findall("mul\(\d+,\d+\)|do\(\)|don't\(\)", file)
    
    somme = 0
    do = True
    for instruction in instructions:
        if instruction == "do()":
            do = True
        elif instruction == "don't()":
            do = False
        elif do:
            digits = list(map(int, instruction[4:-1].split(",")))
            somme += digits[0] * digits[1]
    print(somme)