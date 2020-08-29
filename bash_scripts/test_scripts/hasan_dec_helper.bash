#!/bin/bash
if [[ $# -ne 5 ]]
then
  echo "usage ./script keyQP gopLevel vid out nframes"
  exit
fi

keyQP=$1
gopLevel=$2
vid=$3
dir=data/$4
nframes=$5
out=$dir/hasan
oracle=oracle_${keyQP}.yuv

echo `hostname`
cd dvc_test/
mkdir -p $out

# generate configFile
configFile=$out/dec_config_${1}_${2}.cfg
touch $configFile
echo "InputFile=$vid" >> $configFile
echo "KeyFile=$dir/$oracle" >> $configFile
echo "MVFile=mv.csv" >> $configFile
echo "FramesToBeEncoded=$nframes" >> $configFile
echo "SequenceType=CIF" >> $configFile
echo "Method=3" >> $configFile
echo "GopLevel=$gopLevel" >> $configFile
echo "Param=25" >> $configFile
echo "BlockSize=8" >> $configFile
echo "RefFrames=1" >> $configFile
echo "threshold=17" >> $configFile

(time ./colour $configFile > $out/dec_$1_$2.log) 2> $out/dec_time_$1_$2.log
rm $configFile
