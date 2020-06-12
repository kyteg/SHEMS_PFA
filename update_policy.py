import state
import policy
import random
import numpy as np
from get_loss_func import get_target
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM
from tensorflow import expand_dims

discount = 0.97
train_iter = 50000
loss_list = []

#define our model
input = Input(shape=(5,))
exp = expand_dims(input, axis = -1)  #corrects dimentionality issues related to input to LSTM
a = LSTM(32, input_shape=(5, 1))(exp)
#a = Dense(32, activation = 'relu')(input)
b = Dense(32, activation = 'relu')(input)
output = Dense(8, activation = 'softmax')(b)
model = Model(inputs=input, outputs=output)

model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics=['accuracy'])

print(model.summary())

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
    s.print_state()
    policy = model.predict(np.array([s.return_state()])).tolist()
    target = get_target(s, discount)[0]
    print(target)
    print(policy)
    model.fit(np.array([s.return_state()]), np.array([target]))
    loss = model.evaluate(np.array([s.return_state()]), np.array([target]))
    loss_list.append(loss[0])
    p.manual_update(target.index(max(target)))
    s.update(p)
    print(p.selection())

#now save model
model.save('50000_0.97_5_32LSTM_32_8')
with open('50000_0.97_5_32LSTM_32_8.txt', 'w') as f:
    f.write(str(loss_list))

#test it
for i in range(100):
    pred = model.predict(np.array([s.return_state()])).tolist()[0]
    option = pred.index(max(pred))
    p.manual_update(option)
    s.update(p)
    print("time = {}".format(s.time))
    print("policy selection - EV charging = {}, battery charging = {}, var charging = {}".format(*p.selection()))
    #print state vars here
    print("Money received (reward) this interval is {}".format(s.reward()))
