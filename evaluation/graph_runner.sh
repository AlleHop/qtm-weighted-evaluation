#!/bin/bash

set -ex
graph_sets='biological'
file1="graph_lists/bio_graph_list_opt.txt"

paste -d@ $file1 $file1 | while IFS="@" read -r f1 f2
do
  python3 python_scripts/convert_csv_to_graph.py "../../input/optimization/weights/${f1}.csv" "../../input/optimization/graphs/${f2}.graph" &
  wait
done
