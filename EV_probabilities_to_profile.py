"""
converts the leave and return time probabilities into a ev at home probability profile
by conducting many experiments and seeing when the ev is at home.
"""

import os
import random

loops = 100000

for i in range(1, 11):

    count = 0

    #print out progress:
    print("progress = {}%".format((i-1)*10))

    #import the data:
    filepath = "leave_return_times_data/"+str(i)+"/LIF_CYC = "+str(i)+"_coming.txt"
    with open(filepath, 'r') as f:
        coming = f.readline()
    coming = coming.split('[')[1].split(']')[0].split(', ')
    for j in range(len(coming)):
        coming[j] = float(coming[j])
    filepath = "leave_return_times_data/"+str(i)+"/LIF_CYC = "+str(i)+"_leaving.txt"
    with open(filepath, 'r') as f:
        leaving = f.readline()
    leaving = leaving.split('[')[1].split(']')[0].split(', ')
    for j in range(len(leaving)):
        leaving[j] = float(leaving[j])

    #set some variables:
    ev_profile =[0 for i in range(24)]
    ev_home = False
    #run the experiments
    for j in range(loops):
        time = j%24
        if time == 0:
            count += 1
            leave_prob = 0
            return_prob = 0
            ev_home = True
            yet_to_switch = True
        leave_prob += leaving[time]
        return_prob += coming[time]

        if ev_home:
            #ev was home last interval.
            ev_profile[time] += 1
            if random.randint(0, 1000000) < 1000000*leave_prob and yet_to_switch:
                ev_home = False
        else:
            #ev was not home last interval.
            if random.randint(0, 1000000) < 1000000*return_prob:
                ev_home = True
                yet_to_switch = False


    #cleaning up data:
    for j in range(len(ev_profile)):
        ev_profile[j] = ev_profile[j]/(count)

    #export the results
    filepath = "ev_profiles/LIF_CYC"+str(i)+".txt"
    with open(filepath, 'w') as f:
        f.write(str(ev_profile))
