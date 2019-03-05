### Preparation

Remember to put the sample file in the `data` folder under the root folder, so it looks like this:

    speech_technology_dev_environment
    |___data
        |___sounds
            |___clean_data
                |___train
                    |___hungry
                        |___*.wav
                    |___tired
                        |___*.wav
                    |___... (Other audio sources)
                |___validation
                    |___... (Same as training)
                |___test
                    |___... (Same as training)
                |___class_labels_indices.csv

(Bear me for not putting this as a parameter in the shell script..)

Also Github doesn't like files over 100MB (unless you pay them), so head to [this page](http://s3.amazonaws.com/audioanalysis/models.tar.gz), download, unzip and copy the `vggish_model.ckpt` file to `binary_classifier_demo/models`.

### Training

`bash train.sh`, for help run `bash train.sh -h`

Example

    bash train.sh -a ../data/sounds/clean_data/train -l ../data/sounds/clean_data/class_labels_indices.csv -f ../data/sounds/clean_data/test/features -d ../data/trainlog

### Predictions

Run `sh predict.sh`. for help run `bash predict.sh -h`

Example 
    
    sh predict.sh -a ../data/sounds/clean_data/validation -l ../data/sounds/clean_data/class_labels_indices.csv -c ../data/trainlog -d ../data/results/validation/predictions.csv
