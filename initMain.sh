#!/bin/bash
main=""
for i in {1..25}
do
    puzzleName="puzzle_$i"
    main="${main}import $puzzleName.solve as solve$i\n"
done

main="$main\n\n"
for i in {1..25}
do
    main="${main}solve$i.solve()\n"
done

echo "$main" > __main__.py