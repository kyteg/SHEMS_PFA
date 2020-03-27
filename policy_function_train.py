"""
Trains policy function neural network using reinforement learning.

todo:
create a state vector that changes as a function of time in a realistic manner.
train a neural network using tensorflow using reinforcement leanrning.
test the neural network.
"""

cost = sell_to_grid + pull_from_grid + (1-ev_charge_ratio) + (1-bat_charge_ratio) + ev_not_home*ev_charging*10000000 + time==0*flexi_not_full*10000
minimize(cost)
