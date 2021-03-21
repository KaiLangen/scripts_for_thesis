FUNC=$(cat <<CMD
mkdir -p dvc_test
#cp /discus/kai/openDVC/bin/enDVC dvc_test/
#cp /discus/kai/openDVC/bin/deDVC dvc_test/
cp /discus/kai/multihypothesis/b/encoder dvc_test/
#cp /discus/kai/multihypothesis/b/decoder dvc_test/
#cp /discus/kai/hasan/bin/colour dvc_test/
#cp /discus/kai/multihypothesis/ldpca.tar.gz dvc_test/
#cp /discus/kai/multihypothesis/jm.tar.gz dvc_test/
#cd dvc_test
#tar xzvf ldpca.tar.gz
#tar xzvf jm.tar.gz
CMD
)

#!/bin/bash
#cp /discus/kai/multihypothesis/jm.tar.gz dvc_test/
rsa_keys=/student/kjl408/.ssh/id_test
for i in {1..9}
do
  WORKER="discus-spark$i"
  echo $WORKER
  ssh -i $rsa_keys kai@$WORKER -t "$FUNC"
done


