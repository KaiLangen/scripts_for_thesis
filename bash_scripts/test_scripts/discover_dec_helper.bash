#!/bin/bash
if [[ $# -ne 4 ]]
then
  echo "usage ./script keyQP gopLevel vid dir"
  exit
fi

# Setup Variables
keyQP=$1
gopLevel=$2
vid=$3
dir=data/$4
out=$dir/discover
oracle=oracle_${keyQP}.yuv
rec=rec_${keyQP}_${gopLevel}.yuv

# recolour the video
echo `hostname`
cd dvc_test/
mkdir -p $out

#Usage: ./deDVC [wz varBitstream file] [key frame file]
#               [original video file] [channel] [SI Method] [helper file]
(time ./deDVC $dir/wz_u_${keyQP}_${gopLevel}.bin \
              $dir/$rec $vid u 3 $dir/$oracle > $out/dec_${keyQP}_${gopLevel}_u.log) \
2> $out/dec_time_${keyQP}_${gopLevel}.log
(time ./deDVC $dir/wz_u_${keyQP}_${gopLevel}.bin \
              $dir/$rec $vid v 3 $dir/$oracle > $out/dec_${keyQP}_${gopLevel}_v.log) \
2>> $out/dec_time_${keyQP}_${gopLevel}.log
