# Copyright (C) 2017 DataArt
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import csv
from shutil import copyfile, move
import numpy as np
from scipy.io import wavfile
from audio.processor import WavProcessor, format_predictions

parser = argparse.ArgumentParser(description='Read file and process audio')
parser.add_argument('folder', type=str, help='Folder hoding files to read and process')

def process_file(wav_file):
    sr, data = wavfile.read(wav_file)
    if data.dtype != np.int16:
        raise TypeError('Bad sample type: %r' % data.dtype)

    with WavProcessor() as proc:
        predictions = proc.get_predictions(sr, data)
    print(format_predictions(predictions))
    return predictions

def write_results(directory):
    original_csv_path = os.path.join(directory, 'predictions.csv')
    new_csv_path = os.path.join(directory, 'predictions_temp.csv')

    if not os.path.exists(original_csv_path):
        with open(original_csv_path, 'w'): pass
    copyfile(original_csv_path, new_csv_path)
    with open(original_csv_path, 'r') as old_csv:
        with open(new_csv_path, 'a') as result_csv:
            writer = csv.writer(result_csv)
            reader = csv.DictReader(old_csv)
            if not old_csv.read():
                writer.writerow(['file_name', 'cry', 'others', 'prediction'])
            for filename in os.listdir(directory):
                if not filename.endswith(".wav"):
                    continue
                existed = False
                old_csv.seek(0)
                for exising_row in reader:
                    if exising_row['file_name'] == filename:
                        existed = True
                if not existed:
                    print(filename, end=' ')
                    try:
                        predictions = process_file(os.path.join(directory, filename))
                    except:
                        print('CORRUPTED!')
                        predictions = [('Corrupted', 1)]

                    row = format_csv_row(filename, predictions)
                    writer.writerow(row)
    move(new_csv_path, original_csv_path)

def format_csv_row(filename, predictions):
    row = [filename, 0, 0, 'NEGITIVE']
    for p in predictions:
        if p[0] == 'Cry':
            row[1] = p[1]
        elif p[0] == 'Others':
            row[2] = p[1]
        elif p[0] == 'Corrupted':
            row[3] = p[0]
    if row[1] > row[2] and row[3] != 'Corrupted':
        row[3] = 'POSITIVE'
    return row

if __name__ == '__main__':
    args = parser.parse_args()
    directory = vars(args)['folder']
    write_results(directory)
