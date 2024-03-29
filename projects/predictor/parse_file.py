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

import numpy as np
from scipy.io import wavfile
from audio.processor import WavProcessor, format_predictions

def process_file(wav_file, ckpt_file, labels_file):
    sr, data = wavfile.read(wav_file)
    print(wav_file, end=' ')

    if data.dtype != np.int16:
        raise TypeError('Bad sample type: %r' % data.dtype)
    
    predictions = []
    with WavProcessor(ckpt_file, labels_file) as proc:
        try:
            predictions = proc.get_predictions(sr, data)
            print(format_predictions(predictions))
        except:
            print('CORRUPTED!')
    return predictions
