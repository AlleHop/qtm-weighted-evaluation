#!/bin/bash

set -ex
graph_sets='biological'
#scenarios='full plateauBound withoutBucketQueue'
scenarios='biomatrix biosubtreeMove'
#scenarios='full plateauBound'
seeds='0 1 2 3 4 5 6 7 8 9'
output_name='QTM_subtree'

declare -A graphs
graph_files=(["biological"]="bio_list.txt")

for graph_set in $graph_sets; do
  for scenario in $scenarios; do
    input="graph_lists/bio_list.txt"
    echo "$input"
    paste -d@ $input $input | while IFS="@" read -r graph f2
    do
      echo "$line"
      for seed in $seeds; do
        if [ $scenario == "weighted" ]; then
          python3 python_scripts/evaluation_bio.py -g "${graph}.graph" -p "../output/${output_name}/${graph_set}/temp_${scenario}/" -s ${scenario} -r ${seed} &
        else
          python3 python_scripts/evaluation_bio.py -g "${graph}.graph" -w "${graph}.csv" -p "../output/${output_name}/${graph_set}/temp_${scenario}/" -s ${scenario} -r ${seed} &
        fi  
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
  exact="../bio_exact_solution/bio-solutions.csv"
  python3 python_scripts/compare_to_exact.py "../output/${output_name}/${graph_set}/sorted/${scenario}_minimum_sorted.csv" "${exact}"
  wait
  done
done
python3 performance/performance_plot.py -p "../output/${output_name}/${graph_set}/"
wait



#limit=400
#input="bio${limit}.txt"
#scenario='full'
#while IFS= read -r graph
#do
#  for seed in $seeds; do
#    python3 evaluation.py -g ${graph} -p "../output/QTM_3/biological${limit}/temp_${scenario}/" -s ${scenario} -r ${seed} &
#  done
#  wait
#done < "$input"
#python3 means.py -p "../output/QTM_3/biological${limit}/temp_${scenario}/"

#scenario='plateauBound'
#while IFS= read -r graph
#do
#  for seed in $seeds; do
#    python3 evaluation.py -g ${graph} -p "../output/QTM_3/biological${limit}/temp_${scenario}/" -s ${scenario} -r ${seed} &
#  done
#  wait
#done < "$input"
#python3 means.py -p "../output/QTM_3/biological${limit}/temp_${scenario}/"
