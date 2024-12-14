#!/bin/bash

function getFile(){
    number="$1"
    fileContent="import utils.utils as utils\n\
\n\
fileName = \"puzzle_${number}/input.txt\"\n\
\n\
def solve():\n\
    print(\"Solving puzzle $number of Advent of Code 2024\")\n\
\n\
    "
    echo "$fileContent"
}
    

for i in {1..25}
do
    puzzleName="puzzle_$i"
    mkdir "$puzzleName"
    cd "$puzzleName" || exit -1
    echo ""> "input.txt"
    echo "$(getFile $i)" > "solve.py"
    cd .. || exit -1
done
