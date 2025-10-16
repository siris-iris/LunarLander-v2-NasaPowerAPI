import os # helps with file paths
import gymnasium
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecVideoRecorder
from stable_baselines3.common.evaluation import evaluate_policy
# gives back avg reward and standard dev. of model

env_str = "LunarLander-v3"
log_dir = f"./logs/{env_str}"
name_prefix = "lunar_lander"


# Create elevation environment
env = make_vec_env(env_str, n_envs=1, seed=0) # single eval environment

# Load best model
best_model_path = os.path.join(log_dir, "best_model.zip")
best_model = PPO.load(best_model_path, env=env) # saved from training

# Set up recording best model playing Lunar Lander
best_model_file_name = "best_model+{}".format(name_prefix) # evaluate_policy of 20 eps
env = VecVideoRecorder(env,
                       log_dir,
                       video_length=5000, # timesteps
                       record_video_trigger=lambda x: x==0, # only record first ep
                       name_prefix=best_model_file_name)
# saves to logs/LunarLander-v3/

# To actually record
obs = env.reset()
for _ in range(5000): # _ does same thing as i - throwaway variable!
    action, _states = best_model.predict(obs) # predicts action using trained model
    obs, rewards, dones, info = env.step(action) # applies action and receives new traits
    env.render()
    if dones:
        break

env.close()