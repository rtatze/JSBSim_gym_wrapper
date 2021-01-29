import gym
import numpy as np
from gym_wrapper.jsbsimgymenvironmentwrapper import JsbsimGymEnvironmentWrapper

configuration_path="../config/default_configuration.toml"

env = JsbsimGymEnvironmentWrapper(configuration_file=configuration_path)

throttle = 0
time_step_sec = 0
while time_step_sec <= 30:
    print("time_step_sec: ", time_step_sec)
    #env.render() # comment render() for faster training
    action = env.action_space.sample()
    state, rewards, dones, _ = env.step([np.array([action])],)
    time_step_sec = env.sim.get_properties('simulation/sim-time-sec')
    print("state", state)