import tensorflow as tf


test_rnn = 'testRNN/models/'
model = tf.keras.models.load_model(test_rnn + 'mnist_lstm.h5')
