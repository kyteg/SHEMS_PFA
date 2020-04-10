import datetime
import math

with open("demand_profiles/demand_without_ev.txt") as f:
    demand_profile = f.readline()
demand_profile = demand_profile.split('[')[1].split(']')[0].split(', ')
for i in range(len(demand_profile)):
    demand_profile[i] = float(demand_profile[i])


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

variance = [0 for i in range(48)]
variance_count = [0 for i in range(48)]
count = 0
for point in data: #calculate the variance

    print_progress(count, len(data))

    point = point.split(',')
    date_time = point[3].split()
    date = date_time[0]
    time_d = date_time[1].split(':')
    if is_weekday(date):
        time_index = int(2*(float(time_d[0]) + (1/60)*float(time_d[1])))
        variance[time_index] += (demand_profile[time_index] - float(point[4])/2)**2
        variance_count[time_index] += 1
    count+=1

for i in range(len(variance)):
    variance[i] = math.sqrt(variance[i]/variance_count[i])
print(variance)
with open("demand_profiles/variance.txt", 'w') as f:
    f.write(str(variance))
