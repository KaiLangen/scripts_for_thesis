#!/bin/bash
if [[ $# -ne 6 ]]
then
  echo "$*"
  echo "usage: $0 keyQP FMT nFrames gopLevel vid name"
  exit
fi

# Setup Variables
keyQP=$1
FMT=$2
frames=$3
gopLevel=$4
vid=$5
dir=nomo_data/$6
oracle=oracle_${keyQP}.yuv
if [ "$2" == "CIF" ]; then
  w=352
  h=288
else
  w=172
  h=144
fi

# encode the Intra-coded video
echo `hostname`
cd dvc_test/
mkdir -p $dir
cd jm
# encode the key-frame video
gop=$((1<<gopLevel))
if [[ gopLevel -eq 1 ]]
then
  echo "Encoding key frames with QP $keyQP"
  ./lencod_64.exe -d encoder_intra_main.cfg \
                  -p InputFile="$vid" \
                  -p ReconFile="../$dir/$oracle" \
                  -p QPISlice=$keyQP \
                  -p SourceWidth=$w \
                  -p SourceHeight=$h \
                  -p FramesToBeEncoded=$frames > jm.log
  mv stats.dat ../$dir/stats_${keyQP}.dat
fi
exit
