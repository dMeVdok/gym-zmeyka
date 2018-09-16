import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym_zmeyka.envs.zmeyka import Controller, Discrete

import matplotlib.pyplot as plt

class ZmeykaEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, **kwargs):
        self.controller_params = kwargs
        self.action_space = Discrete(3)
        self.viewer = None
        self.model = {}
        self.rewards = 0

    def step(self, action):
        self.last_obs, self.rewards, done, info = self.controller.step(action)
        return self.last_obs, self.rewards, done, info

    def reset(self):
        self.controller = Controller(self.controller_params)
        self.last_obs = self.controller.grid.pixels
        return self.last_obs 

    def render(self, mode='human', close=False):
        if self.viewer is None:
            self.viewer = plt.imshow(self.last_obs)
            fig = plt.gcf()
            fig.canvas.set_window_title('Zmeyka')
            self.viewer.axes.get_xaxis().set_visible(False)
            self.viewer.axes.get_yaxis().set_visible(False)
        else:
            self.viewer.set_data(self.last_obs)
        plt.title('Zmeyka' + ", reward=%.3f"%self.rewards)
        plt.pause(0.05)
        plt.draw()
    
    def seed(self, x):
        pass