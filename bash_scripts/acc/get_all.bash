videos=(foreman akiyo football mobile flower 1507.2016.1108.images8)
script=$1

for vid in ${videos[@]}
do
  ./$script $vid
done
