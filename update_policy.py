import state
import policy
import random
import numpy as np
from get_loss_func import get_target
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

discount = 0.97
train_iter = 10000

#define our model
input = Input(shape=(5,))
a = Dense(32, activation = 'relu')(input)
b = Dense(32, activation = 'relu')(a)
output = Dense(8, activation = 'softmax')(b)
model = Model(inputs=input, outputs=output)

model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics=['accuracy'])

#initialise the policy and state.
with open("ev_profiles/LIF_CYC1.txt") as f:
    evprofile = f.readline()
evprofile = evprofile.split('[')[1].split(']')[0].split(', ')
for i in range(len(evprofile)):
    evprofile[i] = float(evprofile[i])

p = policy.Policy()
s = state.State(policy, evprofile)

for i in range(train_iter):
    print(i/train_iter)
    policy = model.predict(np.array([s.return_state()])).tolist()
    p.manual_update(policy.index(max(policy)))
    s.update(p)
    target = get_target(s, discount)[0]
    print(target)
    print(policy)
    model.fit(np.array([s.return_state()]), np.array([target]))

for i in range(100):
    pred = model.predict(np.array([s.return_state()])).tolist()
    option = pred.index(max(pred))
    p.manual_update(option)
    s.update(p)
    print("time = {}".format(s.time))
    print("policy selection - EV charging = {}, battery charging = {}, var charging = {}".format(*p.selection()))
    #print state vars here
    print("Money received (reward) this interval is {}".format(s.reward()))
