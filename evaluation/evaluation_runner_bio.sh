#!/bin/bash

set -ex
graph_sets='biological'
#scenarios='full plateauBound withoutBucketQueue'
scenarios='biosubtreeMove biounweighted'
#scenarios='full plateauBound'
seeds='0 1 2 3 4 5 6 7 8 9'
output_name='QTM_subtree'

declare -A graph_files
graph_files=(["biological"]="graph_lists/bio_list.txt")

for graph_set in $graph_sets; do
  for scenario in $scenarios; do
    #input="graph_lists/bio_list1.txt"
    input=${graph_files[$graph_set]}
    echo "$input"
    paste -d@ $input $input | while IFS="@" read -r graph f2
    do
      echo "$line"
      for seed in $seeds; do
        if [ $scenario == "bioweighted" -o $scenario == "biounweighted" ]; then
          python3 python_scripts/evaluation_bio.py -g "${graph}.graph" -p "../output/${output_name}/${graph_set}/temp_${scenario}/" -s ${scenario} -r ${seed} &
        else
          python3 python_scripts/evaluation_bio.py -g "${graph}.graph" -w "${graph}.csv" -p "../output/${output_name}/${graph_set}/temp_${scenario}/" -s ${scenario} -r ${seed} &
        fi  
      done
      wait
  done
  wait
  python3 python_scripts/minimum_editcost.py -p "../output/${output_name}/${graph_set}/temp_${scenario}/"
  wait
  python3 python_scripts/all.py -p "../output/${output_name}/${graph_set}/temp_${scenario}/"
  wait
  python3 python_scripts/time_per_iter.py -p "../output/${output_name}/${graph_set}/temp_${scenario}/"
  wait
  python3 python_scripts/calculate_variance.py -p "../output/${output_name}/${graph_set}/temp_${scenario}/"
  wait
  python3 python_scripts/sort.py -p "../output/${output_name}/${graph_set}/"
  wait
  if [ $scenario == "biounweighted" ]; then
    exact="../bio_exact_solution/bio-solutions-unweighted.csv"
    python3 python_scripts/compare_to_exact_unweighted.py "../output/${output_name}/${graph_set}/sorted/${scenario}_minimum_sorted.csv" "${exact}"
  else
    exact="../bio_exact_solution/bio-solutions.csv"
    python3 python_scripts/compare_to_exact.py "../output/${output_name}/${graph_set}/sorted/${scenario}_minimum_sorted.csv" "${exact}"
  fi
  wait
  done
done
python3 performance/performance_plot.py -p "../output/${output_name}/${graph_set}/"
wait
python3 performance/timeIteration_plot.py -p "../output/${output_name}/${graph_set}/"
wait