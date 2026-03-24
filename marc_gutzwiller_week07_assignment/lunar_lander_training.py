import gymnasium as gym
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.monitor import Monitor


def make_env():
    env = gym.make("LunarLander-v3")
    env = make_vec_env("LunarLander-v3", n_envs=8)
    #env = Monitor(env)
    return env

env = make_env()

model = PPO(
    policy="MlpPolicy", 
    env=env,
    device="cpu",
    n_steps=2048,
    batch_size=64,
    gae_lambda=0.95,
    gamma=0.99,
    n_epochs=10,
    learning_rate=0.0003, 
    verbose=1
    )


model.learn(total_timesteps=500_000)

model_name = "ppo_lunar_lander"
model.save(model_name)
