#!/bin/bash

set -ex
graph_sets='biological'
file1="graph_lists/bio_cm_files_list.txt"
file2="graph_lists/bio_list.txt"


declare -A graphs
graphs=(["biological"]='cost_matrix_component_nr_1_size_9_cutoff_10.0.cm')

paste -d@ $file1 $file2 | while IFS="@" read -r f1 f2
do
  python3 python_scripts/convert_cm_to_csv.py "../../input/biological/cm_files/${f1}" "../../input/biological/weights/${f2}.csv" &
  wait
done
