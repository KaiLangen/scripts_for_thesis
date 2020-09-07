#!/bin/bash
cd /discus/kai/recolouring_analysis/bash_scripts/acc/
vidName=$1
qpLevel=$2

codecNames=(discover proposed hasan mcr_fast)
dataDir=~/dvc_test/data/$vidName

for codec in "${codecNames[@]}"
do
  python parse_output.py $dataDir $codec $qpLevel > tmp/$codec.$vidName.$qpLevel.dat
done
