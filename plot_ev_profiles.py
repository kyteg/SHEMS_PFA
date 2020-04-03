import matplotlib.pyplot as plt

def plot_ev_profiles(filepath):
    with open(filepath, 'r') as f:
        data = f.readline()
    data = data.split("[")[1].split("]")[0].split(", ")
    for i in range(len(data)):
        data[i] = float(data[i])
    plt.plot(data)
    xticks = [0, 6, 12, 18, 24]
    xlabels = ["12:00 am", "6:00 am", "12:00 pm", "6:00 pm", "12:00 am"]
    plt.title("EV profile")
    plt.ylabel('Density')
    plt.xlabel('Time of day')
    plt.xticks(xticks, labels = xlabels)
    plt.suptitle('EV profile')
    plt.title(filepath.split("/")[-1].split(".")[0], fontsize = 10)
    plt.show()

for i in range(1, 11):
    plot_ev_profiles("ev_profiles/LIF_CYC"+str(i)+".txt")
