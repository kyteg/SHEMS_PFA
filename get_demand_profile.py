import matplotlib.pyplot as plt
import datetime

cum_demand = [0 for i in range(48)]

def new_plot(time, demand, point):
    time = []
    demand = []
    demand.append(float(point[4])/2)
    time_data = point[3].split()[1].split(':')
    time_to_append = int(time_data[0]) + (1/60)*int(time_data[2])
    time.append(time_to_append)
    return (time, demand)

def is_weekday(date):
    #date is initially in the form "yyyy-mm-dd"
    date = date.split('-')
    for i in range(len(date)):
        date[i] = int(date[i])
    date = datetime.datetime(date[0], date[1], date[2])
    day = date.weekday()
    if day == 5 or day == 6:
        return False
    return True


def print_progress(count, total):

    if count%(total/10) == 0:
        print("progress = {}%".format(100*count/total))
    return
data = []
with open("../trial_cust_half_hour/CD_INTERVAL_READING.dat", 'r') as f:
    for i in range(100000):      #100000                                       #CHANGE NUMBER OF DATAPOINTS HERE!
        line = f.readline()
        if line == "":
            break
        data.append(line)

time = []
demand = []
customer_id = data[0].split(',')[0]
prev_time = float(data[0].split(',')[3].split()[1].split(':')[0]) + (1/60)*float(data[0].split(',')[3].split()[1].split(':')[1])

count = 0
for point in data:

    print_progress(count, len(data))

    point = point.split(',')
    date_time = point[3].split()
    date = date_time[0]
    time_d = date_time[1].split(':')
    if is_weekday(date):
        if point[0] == customer_id:
            time_to_append = float(time_d[0]) + (1/60)*float(time_d[1])
            if time_to_append == prev_time + 0.5:
                time.append(time_to_append)
                demand.append(float(point[4])/2)
                cum_demand[int(time_to_append*2)] += float(point[4])/2
            else:
                plt.plot(time, demand)  #divide demand by two to convert kW to kWh
                time, demand = new_plot(time, demand, point)
                cum_demand[int(time[0]*2)] += demand[0]/2
        else:
            plt.plot(time, demand)
            time, demand = new_plot(time, demand, point)
            cum_demand[0] += demand[0]/2
        customer_id = point[0]
        prev_time = time_to_append
    count+=1

yticks = [0, 2, 4]
xticks = [0, 6, 12, 18, 24]
xlabels = ["12:00 am", "6:00 am", "12:00 pm", "6:00 pm", "12:00 am"]
plt.yticks(yticks)
plt.xticks(xticks, labels = xlabels)
plt.title("Weekday demand profiles")
plt.xlabel("Time of measurement")
plt.ylabel("Energy usage (kWh)")
plt.show()

plt.plot(cum_demand)
yticks = [50, 100, 150, 200]
xticks = [0, 12, 24, 36, 48]
xlabels = ["12:00 am", "6:00 am", "12:00 pm", "6:00 pm", "12:00 am"]
plt.yticks(yticks)
plt.xticks(xticks, labels = xlabels)
plt.title("Weekday demand profiles - Aggregated")
plt.xlabel("Time of measurement")
plt.ylabel("Energy usage (kWh)")
plt.show()

with open("demand_profiles/demand_without_ev.txt", 'w') as f:
    f.write(str(cum_demand))

#also, modify the general demand in such a way so as to incoporate information from the EV at home data.
#each LYF-CYC might have different implications.
#add the EV charging profile to the damand profile.
