import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym_zmeyka.envs.zmeyka import Controller, Discrete

import matplotlib.pyplot as plt
from IPython import display

class ZmeykaEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, **kwargs):
        self.controller_params = kwargs
        self.action_space = Discrete(3)
        self.viewer = None
        self.rewards = 0

    def step(self, action):
        self.last_obs, self.rewards, done, self.info = self.controller.step(action)
        return self.last_obs, self.rewards, done, self.info

    def reset(self):
        self.controller = Controller(self.controller_params)
        self.last_obs = [self.controller.grid.pixels,[0,0,0,0,0]]
        return self.last_obs 

    def render(self, mode='human', close=False):
        plt.imshow(self.last_obs[0])
        plt.axis('off')
        display.clear_output(wait=True)
        #display.display(plt.gcf())
        plt.title('Zmeyka' + ", reward=%.3f"%self.rewards)
        plt.pause(0.01)
        return None
    
    def seed(self, x):
        pass