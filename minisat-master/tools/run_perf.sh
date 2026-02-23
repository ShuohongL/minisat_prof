#!/usr/bin/env bash
set -euo pipefail

# Defaults
#CNF_FILE="${1:-./inputs/sat100.cnf}"
CNF_FILE="${1:-./inputs/32v_160c_test1.cnf}"
OUT_FILE="${2:-./perf_output/result.txt}"

# Build
make clean
make CXXFLAGS="${CXXFLAGS:-} -DHEAP_PROFILE -g -O2 -march=native -fno-omit-frame-pointer"

# Prepare System
sudo cpupower frequency-set -g performance
taskset -c 0 true  # ensure core 0 is available

# Warm up:
taskset -c 0 ./build/release/bin/minisat "$CNF_FILE" "$OUT_FILE" 2>&1 | tee ./perf_output/solver.log >/dev/null

# Measured runs:
taskset -c 0 ./build/release/bin/minisat "$CNF_FILE" "$OUT_FILE" 2>&1 | tee ./perf_output/solver.log
