import sys
import pandas as pd
from function_lib_ev_analysis import *

###INIT###
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

###FUNCTION TO GET REQUESTS!###
def getrequest():
    r = input(">>").lower()
    if r == "q" or r == "quit":
        sys.exit()
    elif r == "help" or r == "1":
        help()
    elif r == "start/end time plots" or r == "2":
        plot_trip_start_end_times()
    elif r == "usage time likelihood" or r == "3":
        plot_vehicle_usage_time_likelihood(data)
    elif r == "ev usage time likelihood" or r == "4":
        plot_vehicle_usage_time_likelihood(evdata)
    elif r == "vehicle leave return times" or r == "5":
        plot_house_leave_return_times(data)
    elif r == "vehicle leave return times in hours" or r == "6":
        plot_house_leave_return_times(data, bins = True)
    elif r == "ev not in house" or r == "7":
        plot_house_leave_return_times(evdata, ev = True)
    elif r == "vehicle leave return times kde" or r == "8":
        plot_house_leave_return_times_kde(data)
    elif r == "vehicle leave return times in hours catagories" or r == "9":
        plot_house_leave_return_times_catagories(data)
    else:
        print("invalid command")


###MAIN###
if __name__ == "__main__":
    while True:
        getrequest()
