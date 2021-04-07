from services import pid
from core.simulation import Simulation

import numpy as np

pid_roll = pid.PID_angle('PID roll', p=2.9, i=0.01, d=1.9, time=0, angle_max=2 * np.math.pi, out_min=-1.0, out_max=1.0, anti_windup=1)
pid_pitch = pid.PID_angle('PID pitch', p=-2, i=-0.05, d=-0.9, time=0, angle_max=2 * np.math.pi, out_min=-1.0, out_max=1.0, anti_windup=1)

sim = Simulation()
result = sim.run()
print(sim.get_state())

empty_array = np.empty((0, 3), float)
while result and sim.jsbsim.get_sim_time() <= 30:
    state = sim.get_state()
    sim.run()
    #print(np.rad2deg(sim.jsbsim.get_property_value('attitude/roll-rad')))
    print(np.rad2deg(sim.jsbsim.get_property_value('attitude/pitch-rad')))
    sim.set_properties('fcs/aileron-cmd-norm', pid_roll(sim.jsbsim.get_property_value('attitude/roll-rad'), np.deg2rad(12)))
    sim.set_properties('fcs/elevator-cmd-norm', pid_pitch(sim.jsbsim.get_property_value('attitude/pitch-rad'), np.deg2rad(-4)))
    empty_array = np.append(empty_array, np.array([[np.rad2deg(sim.jsbsim.get_property_value('attitude/pitch-rad')), np.rad2deg(sim.jsbsim.get_property_value('attitude/roll-rad')), sim.jsbsim.get_sim_time()]]), axis=0)

import matplotlib.pyplot as plt

x = np.array(empty_array[:,2])
y = np.array(empty_array[:,1])
plt.plot(x, y)
plt.show()
