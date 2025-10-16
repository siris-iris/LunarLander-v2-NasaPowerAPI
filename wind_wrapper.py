import gymnasium as gym
from gymnasium.envs.box2d import LunarLander
from wind_power import get_hourly_data

class WindWrapper(gym.Wrapper):
    def __init__(self, env, wind_speed):
        super().__init__(env) # to initialize wrapper with environment
        if wind_speed is None:
            print("No valid wind data found, defaulting to 0 wind speed")
            self.wind_speed = 0.0
        else:
            self.wind_speed = wind_speed
        self._printed_wind_applied = False

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        obs = list(obs)
        obs[2] += self.wind_speed * 0.1 # modifying horizontal velocity

        if not self._printed_wind_applied:
            print(f"Applied wind speed {self.wind_speed:.2f} m/s, new horizontal velocity: {obs[2]:.2f}")
            self._printed_wind_applied = True
        return obs, reward, terminated, truncated, info