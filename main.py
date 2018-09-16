import gym
import gym_zmeyka

env = gym.make('zmeyka-v0')
env.reset()
for _ in range(1000):
    env.render()
    last_obs, rewards, done, info = env.step(env.action_space.sample())
    if done: break