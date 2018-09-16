from gym.envs.registration import register

register(
    id='zmeyka-v0',
    entry_point='gym_zmeyka.envs:ZmeykaEnv',
)
register(
    id='zmeyka-extrahard-v0',
    entry_point='gym_zmeyka.envs:ZmeykaExtraHardEnv',
)