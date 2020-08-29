# video specific information from external file
# should provide the following variables:
#   qp_lut  - look up table for QP vals
#   FMT     - CIF or QCIF
#   nframes - number of frames to enc/dec
#   vid     - full name of vid
#   name    - name for output dir (foreman, akiyo, etc.)
name=$1
source ../${name}_data.bash

myPwd=`pwd`

rsa_keys=/student/kjl408/.ssh/id_test
script=$myPwd/discover_dec_helper.bash
for gopLevel in {1..4}
do
  for i in {1..7}
  do
    keyQP=${qp_lut[((i-1))]}
    WORKER="discus-spark$i"
    (ssh -i $rsa_keys kai@$WORKER 'bash -s' \
	    < $script $keyQP $gopLevel $vid $name) &
  done
  wait
done
echo "Decoding completed!"

