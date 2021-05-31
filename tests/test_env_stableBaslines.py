import stable_baselines3
from stable_baselines3.common.env_checker import check_env

#from gym_wrapper.abstractEnv import AbstractEnv
from gym_wrapper.jsbsimgymenvironmentwrapper import JsbsimGymEnvironmentWrapper


#env = AbstractEnv()
env = JsbsimGymEnvironmentWrapper()
check_env(env, warn=True)
