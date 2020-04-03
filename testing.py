import state
import policy
import os

evprofile = [1 for i in range(48)]

p = policy.Policy()
s = state.State(policy, evprofile)

for i in range(80):
    s.update(p)
    s.print_state()
