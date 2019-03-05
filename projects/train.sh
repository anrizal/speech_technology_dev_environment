#!/usr/bin/env bash

DIRECTORY="$( cd "$(dirname "$0")" ; pwd -P )"
audio_path=""
labels_path=""
features_path="features"
trainlog_path="trainlog"
num_classes=0
num_epochs=300
skip_feature_extraction=0

print_help () {
    echo "Usage: bash train.sh [-alnfdet]"
    echo "-a    Path to the audio source file"
    echo "-l    Path to the csv file which has the mapping for the labels"
    echo "-n    Number of the labels"
    echo "-f    Path to write the features files"
    echo "-d    Path to write the predictions file"
    echo "-e    Number of epochs"
    echo "-t    Skip feature extraction"
}

OPTINT=0

while getopts "ha:l:n:f:d:e:t" opt; do
    case "$opt" in
    h)  print_help
        exit
        ;;
    a)  audio_path=$OPTARG
        ;;
    l)  labels_path=$OPTARG
        ;;
    n)  num_classes=$OPTARG
        ;;
    f)  features_path=$OPTARG
        ;;
    d)  trainlog_path=$OPTARG
        ;;
    e)  num_epochs=$OPTARG
        ;;
    t)  skip_feature_extraction=1
        ;;
    esac
done

[ -z "$labels_path" ] && labels_path="${audio_path}/class_labels_indices.csv"
[ "$num_classes" -eq 0 ] && num_classes="$(cat $labels_path | wc -l)" && num_classes=$(($num_classes-1))

if [ ! -f models/vggish_model.ckpt ]; then
    echo "Missing models/vggish_model.ckpt, try to download from source"
    curl -o models/vggish_model.ckpt https://storage.googleapis.com/audioset/vggish_model.ckpt
fi

if [ "$skip_feature_extraction" -eq "0" ]
then
    echo
    echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    echo Extracting features
    echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    echo

    python3 models/audio2tfrecord.py --source $audio_path --labels $labels_path --dest $features_path
    ret=$?
    if [ $ret -ne 0 ]; then
        exit 1
    fi
fi

echo
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
echo Training
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
echo

shopt -s dotglob

python3 trainer/train.py --train_data_pattern="$features_path/*.tfrecord" --num_epochs=$num_epochs --learning_rate_decay_examples=40000 --feature_names=audio_embedding --feature_sizes=128 --frame_features --batch_size=64 --num_classes=$num_classes --train_dir=$trainlog_path --base_learning_rate=0.001 --model=LstmModel

echo
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
echo FINISHED!
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
echo
