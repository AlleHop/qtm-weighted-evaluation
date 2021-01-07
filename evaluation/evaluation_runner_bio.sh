#!/bin/bash

set -ex
graph_sets='biological'
#scenarios='full plateauBound withoutBucketQueue'
scenarios='matrix'
#scenarios='full plateauBound'
seeds='0 1 2 3 4 5 6 7 8 9'

declare -A graphs
graph_files=(["biological"]="bio_list.txt")

for graph_set in $graph_sets; do
  for scenario in $scenarios; do
    input="bio_list.txt"
    echo "$input"
    paste -d@ $input $input | while IFS="@" read -r graph f2
    do
      echo "$line"
      for seed in $seeds; do
        if [ $scenario == "weighted" ]; then
          python3 evaluation_bio.py -g "${graph}.graph" -p "../output/QTM_bio/${graph_set}/temp_${scenario}/" -s ${scenario} -r ${seed} &
        else
          python3 evaluation_bio.py -g "${graph}.graph" -w "${graph}.csv" -p "../output/QTM_bio/${graph_set}/temp_${scenario}/" -s ${scenario} -r ${seed} &
        fi  
    done
    wait
  done
  python3 means.py -p "../output/QTM_bio/${graph_set}/temp_${scenario}/"
  python3 minimum_editcost.py -p "../output/QTM_bio/${graph_set}/temp_${scenario}/"
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
