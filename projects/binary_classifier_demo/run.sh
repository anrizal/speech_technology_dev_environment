#!/usr/bin/env bash

DIRECTORY="$( cd "$(dirname "$0")" ; pwd -P )"

echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
echo Extracting features
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

cd models/
python3 audio2tfrecord.py
cd $DIRECTORY/../../data
if [ -d "features" ]; then
    rm -r features
    mkdir features
fi
shopt -s dotglob
mv sounds/*/*.tfrecord features

echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
echo Training
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

cd $DIRECTORY

if [ -d "trainlog" ]; then
    rm -r trainlog
fi

python3 trainer/train.py --train_data_pattern=../../data/features/*.tfrecord --num_epochs=20 --learning_rate_decay_examples=40000 --feature_names=audio_embedding --feature_sizes=128 --frame_features --batch_size=64 --num_classes=2 --train_dir=trainlog --base_learning_rate=0.001 --model=LstmModel

cd trainlog

for f in `ls -1r | head -3`; do
    filename=$(basename "$f")
    ext="${filename##*.}"
    mv $f $DIRECTORY/models/trained_model.ckpt.$ext
done

echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
echo FINISHED!
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
