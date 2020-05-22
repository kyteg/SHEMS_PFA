import policy
import state
import random

depth_to_check = 4

def get_target(s_real, discount, max_reward = [999999, 0], depth = 0):
    """returns the optimal target given a state"""
    if depth == depth_to_check:
        return 1, s_real.reward()

    p = policy.Policy()
    rank = []

    for i in range(8):
        s = state.State(p, ev_profile = s_real.EV_PROFILE, time = s_real.time,
        house_demand = s_real.house_demand, ev_at_home = s_real.ev_at_home, ev_charge = s_real.ev_charge,
        bat_charge = s_real.bat_charge, flexi_charge = s_real.flexi_charge, ev_capacity = s_real.EV_CAPACITY,
        battery_capacity = s_real.BATTERY_CAPACITY, variable_load_power_req = s_real.VARIABLE_LOAD_POWER_REQ,
        solar_generation_capacity = s_real.SOLAR_GENERATION_CAPACITY, solar_generated = s_real.solar_generated)
        p.manual_update(i)
        s.update(p)
        reward = s.reward() + get_target(s, discount, max_reward, depth+1)[1] * discount
        rank.append(reward)
        if reward < max_reward[0]:
            max_reward = [reward, i]

    result = [0 for i in range(8)]
    rank_sorted = sorted(rank)
    for i in range(len(result)):
        result[i] = 0.5**(rank_sorted.index(rank[i])+1)
    return result, max_reward[0]

if __name__ == "__main__":
    with open("ev_profiles/LIF_CYC1.txt") as f:
        evprofile = f.readline()
    evprofile = evprofile.split('[')[1].split(']')[0].split(', ')
    for i in range(len(evprofile)):
        evprofile[i] = float(evprofile[i])

    p = policy.Policy()
    s = state.State(p, evprofile)

    get_target(s, 0.9)
