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
        #update the state to the next state given the current state and input policy.
        #The state is updated every 30 simulated minutes.

        def update_ev_at_home():
            ev_home_prob = self.EV_PROFILE[int(self.time)]
            if random.randint(0, 10000) <= ev_home_prob*10000:
                self.ev_at_home = True
            else:
                self.ev_at_home = False

        def update_ev_charge():
            ev_use = 0
            if self.ev_at_home:
                ev_use = -5
                if policy.charge_ev:
                    self.ev_charge += 5
                    if self.ev_charge > self.EV_CAPACITY:
                        ev_use -= self.EV_CAPACITY - self.ev_charge
                        self.ev_charge = self.EV_CAPACITY
                else:
                    ev_use = 5
                    self.ev_charge -= 5
                    if self.ev_charge < 0:
                        ev_use = self.ev_charge + 5
                        self.ev_charge = 0
            else:
                self.ev_charge -= 5
                if self.ev_charge < 0:
                    self.ev_charge = 0
            return ev_use

        def update_bat_charge():
            bat_use = 0
            if policy.charge_bat:
                bat_use = -5
                self.bat_charge += 5
                if self.bat_charge > self.BATTERY_CAPACITY:
                    bat_use = self.bat_charge-self.BATTERY_CAPACITY
                    self.bat_charge = self.BATTERY_CAPACITY
            else:
                bat_use = 5
                self.bat_charge -= 5
                if self.bat_charge < 0:
                    bat_use = self.bat_charge - 5
                    self.bat_charge = 0
            return bat_use

        def update_flexi_charge():
            flexi_use = 0
            if policy.flexi_load:
                flexi_use = -5
                self.flexi_charge += 5
                if self.flexi_charge > self.VARIABLE_LOAD_POWER_REQ:
                    flexi_use = self.flexi_charge - self.VARIABLE_LOAD_POWER_REQ
                    self.flexi_charge = self.VARIABLE_LOAD_POWER_REQ
            if self.time == 0:
                self.flexi_charge = 0
            return flexi_use

        def update_solar_generated():
            self.solar_generated = 5*solar_generator(self.time)

        def update_house_demand():
            self.house_demand = round(demand_generator(self.time, self.demand_profile, self.sd), 2)

        def grid_pull(ev_use, bat_use, flexi_use):
            #this is what we want to minimise in the optimum policy function (ie the neural net)
            used = self.house_demand - (ev_use + bat_use + flexi_use)
            self.grid_pull = used - self.solar_generated

        def update_time():
            if self.time == 23.5:
                self.time = 0.0
            else:
                self.time += 0.5

        update_ev_at_home()
        ev_use = update_ev_charge()
        bat_use = update_bat_charge()
        flexi_use = update_flexi_charge()
        update_solar_generated()
        update_house_demand()
        grid_pull(ev_use, bat_use, flexi_use)
        update_time()

    def update_policy(self, policy):
        self.policy = policy

    def reward(self):
        reward = 1

        #grid pull/sell
        if self.grid_pull > 0:
            reward -= self.grid_pull
        else:
            reward += self.grid_pull

        reward += (0.25)*self.ev_charge + (0.18)*self.bat_charge + (0.4)*self.flexi_charge

        return reward



    def return_state(self):
        return (self.time, self.ev_at_home, self.ev_charge, self.bat_charge, self.flexi_charge)

    def print_state(self):
        print("""time = {}, ev_at_home = {}, ev_charge = {}, bat_charge = {}, flexi_charge = {},
        solar_generated = {}, house_demand = {}, grid_pull = {}""".format(self.time, self.ev_at_home, self.ev_charge,
        self.bat_charge, self.flexi_charge, self.solar_generated, self.house_demand, self.grid_pull))
