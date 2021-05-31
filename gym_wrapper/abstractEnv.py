from typing import Tuple, List
import numpy as np
from enum import Enum
import gym
from gym import spaces
import logging
from abc import ABC, abstractmethod


class AbstractEnv(gym.Env, ABC):

    def __init__(self):
        super(AbstractEnv, self).__init__()
        self.max_speed = 8
        self.max_torque = 2.
        self.dt = .05
        self.m = 1.
        self.l = 1.
        self.viewer = None

        high = np.array([1., 1., self.max_speed], dtype=np.float32)
        self.action_space = spaces.Box(
            low=-self.max_torque,
            high=self.max_torque, shape=(1,),
            dtype=np.float32
        )
        self.observation_space = spaces.Box(
            low=-high,
            high=high,
            dtype=np.float32
        )
        print(self.observation_space.shape)
        print(self._get_obs().shape)

    def step(self, action) -> Tuple[object, float, bool, dict]:  # ->observation, reward, done, info
        return self._get_obs(), self._calcRewards(), False, {}

    def reset(self) -> object:
        return self._get_obs()

    def _get_obs(self) -> np.ndarray:
        return np.array([1.0, 1.0, 1.0])

    def _calcRewards(self) -> float:
        rewAgent0 = 0
        return rewAgent0

    def render(self, mode='human'):
        pass

    def close(self):
        pass
