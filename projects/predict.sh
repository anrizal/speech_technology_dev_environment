#!/usr/bin/env bash

DIRECTORY="$( cd "$(dirname "$0")" ; pwd -P )"
audio_path=""
labels_path=""
checkpoint_path=""
result_path="predictions.csv"

OPTINT=0

while getopts "a:l:c:d:" opt; do
    case "$opt" in
    a)  audio_path=$OPTARG
        ;;
    l)  labels_path=$OPTARG
        ;;
    c)  checkpoint_path=$OPTARG
        ;;
    d)  result_path=$OPTARG
        ;;
    esac
done

[ -z "$labels_path" ] && labels_path="${audio_path}/class_labels_indices.csv"

echo
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
echo Predicting
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
echo

ckpt_prefix=$(grep -o -m 1 'model\.ckpt-\d*' ${checkpoint_path}/checkpoint)
ckpt_model_path="${checkpoint_path}/${ckpt_prefix}"

python3 predictor/predict.py --source $audio_path --labels $labels_path --ckpt $ckpt_model_path --dest $result_path
ret=$?
if [ $ret -ne 0 ]; then
    exit 1
fi

echo
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
echo FINISHED!
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
echo
