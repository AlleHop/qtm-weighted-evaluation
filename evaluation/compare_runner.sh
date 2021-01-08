#!/bin/bash

set -ex
graph_sets='biological'
qtm="../bio_exact_solution/matrix_minimum_sorted.csv"
exact="../bio_exact_solution/bio-solutions.csv"

python3 python_scripts/compare_to_exact.py "${qtm}" "${exact}" &
wait
