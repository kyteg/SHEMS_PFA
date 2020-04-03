"""
Defines the state class
"""

import random

class State(object):
    def __init__(self, policy, ev_profile, time = 0.0,
    house_demand = 2, ev_at_home = True, ev_charge = 0, bat_charge = 0, flexi_charge = 0, ev_capacity = 75,
    battery_capacity = 30, variable_load_power_req = 10, solar_generation_capacity = 6,
    solar_generated = 0):

        #units are in kWh (except solar_generation_capacity, in kW)

        #time is from 0-23.5 in intervals of 0.5 (correcponding to 30 miniutes)
        #(this will be useful in update(), where we must look at the time of day to update info like vahicle_at_home)
        self.time = time

        #this is the policy to be applied in the next time interval.
        self.policy = policy

        #these are the state variables that are inputs into the policy function
        self.ev_at_home = ev_at_home
        self.ev_charge = ev_charge
        self.bat_charge = bat_charge
        self.flexi_charge = flexi_charge

        #variables that are quasi-randomly generated (with time taken into account).
        self.solar_generated = solar_generated
        self.house_demand = house_demand

        #constants
        self.EV_CAPACITY = ev_capacity
        self.BATTERY_CAPACITY = battery_capacity
        self.VARIABLE_LOAD_POWER_REQ = variable_load_power_req
        self.SOLAR_GENERATION_CAPACITY = solar_generation_capacity
        self.EV_PROFILE = ev_profile

    def update(self, policy):
        #stocastically update the state to the next state given the current state and input policy.
        #The state is updated every 30 simulated minutes.

        def update_time():
            if self.time == 23.5:
                self.time = 0.0
            else:
                self.time += 0.5

        def update_ev_at_home():
            ev_home_prob = self.EV_PROFILE[int(self.time * 2)]
            if random.randint(0, 10000) <= ev_home_prob*10000:
                self.ev_at_home = True
            else:
                self.ev_at_home = False

        def update_ev_charge():
            self.ev_charge += policy.charge_ev

        def update_bat_charge():
            self.bat_charge += policy.charge_bat

        def update_flexi_charge():
            self.flexi_charge += policy.flexi_load

        def update_solar_generated():
            #need to change this with ev profiles.
            if self.time > 7 and self.time < 18:
                self.solar_generated = self.SOLAR_GENERATION_CAPACITY/2
            else:
                self.solar_generated = 0

        def update_house_demand():
            #need to change this with demand profiles.
            self.house_demand = 2

        update_time()
        update_ev_at_home()
        update_ev_charge()
        update_bat_charge()
        update_flexi_charge()
        update_solar_generated()
        update_house_demand()

    def grid_pull(self):
        #this is what we want to minimise in the optimum policy function (ie the neural net)
        used = self.charge_ev + self.charge_battery + self.flexi_load + self.house_demand
        pull = used - self.solar_generated
        return pull

    def policy(self, policy):
        self.policy = policy

    def print_state(self):
        print("""time = {}, ev_at_home = {}, ev_charge = {}, bat_charge = {}, flexi_charge = {},
        solar_generated = {}, house_demand = {}""".format(self.time, self.ev_at_home, self.ev_charge,
        self.bat_charge, self.flexi_charge, self.solar_generated, self.house_demand))
