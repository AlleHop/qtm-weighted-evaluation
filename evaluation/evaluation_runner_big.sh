#!/bin/bash

set -ex
graph_sets='small social roadnetwork facebook'
#scenarios='full plateauBound withoutBucketQueue'
scenarios='unweighted'
#scenarios='full plateauBound'
seeds='0 1 2 3 4 5 6 7 8 9'
output_name='QTM_big'

declare -A graph_files
graph_files=(
  ["small"]="graph_lists/small_graph_list.txt"
  ["social"]="graph_lists/social_graph_list.txt"
  ["roadnetwork"]="graph_lists/roadnetwork_graph_list.txt"
  ["facebook"]="graph_lists/facebook_graph_list.txt")

declare -A graph_endings
graph_endings=(
  ["small"]=".graph"
  ["social"]=".ungraph.txt"
  ["roadnetwork"]=".graph"
  ["facebook"]=".mat")

for graph_set in $graph_sets; do
  input=${graph_files[$graph_set]}
  ending=${graph_endings[$graph_set]}
  for scenario in $scenarios; do
    #input="graph_lists/bio_list1.txt"
    paste -d@ $input $input | while IFS="@" read -r graph f2
    do
      for seed in $seeds; do
        python3 python_scripts/evaluation_weighted.py -i "../../input/${graph_set}/graphs/" -g "${graph}${ending}" -p "../output/${output_name}/${graph_set}/temp_${scenario}/" -s ${scenario} -r ${seed} & 
      done
      wait
  done
  wait
  python3 python_scripts/means.py -p "../output/${output_name}/${graph_set}/temp_${scenario}/"
  wait
  python3 python_scripts/minimum_editcost.py -p "../output/${output_name}/${graph_set}/temp_${scenario}/"
  wait
  python3 python_scripts/all.py -p "../output/${output_name}/${graph_set}/temp_${scenario}/"
  wait
  python3 python_scripts/calculate_variance.py -p "../output/${output_name}/${graph_set}/temp_${scenario}/"
  wait
  python3 python_scripts/sort.py -p "../output/${output_name}/${graph_set}/"
  wait
  done
done
python3 performance/performance_plot.py -p "../output/${output_name}/${graph_set}/"
wait