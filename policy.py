"""
defines the policy class
"""

class Policy(object):
    def __init__(self, charge_ev = 1, charge_bat = 1, flexi_load = 1):
        self.charge_ev = charge_ev
        self.charge_bat = charge_bat
        self.flexi_load = flexi_load

    def update(self, state):
        #This is where we use the trained neural net to update the policy given a new state
        return
