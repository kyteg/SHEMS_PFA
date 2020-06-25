import pandas as pd
import matplotlib.pyplot as plt
import sys
from scipy.stats import gaussian_kde
#import numpy as np

###OPTIONS IN COMMAND LINE###
def help():

    helpmsg="""
    q, quit                             - quits the program

    help                                - displays the help screen

    start/end time plots                - plots the start and end times of all trips in the dataset. (title etc needs to be added)

    usage time likelihood               - plots the likelihood of a vehicle on the road at a given time.

    vehicle leave return times          - plots times whereby vehicle leaves or returns home. Precise to the minute (bins may be more useful as ppl are more likely to report a clean leave/return time, eg 1pm rather than 1:02 pm)

    vehicle leave return times in hours - plots times whereby vehicle leaves or returns home. To the hour.
    """
    print(helpmsg)

def plot_trip_start_end_times():
    """Plots the start and end times of all travel data"""
    data.STRTTIME.plot.hist(bins=100)
    data.ENDTIME.plot.hist(bins=100)
    plt.show()

def plot_vehicle_usage_time_likelihood(d):
    """Plots the likelihood of vehicle (any fuel type) being used at a given time."""
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

def plot_house_leave_return_times(d, bins = False, ev = False, subtitle = ''):
    """plots the leave and return times from house of vehivles."""
    cars_leaving_home = []
    cars_coming_home = []
    numof_cars_leaving_home = 0
    numof_cars_coming_home = 0

    if bins:
        for i in range(25):
            cars_leaving_home.append(0)
            cars_coming_home.append(0)
    else:
        for i in range(1440):
            cars_leaving_home.append(0)
            cars_coming_home.append(0)

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
            cars_coming_home[return_index] += 1
            numof_cars_coming_home += 1

    #plot
    times = []
    if bins:
        for i in range(25):
            times.append(i)
    else:
        for i in range(1440):
            time = ((i-i%60)/60)*100+i%60
            times.append(time)
    for i in range(len(cars_leaving_home)):
        cars_leaving_home[i] = cars_leaving_home[i]/numof_cars_leaving_home
    for i in range(len(cars_coming_home)):
        cars_coming_home[i] = cars_coming_home[i]/numof_cars_coming_home
    xticks = [0, 6, 12, 18, 24]
    xlabels = ["12:00 am", "6:00 am", "12:00 pm", "6:00 pm", "12:00 am"]
    plt.plot(times, cars_leaving_home)
    plt.plot(times, cars_coming_home)
    plt.ylabel('Density')
    plt.xlabel('Time of day')
    plt.xticks(xticks, labels = xlabels)
    plt.suptitle('EV leaving/returning')
    plt.title(subtitle, fontsize = 10)
    print("Done!")

    plt.show()

    #export
    if subtitle != '':
        file_location = '../leave_return_times_data/'+subtitle.strip()+'_leaving.txt'
        with open(file_location, 'w') as f:
            f.write(str(cars_leaving_home))
        file_location = '../leave_return_times_data/'+subtitle.strip()+'_coming.txt'
        with open(file_location,'w') as f:
            f.write(str(cars_coming_home))

def plot_house_leave_return_times_kde(d):
    """ function does the same thing as plot_house_leave_return_times(). Just experimenting with gaussian_kde() to be able to tweak parameters when doing kde."""
    cars_leaving_home = []
    cars_coming_home = []

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
            cars_coming_home.append(return_time)

    #plot
    times = []
    xticks = []

    for i in range(1440):
        time = ((i-i%60)/60)*100+i%60
        times.append(time)
    for i in range(12):
        xticks.append(i*200)
    going_home_density = gaussian_kde(cars_leaving_home)
    comming_home_density = gaussian_kde(cars_coming_home)
    going_home_density.covariance_factor = lambda : .25
    going_home_density._compute_covariance()
    plt.ylabel('Density')
    plt.xlabel('time')
    plt.xticks(xticks)
    plt.title('Density of vehicle leaving or returning house at a given time')
    plt.plot(times, going_home_density(cars_leaving_home))
    print("Done!")

    plt.show()

def plot_house_leave_return_times_catagories(d):

    #separate d into catagories!
    catagories = [pd.DataFrame(columns = ['LIF_CYC', 'WHYFROM', 'WHYTO', 'STRTTIME', 'ENDTIME']) for i in range(11)]   #ignore list index 0 to avoid confusion.
    counters = [0 for i in range(11)]
    for i in range(int(len(d))):
        if i%1000 == 0:
            print("progress = {}%".format(100*i/(len(d))))
        new_entry = [d.LIF_CYC[i], d.WHYFROM[i], d.WHYTO[i], d.STRTTIME[i], d.ENDTIME[i]]
        if d.LIF_CYC[i] == 1:
            catagories[1].loc[counters[1]] = new_entry
            counters[1]+=1
        elif d.LIF_CYC[i] == 2:
            catagories[2].loc[counters[2]] = new_entry
            counters[2]+=1
        elif d.LIF_CYC[i] == 3:
            catagories[3].loc[counters[3]] = new_entry
            counters[3]+=1
        elif d.LIF_CYC[i] == 4:
            catagories[4].loc[counters[4]] = new_entry
            counters[4]+=1
        elif d.LIF_CYC[i] == 5:
            catagories[5].loc[counters[5]] = new_entry
            counters[5]+=1
        elif d.LIF_CYC[i] == 6:
            catagories[6].loc[counters[6]] = new_entry
            counters[6]+=1
        elif d.LIF_CYC[i] == 7:
            catagories[7].loc[counters[7]] = new_entry
            counters[7]+=1
        elif d.LIF_CYC[i] == 8:
            catagories[8].loc[counters[8]] = new_entry
            counters[8]+=1
        elif d.LIF_CYC[i] == 9:
            catagories[9].loc[counters[9]] = new_entry
            counters[9]+=1
        elif d.LIF_CYC[i] == 10:
            catagories[10].loc[counters[10]] = new_entry
            counters[10]+=1
        else:
            pass

    #run the plotting function with bins set to true.
    for catagory in catagories:
        if not catagory.empty:
            subtitle = 'LIF_CYC = '+str(catagory.LIF_CYC[0])
            plot_house_leave_return_times(catagory, bins=True, subtitle = subtitle)
