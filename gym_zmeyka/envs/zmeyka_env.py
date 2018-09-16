import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym_zmeyka.envs.zmeyka import Controller, Discrete

import matplotlib.pyplot as plt

class ZmeykaEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, **kwargs):
        self.controller_params = kwargs
        self.viewer = None
        self.action_space = Discrete(4)

    def step(self, action):
        self.last_obs, rewards, done, info = self.controller.step(action)
        return self.last_obs, rewards, done, info

    def reset(self):
        self.controller = Controller(self.controller_params)
        self.last_obs = self.controller.grid.grid
        return self.last_obs

    def render(self, mode='human', close=False):
        if self.viewer is None:
            self.viewer = plt.imshow(self.last_obs)
        plt.pause(0.1)
        plt.draw()
    
    def seed(self, x):
        pass