"""
Defines the state class
"""

import random

class state(object):
    def __init__(self, policy, ev_leave_probabilities, ev_return_probabilities, time = 0.0,
    house_power_draw = 0, ev_at_home = True, ev_capacity = 50, battery_capacity = 8,
    variable_load_power_req = ?, solar_generation_capacity = 8, solar_power_generated = 0):

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
        self.house_power_draw = house_power_draw

        #constants
        self.EV_CAPACITY = ev_capacity
        self.BATTERY_CAPACITY = battery_capacity
        self.VARIABLE_LOAD_POWER_REQ = variable_load_power_req
        self.SOLAR_GENERATION_CAPACITY = solar_generation_capacity
        self.EV_LEAVE_PROBABILITIES = ev_leave_probabilities
        self.EV_RETURN_PROBABILITIES = ev_return_probabilities

    def update(self, policy):
        #stocastically update the state to the next state given the current state and input policy.
        #The state is updated every 30 simulated minutes.

        def update_time():
            if self.time == 23.5:
                self.time = 0.0
            else:
                self.time += 0.5

        def update_ev_at_home():
            if self.ev_at_home:
                ev_leave_prob = self.EV_LEAVE_PROBABILITIES[self.time * 2]
                if random.randint(10000) <= ev_leave_prob*10000:
                    #ev is at home
                    ev_at_home = True
                else:
                    ev_at_home = False
            else:
                ev_return_prob = self.EV_RETURN_PROBABILITIES[self.time*2]
                if random.randint(10000) <= ev_return_prob*10000:
                    #ev returned home
                    ev_at_home = True
                else:
                    ev_at_home = False

        def update_

    def grid_pull(self):
        #this is what we want to minimise in the optimum policy function (ie the neural net)
        used = self.charge_ev + self.charge_battery + self.flexi_load + self.house_power_draw
        pull = used - self.solar_generated
        return pull
