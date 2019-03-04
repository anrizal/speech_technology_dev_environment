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

import csv
import operator

class PredictionWriter(object):
    def __init__(self, labels, path):
        self._labels = labels
        self._headers = ['file_name'] + self._labels + ['final_prediction']
        self._file = open(path, 'w')
        self._writer = csv.DictWriter(self._file, fieldnames=self._headers)
    
    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()
    
    def close(self):
        if self._file:
            self._file.close()

    def write_headers(self):
        self._writer.writeheader()
    
    def write_row(self, filename, predicitons):
        row = self._format_csv_row(filename, predicitons)
        self._writer.writerow(row)
    
    def _format_csv_row(self, filename, predictions):
        result = {p[0]: p[1] for p in predictions}
        result['file_name'] = filename
        max_label = max(predictions, key=operator.itemgetter(1))[0]
        result['final_prediction'] = max_label
        return result
