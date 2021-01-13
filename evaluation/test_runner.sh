#!/bin/bash

set -ex
graph_sets='biological'
#scenarios='full plateauBound withoutBucketQueue'
scenarios='matrix'
#scenarios='full plateauBound'
seeds='0 1 2 3 4 5 6 7 8 9'

declare -A graphs
graphs=(["biological"]="bio-nr-3261-size-13")

for graph_set in $graph_sets; do
  for scenario in $scenarios; do
    graph_list=${graphs[$graph_set]}
    for graph in $graph_list; do
      for seed in $seeds; do
        if [ $scenario == "weighted" ]; then
          python3 python_scripts/evaluation_bio.py -g "${graph}.graph" -p "../output/QTM_error/${graph_set}/temp_${scenario}/" -s ${scenario} -r ${seed} &
        else
          python3 python_scripts/evaluation_bio.py -g "${graph}.graph" -w "${graph}.csv" -p "../output/QTM_error/${graph_set}/temp_${scenario}/" -s ${scenario} -r ${seed} &
        fi  
    done
    wait
  done
  python3 python_scripts/means.py -p "../output/QTM_error/${graph_set}/temp_${scenario}/"
  wait
  python3 python_scripts/minimum_editcost.py -p "../output/QTM_error/${graph_set}/temp_${scenario}/"
  wait
  done
done


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
