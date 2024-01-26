from PPO_solver.minesweeper_env import MinesweeperEnv

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.utils import set_random_seed

def make_env(env, rank: int, seed: int = 0):
    """
    Utility function for multiprocessed env.

    :param env_id: the environment ID
    :param num_env: the number of environments you wish to have in subprocesses
    :param seed: the inital seed for RNG
    :param rank: index of the subprocess
    """
    def _init():
        env.reset(seed=seed + rank)
        return env
    set_random_seed(seed)
    return _init

def train(file_name):
    env = MinesweeperEnv(render_mode=None)
    num_cpu = 3
    vec_env = SubprocVecEnv([make_env(env, i) for i in range(num_cpu)], start_method="spawn")

    model = PPO(
        "MlpPolicy",
        vec_env,
        verbose=2,
        stats_window_size=100,
        tensorboard_log="tensor_dir",
        learning_rate=.00003,
        gamma=.1,
        gae_lambda=.9,
    )
    model.learn(total_timesteps=200_000)
    model.save(file_name)

def run(file_name):
    env = MinesweeperEnv(render_mode="human")
    num_cpu = 1
    vec_env = SubprocVecEnv([make_env(env, i) for i in range(num_cpu)], start_method="spawn")
    model = PPO.load(file_name, env=vec_env)
    obs = vec_env.reset()
    games = 0
    while games < 10:
        action, _states = model.predict(obs)
        obs, rewards, dones, info = vec_env.step(action)
        print(f"Reward: {rewards} Dones: {dones} Action: {action}")
        if dones: games += 1

if __name__ == "__main__":
    file_name = "test1"
    train(file_name)
    run(file_name)

