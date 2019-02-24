### Preparation

Remember to put the sample file in the `data` folder under the root folder, so it looks like this:

    speech_technology_dev_environment
    |___data
        |___sounds
            |___cries
                |___*.wav
            |___other
                |___*.wav
            |___... (Other audio sources)

(Bear me for not putting this as a parameter in the shell script..)

Also Github doesn't like files over 100MB (unless you pay them), so head to [this page](http://s3.amazonaws.com/audioanalysis/models.tar.gz), download, unzip and copy the `vggish_model.ckpt` file to `binary_classifier_demo/models`.

### Training

`bash run.sh`, everything should be fine.

### Predictions

Run `python3 predictor/parse_folder.py PATH_TO_YOUR_CORPUS_FOLDER`. The result will be in the corpus folder as `predictions.csv`
