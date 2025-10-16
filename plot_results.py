import os
import numpy
import matplotlib.pyplot
from importlib.metadata import version

log_dir = "./logs/LunarLander-v3"
rl_type = "PPO"
env_str = "LunarLander-v3"


# Load evaluations.npz file
data = numpy.load(os.path.join(log_dir, "evaluations.npz")) # how well agent performed after each eval_freq timestep

# Extract relevant data
timesteps = data["timesteps"] # counts at which evaluations occurred
results = data["results"] # reward for each evaluation

# Calculate mean and std dev of results - ie. how much the rewards fluctuate
mean_results = numpy.mean(results, axis=1)
std_results = numpy.std(results, axis=1)

# Plot results
matplotlib.pyplot.figure()
matplotlib.pyplot.plot(timesteps, mean_results)
matplotlib.pyplot.fill_between(timesteps,
                               mean_results - std_results,
                               mean_results + std_results,
                               alpha=0.3)

matplotlib.pyplot.xlabel("Timesteps")
matplotlib.pyplot.ylabel("Mean Reward")
matplotlib.pyplot.title(f"{rl_type} Performance on {env_str}")
matplotlib.pyplot.legend()
matplotlib.pyplot.grid(True)
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.show()