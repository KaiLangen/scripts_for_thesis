#!/bin/bash
cd /discus/kai/recolouring_analysis/acc/
vidName=$1
qpLevel=$2

codecNames=(discover proposed hasan)
dataDir=~/dvc_test/data/$vidName

for codec in "${codecNames[@]}"
do
  python parse_output.py $dataDir $codec $qpLevel > tmp/$codec.$vidName.$qpLevel.dat
done
