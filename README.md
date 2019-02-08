# speech_technology_dev_environment
Development Environment for Speech Technology Project

Tensorflow installation manual
https://www.tensorflow.org/install/pip


How to:
1. clone this repository
2. go to the repository folder
3. Create "projects" and "data" folder
4. vagrant up
5. vagrant ssh
6. test tensorflow by running the following command

```python
python -c "import tensorflow as tf; tf.enable_eager_execution(); print(tf.reduce_sum(tf.random_normal([1000, 1000])))"
```


let me know if there is a warning
Known warning:
Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2
It means that the CPU has capability that tensorflow is not using.

https://stackoverflow.com/questions/47068709/your-cpu-supports-instructions-that-this-tensorflow-binary-was-not-compiled-to-u
