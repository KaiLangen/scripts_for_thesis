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
rec=rec_nomo$gop.$keyQP.yuv
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
echo "Encoding key frames with GOP $gop, QP $keyQP"
(time ./lencod_64.exe \
        -d encoder_intra_main.cfg \
        -p InputFile= "$vid" \
        -p ReconFile= "../$dir/$rec" \
        -p QPISlice=$keyQP \
        -p QPPSlice=$keyQP \
        -p SourceWidth=$w \
        -p SourceHeight=$h \
        -p IntraPeriod=$gop \
        -p NumberReferenceFrames=1 \
        -p DisableSubpelME=1 \
        -p SearchRange=0 \
        -p BiPredMotionEstimation=0 \
        -p FramesToBeEncoded=$frames > jm.log) 2> "../$dir/nomo_${gop}_${keyQP}_time.log"
mv stats.dat ../$dir/stats_nomo$gop.$keyQP.dat
cd ..;

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
