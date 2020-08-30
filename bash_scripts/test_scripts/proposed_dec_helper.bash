#!/bin/bash
if [[ $# -ne 4 ]]
then
  echo "usage ./script keyQP gopLevel vid out"
  exit
fi

keyQP=$1
gopLevel=$2
vid=$3
dir=data/$4
out=$dir/proposed
out2=$dir/hasan
oracle=$dir/oracle_${keyQP}.yuv
rec=$dir/rec_${keyQP}_${gopLevel}.yuv
wz=$dir/wz_${keyQP}_${gopLevel}.bin

echo `hostname`
cd dvc_test/
mkdir -p $out
mkdir -p $out2

##############################################################################
# New proposed method
##############################################################################
# generate configFile
configFile=$out/dec_config_${1}_${2}.cfg
touch $configFile
echo "KeyFile=$rec" >> $configFile
echo "OracleFile=$oracle" >> $configFile
echo "WZFile=$wz" >> $configFile
echo "SearchWindowSize=11" >> $configFile
echo "BlockSize=8" >> $configFile
echo "NumRefFrames=2" >> $configFile
echo "SpatialSmoothing=5" >> $configFile
echo "SearchMethod=0" >> $configFile

(time ./decoder $configFile $vid > $out/dec_$1_$2.log) 2> $out/dec_time_$1_$2.log
rm $configFile
