import state
import policy
import os

with open("ev_profiles/")

p = policy.Policy()
s = state.State(policy, evprofile)

for i in range(80):
    s.update(p)
    s.print_state()
