import matplotlib.pyplot as plt
import numpy as np
import math

def demand_generator(time, ave_demand, sd):
    """
    The demand generator generates a random demand profile taking into account the average demand profile
    and the variace of the demand at each point in time.
    """
    noise = np.random.normal(0, 0.03)
    demand = ave_demand[int(time*2)] + noise
    if demand < 0:
        demand = 0
    return 2*demand

if __name__ == "__main__":
    with open("demand_profiles/demand_without_ev.txt") as f:
        demand_profile = f.readline()
    demand_profile = demand_profile.split('[')[1].split(']')[0].split(', ')
    for i in range(len(demand_profile)):
        demand_profile[i] = float(demand_profile[i])

    with open("demand_profiles/variance.txt") as f:
        variance = f.readline()
    variance = variance.split('[')[1].split(']')[0].split(', ')
    sd = [0 for i in range(len(variance))]
    for i in range(len(variance)):
        sd[i] = math.sqrt(float(variance[i]))

    time = [i/2 for i in range(48)]
    for i in range(10):
        demand = []
        for i in range(len(time)):
            demand.append(demand_generator(time[i], demand_profile, sd))
        plt.plot(demand)
        plt.show()
