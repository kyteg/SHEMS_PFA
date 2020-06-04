import matplotlib.pyplot as plt
import numpy as np

with open('demand_without_ev.txt', 'r') as f:
    demand = f.readline()

with open('variance.txt', 'r') as f:
    variance = f.readline()

demand = demand.split('[')[1].split(']')[0].split(', ')
variance = variance.split('[')[1].split(']')[0].split(', ')

for i in range(len(demand)):
    demand[i] = float(demand[i])
for i in range(len(variance)):
    variance[i] = float(variance[i])
for i in range(len(variance)):
    variance[i] = np.sqrt(variance[i])

y = np.array(demand)
x = np.array([i/2 for i in range(48)])
yer = np.array(variance)

plt.errorbar(x, y, yerr = yer, elinewidth = 0.1)
plt.fill_between(x,y-yer, y+yer, facecolor='#F0F8FF', alpha=1.0, edgecolor='#8F94CC', linewidth=1, linestyle='dashed')
xticks = [0, 6, 12, 18, 24]
xlabels = ["12:00 am", "6:00 am", "12:00 pm", "6:00 pm", "12:00 am"]
plt.xticks(xticks, labels = xlabels)
plt.title("Weekday demand profiles, 1 standard deveation")
plt.xlabel("Time of measurement")
plt.ylabel("Energy usage (kW)")
plt.ylim(0, 1.2)
plt.show()
