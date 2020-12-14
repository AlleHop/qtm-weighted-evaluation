#!/bin/bash

set -ex
graph_sets='biological'
file1="bio_cm_files_list.txt"
file2="bio_graph_list.txt"


declare -A graphs
graphs=(["biological"]='cost_matrix_component_nr_1_size_9_cutoff_10.0.cm')

paste -d@ $file1 $file2 | while IFS="@" read -r f1 f2
do
  python3 convert_cm_to_metis.py "../../input/biological/cm_files/${f1}" "../../input/biological/graphs/${f2}" &
  wait
done
