# video/codec specific information
vidName=$1

machines=(1 2 3 4 5 6 7 8 9)
myPwd=`pwd`
mkdir -p tmp/
mkdir -p data/
discoverFile=data/$vidName.discover.dat
proposedFile=data/$vidName.proposed.dat
mcrFastFile=data/$vidName.mcr.fast.dat
hasanFile=data/$vidName.hasan.dat

# grab the data files in parallel
for i in {0..6}
do
  WORKER="discus-spark${machines[i]}"
  rsa_keys=/student/kjl408/.ssh/id_test
  script=$myPwd/spark_acc.bash
  (ssh kai@$WORKER -i $rsa_keys 'bash -s' < $script $vidName $i) &
done
wait
cat tmp/discover* > $discoverFile
cat tmp/proposed* > $proposedFile
cat tmp/hasan* > $hasanFile
cat tmp/mcr_fast* > $mcrFastFile
rm tmp/*
echo "Data files collected..."
