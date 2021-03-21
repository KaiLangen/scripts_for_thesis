#!/bin/bash
if [[ $# -ne 4 ]]
then
  echo "usage ./script keyQP gopLevel vid out"
  exit
fi

keyQP=$1
gopLevel=$2
vid=$3
dir=nomo_data/$4
out=$dir/proposed
gop=$((1<<gopLevel))
oracle=$dir/oracle_${keyQP}.yuv
rec=$dir/rec_nomo${gop}.${keyQP}.yuv
wz=$dir/wz_${keyQP}_${gopLevel}.bin

echo `hostname`
cd dvc_test/
mkdir -p $out

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

(time ./decoder $configFile $vid > $out/dec_$1_$2.log) 2> $out/dec_time_$1_$2.log
#rm $configFile
