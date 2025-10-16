import gymnasium
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
# vectorized environments - runs parallel to other identical copies 
# speeding up data collection, reduces variance training algorithm faster, 
# and improves performance
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.vec_env import VecFrameStack, VecTransposeImage
from stable_baselines3.common.vec_env import VecVideoRecorder

import os
import torch
import numpy
import scipy
import platform
import IPython
import matplotlib
import matplotlib.pyplot
from importlib.metadata import version


rl_type = "PPO" # RL algorithm being implemented
env_str = "LunarLander-v3" # gymnasium environment ID for LunarLander
log_dir = f"./logs/{env_str}" # folder path to save logs and models
name_prefix = "lunar_lander" # prefix for saved model files or logs

env = gymnasium.make(env_str) # creates specified environment
print("Observation Space Size: ", env.observation_space.shape) # shape of obs agent will receive
print("Actions Space: ", env.action_space) # discrete or cts actions available
env.close() # closes environment to free up resources


# Create training environment
env = make_vec_env(env_str, n_envs=1) # single LunarLander-v3

# Create elevation environment
env_val = make_vec_env(env_str, n_envs=1) # environment being evaluated (separate to avoid bias)

# Periodically evaluate and save best model
eval_callback = EvalCallback(env_val,
                             best_model_save_path=log_dir,
                             eval_freq=25_000, # evaluate every 25k timesteps
                             render=False, # don't create window during eval
                             deterministic=True, # highest-prob (no randomness)
                             n_eval_episodes=20) # num episodes tested per evaluation

# Initialize PPO
# entropy coefficient adds some randomness in actions
model = PPO("MlpPolicy", env, verbose=0, ent_coef=0.005)

# Train the model
model.learn(total_timesteps=500_000,
            progress_bar=True,
            callback=eval_callback) # runs evaluation during training

# Save model
# can reload without retraining
model.save(os.path.join(log_dir, "final_model"))

mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=20)
print(f"Mean reward: {mean_reward:.2f} +/- {std_reward:.2f}")

env.close()
env_val.close()