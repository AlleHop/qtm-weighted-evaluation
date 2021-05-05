#!/bin/bash

set -ex
graph_sets='biological'
file1="graph_lists/bio_cm_files_list.txt"
file2="graph_lists/bio_list.txt"

paste -d@ $file1 $file2 | while IFS="@" read -r f1 f2
do
  python3 python_scripts/convert_cm_to_metis.py "../../input/biological/cm_files/${f1}" "../../input/biological/graphs/${f2}.graph" &
  wait
done
