import gym
import numpy as np
from gym_wrapper.jsbsimgymenvironmentwrapper import JsbsimGymEnvironmentWrapper

configuration_path="../config/default_configuration.toml"

env = JsbsimGymEnvironmentWrapper(configuration_path=configuration_path)

throttle = 0
time_step_sec = 0
# while time_step <= in_seconds(minutes=2):
while time_step_sec <= 30:
    print("time_step_sec: ", time_step_sec)
    env.render() # comment render() for faster training
    state, rewards, dones, _ = env.step([np.array([throttle])],)
    time_step_sec = state[-1]
    print("state", state)