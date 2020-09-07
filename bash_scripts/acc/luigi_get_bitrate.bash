# video/codec specific information
vidName=$1

machines=(1 2 3 4 5 6 7 8 9)
myPwd=`pwd`
outDir=data/bitrates/
mkdir -p  $outDir

outFile=$outDir/$vidName.bitrate.txt
rm -f $outFile

for i in {0..6}
do
  WORKER="discus-spark${machines[i]}"
  rsa_keys=/student/kjl408/.ssh/id_test
  script=$myPwd/spark_get_bitrate.bash
  (ssh kai@$WORKER -i $rsa_keys 'bash -s' < $script $vidName $i) >> $outFile 
done
wait
echo "Collected bitrate for $vidName..."

