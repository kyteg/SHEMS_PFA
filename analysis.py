import pandas as pd
import matplotlib.pyplot as plt
import sys
from scipy.stats import gaussian_kde
#import numpy as np

###INIT###
helpmsg="""
q, quit                             - quits the program

help                                - displays the help screen

start/end time plots                - plots the start and end times of all trips in the dataset. (title etc needs to be added)

usage time likelihood               - plots the likelihood of a vehicle on the road at a given time.

vehicle leave return times          - plots times whereby vehicle leaves or returns home. Precise to the minute (bins may be more useful as ppl are more likely to report a clean leave/return time, eg 1pm rather than 1:02 pm)

vehicle leave return times in hours - plots times whereby vehicle leaves or returns home. To the hour.
"""
welcomemsg="""
 --------------------------
|TRAVEL DATA VISUALISATION |
 --------------------------

data from National Household Travel Survey.
code by Kyte Gurner
 """

print(welcomemsg)

print("importing data...")
data = pd.read_csv(r'../CSV/trippub.csv')
#make a df of evs?
# ev_data = pd.DataFrame()
# for i in range(len(data)):
#     if data.HFUEL[i] == 3:
#         ev_data = ev_data.append(data[i])
print("...done!\n")

###OPTIONS IN COMMAND LINE###
def help():
    print(helpmsg)

def plot_trip_start_end_times():
    #Plots the start and end times of all travel data
    data.STRTTIME.plot.hist(bins=100)
    data.ENDTIME.plot.hist(bins=100)
    plt.show()

def plot_vehicle_usage_time_likelihood(d):
    #Plots the likelihood of vehicle (any fuel type) being used at a given time.
    print("computing...")
    cumsum = []
    tot = 0
    for i in range (1439):
        cumsum.append(0)
    for i in range(len(d.STRTTIME)):
        if i%100000 == 0:
            print("{}%".format(int(100*i/len(d.STRTTIME))))
        start_time = d.STRTTIME[i]
        start_index = int((start_time - start_time%100)*0.6 + start_time%100)
        end_time = d.ENDTIME[i]
        end_index = int((end_time - end_time%100)*0.6 + end_time%100)
        for j in range(start_index, end_index):
            cumsum[j] += 1
            tot+=1

    for i in range(len(cumsum)):
        cumsum[i] = cumsum[i]/tot

    #plot
    times = []
    xticks = []
    for i in range(1439):
        time = ((i-i%60)/60)*100+i%60
        times.append(time)
    for i in range(12):
        xticks.append(i*200)
    plt.plot(times, cumsum)
    plt.ylabel('Density')
    plt.xlabel('time')
    plt.xticks(xticks)
    plt.title('Density of vehicle being used at a given time')
    print("Done!")

    plt.show()

def plot_house_leave_return_times(d, bins = False, ev = False):
    #plots the leave and return times from house of vehivles.
    cars_leaving_home = []
    cars_comming_home = []
    numof_cars_leaving_home = 0
    numof_cars_comming_home = 0

    if bins:
        for i in range(25):
            cars_leaving_home.append(0)
            cars_comming_home.append(0)
    else:
        for i in range(1440):
            cars_leaving_home.append(0)
            cars_comming_home.append(0)

    for i in range(len(d.WHYFROM)):
        if i%100000 == 0:
            print("{}%".format(int(100*i/len(d.WHYFROM))))
        if (d.WHYFROM[i] == 1 or d.WHYFROM[i] == 2):
            #leaving. Setting leave time.
            leave_time = d.STRTTIME[i]
            leave_index = int((leave_time - leave_time%100)*0.6 + leave_time%100)
            if bins:
                if leave_index%60 > 30:
                    #round up
                    leave_index = int((leave_index + 60 - leave_index%60)/60)
                else:
                    #round down
                    leave_index = int((leave_index - leave_index%60)/60)
            cars_leaving_home[leave_index] += 1
            numof_cars_leaving_home += 1
        if (d.WHYTO[i] == 1 or d.WHYTO[i] == 2):
            #returning.Setting return time.
            return_time = d.ENDTIME[i]
            return_index = int((return_time - return_time%100)*0.6 + return_time%100)
            if bins:
                if return_index%60 > 30:
                    #round up
                    return_index = int((return_index + 60 - return_index%60)/60)
                else:
                    #round down
                    return_index = int((return_index - return_index%60)/60)
            cars_comming_home[return_index] += 1
            numof_cars_comming_home += 1

    #plot
    times = []
    xticks = []
    if bins:
        for i in range(25):
            times.append(i)
        for i in range (12):
            xticks.append(i*2)
    else:
        for i in range(1440):
            time = ((i-i%60)/60)*100+i%60
            times.append(time)
        for i in range(12):
            xticks.append(i*200)
    for i in range(len(cars_leaving_home)):
        cars_leaving_home[i] = cars_leaving_home[i]/numof_cars_leaving_home
    for i in range(len(cars_comming_home)):
        cars_comming_home[i] = cars_comming_home[i]/numof_cars_comming_home
    plt.plot(times, cars_leaving_home)
    plt.plot(times, cars_comming_home)
    plt.ylabel('Density')
    plt.xlabel('time')
    plt.xticks(xticks)
    plt.title('Density of vehicle leaving or returning house at a given time')
    print("Done!")

    plt.show()

def plot_house_leave_return_times_kde(d):
    cars_leaving_home = []
    cars_comming_home = []

    for i in range(len(d.WHYFROM)):
        if i%100000 == 0:
            print("{}%".format(int(100*i/len(d.WHYFROM))))
        if (d.WHYFROM[i] == 1 or d.WHYFROM[i] == 2):
            #leaving. Setting leave time.
            leave_time = d.STRTTIME[i]
            cars_leaving_home.append(leave_time)
        if (d.WHYTO[i] == 1 or d.WHYTO[i] == 2):
            #returning.Setting return time.
            return_time = d.ENDTIME[i]
            cars_comming_home.append(return_time)

    #plot
    times = []
    xticks = []

    for i in range(1440):
        time = ((i-i%60)/60)*100+i%60
        times.append(time)
    for i in range(12):
        xticks.append(i*200)
    going_home_density = gaussian_kde(cars_leaving_home)
    comming_home_density = gaussian_kde(cars_comming_home)
    going_home_density.covariance_factor = lambda : .25
    going_home_density._compute_covariance()
    plt.ylabel('Density')
    plt.xlabel('time')
    plt.xticks(xticks)
    plt.title('Density of vehicle leaving or returning house at a given time')
    plt.plot(times, going_home_density(cars_leaving_home))
    print("Done!")

    plt.show()


###FUNCTION TO GET REQUESTS!###
def getrequest():
    r = input(">>").lower()
    if r == "q" or r == "quit":
        sys.exit()
    elif r == "help":
        help()
    elif r == "start/end time plots":
        plot_trip_start_end_times()
    elif r == "usage time likelihood":
        plot_vehicle_usage_time_likelihood(data)
    elif r == "ev usage time likelihood":
        plot_vehicle_usage_time_likelihood(evdata)
    elif r == "vehicle leave return times":
        plot_house_leave_return_times(data)
    elif r == "vehicle leave return times in hours":
        plot_house_leave_return_times(data, bins = True)
    elif r == "ev not in house":
        plot_house_leave_return_times(evdata, ev = True)
    elif r == "vehicle leave return times kde":
        plot_house_leave_return_times_kde(data)

    else:
        print("invalid command")


###MAIN###
while True:
    getrequest()
