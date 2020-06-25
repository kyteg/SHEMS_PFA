# SHEMS_PFA

This code is a part of the "Policy Function Approximation on Household Solar Power
Management using  Neural  Networks  -  a  Preliminary  Investigation" paper
by Kyte Gurner.

##analisys.py (core)
Interactive command line based app to compute different statistics on the
National Household Travel Survey in real time. Options 5, 6 or 7 must be run
here for EV_probabilities_to_profile.py to work.

REQUIRES:
- ../CSV/trippub.csv

WRITES:
- ../leave_return_times_data

#function_lib_ev_analisis.py (helper)
Contains function for EV_probabilities_to_profile.py.


##EV_probabilities_to_profile.py (core)
Converts the leave and return time probabilities produced by analisis.py into an
EV at home probability profile by conducting a Monte Carlo simulation. The file
then writes the result for each LIFCYC into the ev_profiles directory. (For
information on LIFCYC, consult the documentation for the NHTS dataset
- https://nhts.ornl.gov).

REQUIRES:
- ../leave_return_times_data

WRITES:
- ev_profiles

#plot_ev_profiles.py (helper)
Plots the ev profiles.


##get_demand_profile.py (core)
Makes demand profiles from the Smart City Smart Grid dataset. Only takes Weekday
demand data.

REQUIRES:
- ../trial_cust_half_hour

WRITES:
- demand_profiles/demand_without_ev.txt

##get_demand_variance.py (core)
Calculates the variance in the demand from the SCSG dataset.

REQUIRES:
- demand_profiles
- ../trial_cust_half_hour/CD_INTERVAL_READING.dat

Writes:
- demand_profiles/variance.txt

##update_policy.py (core)
Builds and trains the nerual network to be used as the policy function approximator.

REQUIRES:
- ev_profiles
- demand_profiles

WRITES:
- (model name).txt
- The trained neural network model.

#get_loss_func.py (helper)
The get_target function in this file is the DP Algorithm to calculate the
optimal policy give a state.

#get_loss_func_dilute.py (helper)
Similar to the above 'get_loss_func', but returns a vector with floats corresponding
to the firt, second, third etc best choices to make.

#plot_model_loss (helper)
Plots the loss as a function of training iteration for the neural network.

REQUIRES:
- (model name).txt

#Policy.py (helper)
Defines the policy class.

Important variables:
- self.charge_ev    True/False whether as to if ev is being charged. (bool)
- self.charge_bat   True/False whether as to if battery is being charged. (bool)
- self.flexi_load   True/False whether as to if flexi-load is being charged. (bool)

Important methods:
- manual_update(self, num) - Updates the policy given a policy code (0-7).

#State.py (helper)
Defines the state class.

Important variables:
- self.time                     - Simulated time.
- self.policy                   - policy of current state.
- self.ev_at_home               - True/False whether as to if ev is at home.
- self.ev_charge                - Amount of charge in the ev.
- self.bat_charge               - Amount of charge in the battery.
- self.flexi_charge             - Amount of charge in the flexi_charge.
- self.solar_generated          - Amount of solar energy generated.
- self.house_demand             - The electricity demand of the household.
- self.grid_pull                - The amount of electricity pulled from the grid.
- self.EV_CAPACITY              - The EV's maximum capacity
- self.BATTERY_CAPACITY         - Battery's maximum capacity.
- self.VARIABLE_LOAD_POWER_REQ  - Amount of electricity needed to charge the flexi-load fully.
- self.SOLAR_GENERATION_CAPACITY - The maximum power attainable from solar panels.
- self.EV_PROFILE               - The EV profile probabilities in a list
- self.demand_profile           - Electricity demand profile
- self.sd                       - Electricity demand sd.

Important methods:
- update(self, policy)        - Updates the state given a policy.
- update_policy(self, policy) - modifies self.policy to policy.
- reward(self)                - Computes the reward of being in he current state.


#solar_generator.py (helper)
- Contains solar_generator(time) that returns a estimate of the solar generation
given the time.


#demand_generator.py (helper)
The demand generator generates a random demand profile taking into account the average demand profile
and the variace of the demand at each point in time.
This is modified because sd is too large. The sd for all points is set to be 0.03.

If this file is run, it will produce plots of random demand that the algorithm generates.

REQUIRES:
- demand_profiles (if running it standalone.)
