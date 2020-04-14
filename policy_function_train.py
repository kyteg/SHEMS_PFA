"""
Trains policy function neural network using reinforement learning.

todo:
create a state vector that changes as a function of time in a realistic manner.
train a neural network using tensorflow using reinforcement leanrning.
test the neural network.
"""
import state
import policy
import os
import tensorflow as tf
from tensorflow import keras
import numpy as np

with open("ev_profiles/LIF_CYC1.txt") as f:
    evprofile = f.readline()
evprofile = evprofile.split('[')[1].split(']')[0].split(', ')
for i in range(len(evprofile)):
    evprofile[i] = float(evprofile[i])

p = policy.Policy()
s = state.State(policy, evprofile)

class ActivityRegularizationLayer(keras.layers.Layer):

  def call(self, inputs):
    self.add_loss(s.reward())
    return inputs

model = keras.Sequential([
            keras.Input(shape = (5,)),
            ActivityRegularizationLayer(),
            keras.layers.Dense(5, activation = tf.nn.elu),
            keras.layers.Dense(3, activation = tf.nn.elu),
    ])


# Create Optimizer

#model.compile(optimizer='adam',
#              loss=loss, metrics=['accuracy'])

inputs = []
for i in range(1000):
    inputs.append(np.array(s.return_state()))
    s.update(p)

inputs = np.array(inputs)

epochs = 3
for epoch in range(epochs):
  print('Start of epoch %d' % (epoch,))

  # Iterate over the batches of the dataset.
  for i in range(1000):

    # Open a GradientTape to record the operations run
    # during the forward pass, which enables autodifferentiation.
    with tf.GradientTape() as tape:

      # Run the forward pass of the layer.
      # The operations that the layer applies
      # to its inputs are going to be recorded
      # on the GradientTape.
      logits = model(inputs, training=True)  # Logits for this minibatch

      # Compute the loss value for this minibatch.
      loss_value = model()

    # Use the gradient tape to automatically retrieve
    # the gradients of the trainable variables with respect to the loss.
    grads = tape.gradient(loss_value, model.trainable_weights)

    # Run one step of gradient descent by updating
    # the value of the variables to minimize the loss.
    optimizer.apply_gradients(zip(grads, model.trainable_weights))

    # Log every 200 batches.
    if step % 200 == 0:
        print('Training loss (for one batch) at step %s: %s' % (step, float(loss_value)))
        print('Seen so far: %s samples' % ((step + 1) * 64))
