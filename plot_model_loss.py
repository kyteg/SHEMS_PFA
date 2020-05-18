import matplotlib.pyplot as plt

with open('model1_loss', 'r') as f:
    loss = f.readline()

loss = loss.split('[')[1].split(']')[0].split(', ')
for i in range(len(loss)):
    loss[i] = float(loss[i])

plt.plot(loss, '.')
plt.show()
