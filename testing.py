import state
import policy
import os

with open("ev_profiles/LIF_CYC1.txt") as f:
    evprofile = f.readline()
evprofile = evprofile.split('[')[1].split(']')[0].split(', ')
for i in range(len(evprofile)):
    evprofile[i] = float(evprofile[i])

p = policy.Policy()
s = state.State(policy, evprofile)

for i in range(80):
    s.update(p)
    print(s.reward())
