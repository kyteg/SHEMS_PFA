import state
import policy
import os

data = []
for file in os.listdir("leave_return_times_data/"):
    path = "leave_return_times_data/"+file
    with open(path, 'r') as f:
        data.append(f.read())

print(data[1])


p = policy()
s = state(policy, )
