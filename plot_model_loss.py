import matplotlib.pyplot as plt
import numpy as np

with open('10000_0.97_5_32LSTM_32_8_dilute.txt', 'r') as f:  #CHANGE THIS
    loss = f.readline()

loss = loss.split('[')[1].split(']')[0].split(', ')
for i in range(len(loss)):
    loss[i] = float(loss[i])

plt.plot(loss, '.')
plt.title("RNN loss against number of training iterations")
plt.ylabel("Loss")
plt.xlabel("Iteration")
plt.yticks([0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5])

plt.show()

aves = []
for i in range(0, len(loss), 100):
    sum = 0
    for j in range(100):
        sum += loss[i+j]
    ave = sum/100
    aves.append(ave)

plt.plot(aves, '.', label='')
plt.title("Conventional neural network loss against number of training iterations - bins of 100")
plt.ylabel("Loss")
plt.xlabel("Iteration/100")
x = [i for i in range(50)]
print(len(x), len(aves))
eqs = np.polyfit(x, aves, 1)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, aves, 1))(np.unique(x)), label='regression line, y={0:2f}x+{0:2f}'.format(eqs[0], eqs[1]))
plt.legend()
plt.show()
