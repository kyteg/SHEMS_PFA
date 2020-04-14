"""
Trains policy function neural network using reinforement learning.

todo:
create a state vector that changes as a function of time in a realistic manner.
train a neural network using tensorflow using reinforcement leanrning.
test the neural network.
"""

reward = sell_to_grid + pull_from_grid + (1-ev_charge_ratio) + (1-bat_charge_ratio) + ev_not_home*ev_charging*10000000 + time==0*flexi_not_full*10000

import state
import policy
import os
import tensorflow as tf
from tensorflow import keras


model = keras.Sequential([
            keras.layers.Dense(5, activation = 'relu'),
            keras.layers.Dense(5, activation = tf.nn.elu),
            keras.layers.Dense(3, activation = tf.nn.elu)
    ])

model.compile(optimizer = 'adam', )


with open("ev_profiles/LIF_CYC1.txt") as f:
    evprofile = f.readline()
evprofile = evprofile.split('[')[1].split(']')[0].split(', ')
for i in range(len(evprofile)):
    evprofile[i] = float(evprofile[i])

p = policy.Policy()
s = state.State(policy, evprofile)


# Define Losses
pg_loss = tf.reduce_mean((D_R - value) * tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=Y))
value_loss = value_scale * tf.reduce_mean(tf.square(D_R - value))
entropy_loss = -entropy_scale * tf.reduce_sum(aprob * tf.exp(aprob))
loss = pg_loss + value_loss - entropy_loss

# Create Optimizer
optimizer = tf.train.AdamOptimizer(alpha)
grads = tf.gradients(loss, tf.trainable_variables())
grads, _ = tf.clip_by_global_norm(grads, gradient_clip) # gradient clipping
grads_and_vars = list(zip(grads, tf.trainable_variables()))
train_op = optimizer.apply_gradients(grads_and_vars)

# Initialize Session
sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)
