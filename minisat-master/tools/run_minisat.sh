#!/usr/bin/env bash
set -euo pipefail
if [ -f ./output/heap_trace.txt ]; then rm ./output/heap_trace.txt; fi

# Defaults
#CNF_FILE="${1:-./inputs/sat100.cnf}"
CNF_FILE="${1:-./inputs/test.cnf}"
OUT_FILE="${2:-output/result.txt}"

# Build
( make distclean || true ) &&
make config &&
make cr CPP=-std=c++11 MINISAT_REL='-O3 -DNDEBUG -DHEAP_DEBUG'

# Run
./build/release/bin/minisat_core -verb=2 "$CNF_FILE" "$OUT_FILE" 1>output/solver.log 2>output/heap.log

echo "Done. Output -> $OUT_FILE | stdout -> output/solver.log | stderr -> output/heap.log"
