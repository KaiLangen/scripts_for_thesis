#!/bin/bash
cd /discus/kai/recolouring_analysis/bash_scripts/acc/
vidName=$1

dataDir=~/dvc_test/data/$vidName

for file in `ls $dataDir/stats_[0-9][0-9].dat`;
do
  echo $file;
  awk '
    $1 == "Mode" && $2 == "|" {print $1 ": " $3};
    $1 == "Coeffs." {print $1 " " $2 ": " $4};
    $1 == "average" {print $1 ": " $4};
  ' $file;
done
