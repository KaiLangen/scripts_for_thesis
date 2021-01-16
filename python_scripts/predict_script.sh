# Training Data
train_bitrate=../bitrates
train_si_ti=../si_ti

# Test Data
test_bitrate=~/data/bitrates
test_si_ti=~/data/si_ti_data

python3 predict_percent_chroma.py $train_bitrate $test_bitrate $train_si_ti $test_si_ti True

python3 predict_percent_chroma.py $train_bitrate $test_bitrate $train_si_ti $test_si_ti False
