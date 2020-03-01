import pandas as pd
import matplotlib.pyplot as plt
import sys
#import numpy as np

###INIT###
helpmsg="""
quit - q or quit
help - help
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
#sort with TRPHHVEH here!
#define evdata here!!
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

    times = []
    xticks = []
    for i in range(1439):
        time = ((i-i%60)/60)*100+i%60
        times.append(time)
    for i in range(12):
        xticks.append(i*200)
    plt.plot(times, cumsum)
    plt.ylabel('likelihood')
    plt.xlabel('time')
    plt.xticks(xticks)
    plt.title('Likelihood of vehicle being used at a given time')
    print("Done!")

    plt.show()

def plot_vehicle_not_in_house(d):
    #shows when the vehicle is not in the house.
    #use WHYTO/WHYFROM! whyto from house, whyto to house. filter data with these constraints.
    cars = []
    cars_going_home = []
    for i in range(len(d.WHYFROM)):
        if i%100000 == 0:
            print("{}%".format(int(100*i/len(d.WHYFROM))))
        if (d.WHYFROM[i] == 1 or d.WHYFROM[i] == 2):
            #leaving. Setting leave time.
            cars.append([d.VEHID[i], d.STRTTIME[i], 9999])

        #precompute relavant car entries to make computation more efficient.
        if d.WHYTO[i]==1 or d.WHYTO[i]==2:
            cars_going_home.append([d.VEHID[i], d.WHYTO[i], d.STRTTIME[i], d.ENDTIME[i]])
        if len(cars_going_home) >= 5000:  #for testing
            break

    print(len(cars_going_home))
    for i in range(len(cars)):
        vehid = cars[i][0]
        strttime = cars[i][1]
        if i%1000 == 0:
            print("{}%".format(int(100*i/len(cars))))
        for j in range(len(cars_going_home)):
            #returning. Setting return time.
            if cars_going_home[j][0] == vehid and cars_going_home[j][2] != strttime:
                cars[i][2] = cars_going_home[j][3]
    print(cars[1:100])
    #plot here!
###FUNCTION TO GET REQUESTS!###
def getrequest():
    r = input(">>").lower()
    if r == "q" or r == "quit":
        sys.exit()
    elif r == "help":
        help()
    elif r == "start to end time plot":
        plot_start_end_time()
    elif r == "usage time likelihood":
        plot_vehicle_usage_time_likelihood(data)
    elif r == "ev usage time likelihood":
        plot_vehicle_usage_time_likelihood(evdata)
    elif r == "vehicle not in house":
        plot_vehicle_not_in_house(data)
    elif r == "ev not in house":
        plot_vehicle_not_in_house(evdata)

    else:
        print("invalid command")


###MAIN###
while True:
    getrequest()
