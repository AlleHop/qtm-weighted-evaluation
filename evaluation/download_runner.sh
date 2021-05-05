#!/bin/bash

set -ex
file1="graph_lists/social_graph_list.txt"

paste -d@ $file1 $file1 | while IFS="@" read -r f1 f2
do
  curl "https://snap.stanford.edu/data/bigdata/communities/${f1}.ungraph.txt.gz" --output "../../input/social/graphs/${f1}.ungraph.txt.gz" &
  wait
  gzip -d "../../input/social/graphs/${f1}.ungraph.txt.gz" &
  wait
done

file1="graph_lists/small_graph_list.txt"

paste -d@ $file1 $file1 | while IFS="@" read -r f1 f2
do
  curl "https://www.cc.gatech.edu/dimacs10/archive/data/clustering/${f1}.graph.bz2" --output "../../input/small/graphs/${f1}.graph.bz2" &
  wait
  bzip2 -d "../../input/small/graphs/${f1}.graph.bz2" &
  wait
done

file1="graph_lists/roadnetwork_graph_list.txt"

paste -d@ $file1 $file1 | while IFS="@" read -r f1 f2
do
  curl "https://www.cc.gatech.edu/dimacs10/archive/data/clustering/${f1}.graph.bz2" --output "../../input/roadnetwork/graphs/${f1}.graph.bz2" &
  wait
  bzip2 -d "../../input/roadnetwork/graphs/${f1}.graph.bz2" &
  wait
done

curl "https://archive.org/download/oxford-2005-facebook-matrix/facebook100.zip" --output "../../input/facebook/facebook.zip" &
wait
unzip "../../input/facebook/facebook.zip" &
wait
