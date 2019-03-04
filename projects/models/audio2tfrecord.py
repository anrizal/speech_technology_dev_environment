# Mine
# convert from audio to tfrecods
# referenced vggish_inference_demo.py

from __future__ import print_function

import numpy as np
from scipy.io import wavfile
import six
import tensorflow as tf
from absl import flags

import vggish_input
import vggish_params
import vggish_postprocess
import vggish_slim
import glob
import os
import csv
import sys

FLAGS = flags.FLAGS
SELF_DIR = os.path.dirname(os.path.realpath(__file__))
flags.DEFINE_string("source", None, "Path to the audio resources")
flags.DEFINE_string("labels", None, "Path to the csv file which records the relationship between a label and its index number")
flags.DEFINE_string("dest", None, "Path to write extracted features")
flags.mark_flag_as_required('source')

def extract_features(dirname, label):
  pproc = vggish_postprocess.Postprocessor(os.path.join(SELF_DIR, "vggish_pca_params.npz"))

  for wav_file in glob.glob(dirname + "*.wav"):
    print(wav_file)
    try:
      examples_batch = vggish_input.wavfile_to_examples(wav_file)
    except:
      continue
    tfrecord_path = os.path.join(
      FLAGS.dest, os.path.basename(wav_file)[:-3] + "tfrecord")
    writer = tf.python_io.TFRecordWriter(tfrecord_path)

    with tf.Graph().as_default(), tf.Session() as sess:
      vggish_slim.define_vggish_slim(training=False)
      vggish_slim.load_vggish_slim_checkpoint(sess, os.path.join(SELF_DIR, "vggish_model.ckpt"))
      features_tensor = sess.graph.get_tensor_by_name(
          vggish_params.INPUT_TENSOR_NAME)
      embedding_tensor = sess.graph.get_tensor_by_name(
          vggish_params.OUTPUT_TENSOR_NAME)
      try:
        [embedding_batch] = sess.run([embedding_tensor],
                                     feed_dict={features_tensor: examples_batch})
      except:
        continue
      postprocessed_batch = pproc.postprocess(embedding_batch)

      nBatches = len(postprocessed_batch)

      if nBatches < 10:
        nBatches = 1
      else:
        nBatches = int(nBatches / 10)
      
      for i in range(nBatches):
        seq_example = tf.train.SequenceExample(
            context=tf.train.Features(
                feature={
                    "labels": tf.train.Feature(int64_list=tf.train.Int64List(value=[label]))                    
                }
            ),
            feature_lists=tf.train.FeatureLists(
                feature_list={
                    vggish_params.AUDIO_EMBEDDING_FEATURE_NAME:
                        tf.train.FeatureList(
                            feature=[
                                tf.train.Feature(
                                    bytes_list=tf.train.BytesList(
                                        value=[embedding.tobytes()]))
                                for embedding in postprocessed_batch[i*10:i*10+10]
                            ]
                        )
                }
            )
        )

        if writer:
          writer.write(seq_example.SerializeToString())

    if writer:
      writer.close()

def main(argv):
  del argv

  if not os.path.exists(FLAGS.source):
    print('ERROR! No audio resources at {}'.format(FLAGS.source))
    sys.exit(2)

  if not os.path.exists(FLAGS.labels):
    print('ERROR! No label mapping csv file at {}'.format(FLAGS.labels))
    sys.exit(2)

  if not os.path.exists(FLAGS.dest):
    os.mkdir(FLAGS.dest)

  with open(FLAGS.labels, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      subpath = os.path.join(FLAGS.source, row['display_name'], '')
      extract_features(subpath, int(row['index']))

if __name__ == '__main__':
  tf.app.run()
