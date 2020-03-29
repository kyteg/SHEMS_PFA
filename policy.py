"""
defines the policy class
"""

class policy(object):
    def __init__(charge_ev = 0, charge_bat = 0, flexi_load = 0):
        self.charge_ev = charge_ev
        self.charge_bat = charge_bat
        self.flexi_load = flexi_load

    def update(self, state):
        #This is where we use the trained neural net to update the policy given a new state
        return
