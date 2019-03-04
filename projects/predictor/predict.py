from absl import flags, app
from prediction_writer import PredictionWriter
from parse_file import process_file

import os
import glob
import csv

FLAGS = flags.FLAGS
flags.DEFINE_string("source", None, "Path to the audio resources")
flags.DEFINE_string("labels", None, "Path to the csv file which records the relationship between a label and its index number")
flags.DEFINE_string("ckpt", None, "Path and prefix to the training checkpoint file")
flags.DEFINE_string("dest", 'predictions.csv', "Path to write the predicitons result csv")
flags.mark_flags_as_required(['source', 'labels', 'ckpt'])

def read_class_labels():
    with open(FLAGS.labels) as f:
        reader = csv.DictReader(f)
        result = [row['display_name'] for row in reader]
        return result

def main(argv):
    del argv

    labels = read_class_labels()
    with PredictionWriter(labels, FLAGS.dest) as pwriter:
        pwriter.write_headers()
        for filepath in glob.glob(FLAGS.source + '/**/*.wav', recursive=True):
            filename = os.path.basename(filepath)
            predictions = process_file(filepath, FLAGS.ckpt, FLAGS.labels)
            pwriter.write_row(filename, predictions)
            

if __name__ == '__main__':
    app.run(main)
