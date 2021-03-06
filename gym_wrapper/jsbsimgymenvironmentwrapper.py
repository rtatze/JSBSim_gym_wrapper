import gym
from typing import List, Tuple, Dict
import numpy as np
from gym import spaces
from core.simulation import Simulation
import os
import toml

import config

class JsbsimGymEnvironmentWrapper(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}
    def __init__(self, configuration_file: str=config.DEFAULT_CONFIGURATION_FILE):
        super(JsbsimGymEnvironmentWrapper, self).__init__()
        self.configuration = toml.load(os.path.expanduser(configuration_file))
        self.sim = Simulation(configuration_file=configuration_file)
        self._dimensions = 1
        self.action_space = spaces.Box(
            low=-0,
            high=1,
            shape=(self._dimensions,),
            dtype=np.float32
        )
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(self._getObs().shape[0],),
            dtype=np.float32
        )
        self.sim_steps = self.configuration['simulation']['agent_interaction_freq']

    def reset(self) -> object:
        self.sim.reset_with_initial_condition()
        observation = self._getObs()
        return observation

    def step(self, actions: List[np.ndarray]) -> Tuple[object, float, bool, dict]:
        for _ in range(self.sim_steps):
            self.sim.set_properties('fcs/elevator-cmd-norm', actions[0])
            self.sim.run()
        observation = self._getObs()
        reward = self._calcRewards(observation)
        return observation, reward, self._calcDones(), {}

    def _getObs(self) -> np.ndarray:
        state = list(self.sim.get_state().values())
        return np.array(state)

    def _calcRewards(self, observation) -> float:
        rewAgent0 = 0
        return rewAgent0

    def _calcDones(self) -> bool:
        dones = False
        return dones

    def render(self, mode='human'):
        pass

    def close(self):
        pass

    def seed(self, seed=None) -> None:
        pass

if __name__ == "__main__":
    env = JsbsimGymEnvironmentWrapper()
    ob = env.reset()
    action = env.action_space.sample()
    for _ in range(10):
        print(env.step(action))

