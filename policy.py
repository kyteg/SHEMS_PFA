"""
defines the policy class
"""

class Policy(object):
    def __init__(self, charge_ev = False, charge_bat = False, flexi_load = False):
        self.charge_ev = charge_ev
        self.charge_bat = charge_bat
        self.flexi_load = flexi_load

    def manual_update(self, num):
        #[0[0,0,0], 1[0,0,1], 2[0,1,0], 3[0,1,1], 4[1,0,0], 5[1,0,1], 6[1,1,0], 7[1,1,1]]
        self.charge_ev, self.charge_bat, self.flexi_load = False, False, False
        if (num)%2:
            self.flexi_load = True
        if (num - (num)%2)%2:
            self.charge_bat = True
        if (num > 3):
            self.charge_ev = True

    def update(self, state):
        #This is where we use the trained neural net to update the policy given a new state
        return

    def selection(self):
        return (self.charge_ev, self.charge_bat, self.flexi_load)
