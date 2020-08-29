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
dir=data/$6
oracle=oracle_${keyQP}.yuv
rec=rec_${keyQP}_${gopLevel}.yuv
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

# encode the key-frame video
gop=$((1<<gopLevel))
echo "Encoding key frames with GOP $gop, QP $keyQP"
./lencod_64.exe -d encoder_intra_main.cfg \
                -p InputFile="$vid" \
                -p ReconFile="../$dir/$rec" \
                -p QPISlice=$keyQP \
                -p FrameSkip=$(( gop-1 )) \
                -p SourceWidth=$w \
                -p SourceHeight=$h \
                -p FramesToBeEncoded=$(( (frames + 1)/gop )) > jm.log
mv stats.dat ../$dir/stats_${keyQP}_${gopLevel}.dat
cd ..;

#encode DISCOVER headers
./enDVC 0 $keyQP $frames $gopLevel u $vid \
	$dir/wz_u_${keyQP}_${gopLevel}.bin $dir/$rec > /dev/null
./enDVC 0 $keyQP $frames $gopLevel v $vid \
        $dir/wz_v_${keyQP}_${gopLevel}.bin $dir/$rec > /dev/null

# generate configFile
configFile=$dir/enc_config_${1}_${4}.cfg
wz=wz_${keyQP}_${gopLevel}.bin
touch $configFile
echo "WZFile=$dir/$wz" >> $configFile
echo "KeyFile=$dir/$rec" >> $configFile
echo "WzQP=0" >> $configFile
echo "ChrQP=0" >> $configFile
echo "KeyQP=0" >> $configFile
echo "Gop=$gop" >> $configFile
echo "NumFrames=$frames" >> $configFile
echo "SequenceType=$FMT" >> $configFile
cat $configFile

#encode PROPOSED headers
./encoder $configFile $vid #> /dev/null
rm $configFile
exit
