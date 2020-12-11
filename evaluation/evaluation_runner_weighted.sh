#!/bin/bash

set -ex
graph_sets='small_graphs'
#scenarios='full plateauBound withoutBucketQueue'
scenarios='weighted matrix'
#scenarios='full plateauBound'
seeds='0 1 2 3 4 5 6 7 8 9'

declare -A graphs
graphs=(["small_graphs"]='lesmis jazz karate'
["social_network"]='amazon.edgelist facebook100/Caltech36.mat dblp.edgelist youtube.edgelist facebook100/Penn94.mat'
["web"]='cnr-2000.graph in-2004.graph eu-2005.graph')

declare -A weights
weights=(["small_graphs"]='lesmis.csv jazz.csv karate.csv')

for graph_set in $graph_sets; do
  for scenario in $scenarios; do
    graph_list=${graphs[$graph_set]}
    for graph in $graph_list; do
      for seed in $seeds; do
        if [ $scenario == "weighted" ]; then
          python3 evaluation_weighted.py -g ${graph}".graph" -p "../output/QTM_matrix/${graph_set}/temp_${scenario}/" -s ${scenario} -r ${seed} &
        else
          python3 evaluation_weighted.py -g ${graph}".graph" -w ${graph}".csv" -p "../output/QTM_matrix/${graph_set}/temp_${scenario}/" -s ${scenario} -r ${seed} &
        fi  
      done
      wait
    done
    python3 means.py -p "../output/QTM_matrix/${graph_set}/temp_${scenario}/"
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
