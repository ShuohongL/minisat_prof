#!/bin/bash

input_file="./inputs/sat100.cnf"
./build/release/bin/minisat_core -verb=2 $input_file result.txt 1>solver.log 2>heap.log
