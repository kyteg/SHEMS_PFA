"""
Defines the state class
"""

import random
from demand_generator import demand_generator
import math
from solar_generator import solar_generator


class State(object):
    def __init__(self, policy, ev_profile, time = 0.0,
    house_demand = 0, ev_at_home = True, ev_charge = 0, bat_charge = 0, flexi_charge = 0, ev_capacity = 75,
    battery_capacity = 30, variable_load_power_req = 10, solar_generation_capacity = 3,
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

        #This is what we want as close to 0 as possible!
        self.grid_pull = 0

        #constants
        self.EV_CAPACITY = ev_capacity
        self.BATTERY_CAPACITY = battery_capacity
        self.VARIABLE_LOAD_POWER_REQ = variable_load_power_req
        self.SOLAR_GENERATION_CAPACITY = solar_generation_capacity
        self.EV_PROFILE = ev_profile


        with open("demand_profiles/demand_without_ev.txt") as f:
            demand_profile = f.readline()
        demand_profile = demand_profile.split('[')[1].split(']')[0].split(', ')
        for i in range(len(demand_profile)):
            demand_profile[i] = float(demand_profile[i])

        with open("demand_profiles/variance.txt") as f:
            variance = f.readline()
        variance = variance.split('[')[1].split(']')[0].split(', ')
        sd = [0 for i in range(len(variance))]
        for i in range(len(variance)):
            sd[i] = math.sqrt(float(variance[i]))

        self.demand_profile = demand_profile
        self.sd = sd

    def update(self, policy):
        #stocastically update the state to the next state given the current state and input policy.
        #The state is updated every 30 simulated minutes.

        def update_ev_at_home():
            ev_home_prob = self.EV_PROFILE[int(self.time)]
            if random.randint(0, 10000) <= ev_home_prob*10000:
                self.ev_at_home = True
            else:
                self.ev_at_home = False

        def update_ev_charge():
            if self.ev_at_home:
                self.ev_charge += policy.charge_ev
                if self.ev_charge > self.EV_CAPACITY:
                    self.ev_charge = self.EV_CAPACITY
                if self.ev_charge < 0:
                    self.ev_charge = 0
            else:
                policy.charge_ev = 0

        def update_bat_charge():
            self.bat_charge += policy.charge_bat
            if self.bat_charge > self.BATTERY_CAPACITY:
                self.bat_charge = self.BATTERY_CAPACITY
            if self.bat_charge < 0:
                self.bat_charge = 0

        def update_flexi_charge():
            self.flexi_charge += policy.flexi_load
            if self.flexi_charge > self.VARIABLE_LOAD_POWER_REQ:
                self.flexi_charge = self.VARIABLE_LOAD_POWER_REQ

        def update_solar_generated():
            self.solar_generated = solar_generator(self.time)

        def update_house_demand():
            self.house_demand = round(demand_generator(self.time, self.demand_profile, self.sd), 2)

        def grid_pull():
            #this is what we want to minimise in the optimum policy function (ie the neural net)
            used = policy.charge_ev + policy.charge_bat + policy.flexi_load + self.house_demand
            self.grid_pull = used - self.solar_generated

        def update_time():
            if self.time == 23.5:
                self.time = 0.0
            else:
                self.time += 0.5

        update_ev_at_home()
        update_ev_charge()
        update_bat_charge()
        update_flexi_charge()
        update_solar_generated()
        update_house_demand()
        grid_pull()
        update_time()

    def update_policy(self, policy):
        self.policy = policy

    def reward(self):
        reward = 0

        #grid pull/sell
        if self.grid_pull > 0:
            reward -= self.grid_pull
        else:
            reward += 0.5*self.grid_pull

        reward += (self.ev_charge/self.EV_CAPACITY)
        reward += self.bat_charge/self.BATTERY_CAPACITY
        if self.time == 0 and self.flexi_charge != self.VARIABLE_LOAD_POWER_REQ:
            reward -= 10

        return reward if reward > 0 else 0



    def return_state(self):
        return (self.time, self.ev_at_home, self.ev_charge, self.bat_charge, self.flexi_charge)

    def print_state(self):
        print("""time = {}, ev_at_home = {}, ev_charge = {}, bat_charge = {}, flexi_charge = {},
        solar_generated = {}, house_demand = {}, grid_pull = {}""".format(self.time, self.ev_at_home, self.ev_charge,
        self.bat_charge, self.flexi_charge, self.solar_generated, self.house_demand, self.grid_pull))
