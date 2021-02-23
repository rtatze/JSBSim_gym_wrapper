from datetime import datetime
import numpy as np
from gym_wrapper.jsbsimgymenvironmentwrapper import JsbsimGymEnvironmentWrapper

configuration_path = "../config/default_configuration.toml"

env = JsbsimGymEnvironmentWrapper(configuration_file=configuration_path)



def simCycle(name, outer, inner):
    print ('Simulation {}: {}x{} steps'.format(name, outer, inner),end='\r')
    before = datetime.now()
    for _ in range(outer):
        env.reset()
        for _ in range(inner):
            #action=env.action_space.sample()
            action = np.array([0.0])
            env.step(action)
    after = datetime.now()
    dt = (after-before)
    print ('Simulation {}: {}x{} steps: {}.{}s'.format(name, outer, inner, dt.seconds, dt.microseconds) )

name = 'JSBSIM'

simCycle(name, 1, 10000)
simCycle(name, 10, 1000)
simCycle(name, 100, 100)
simCycle(name, 1000, 10)
print(env.get)
env.close()
