from PPO_solver.minesweeper_env import MinesweeperEnv

import optuna

from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.logger import HParam
from stable_baselines3.common.monitor import Monitor

def eval_callback(locals, globals):
    print(f"locals: {locals['reward']} - {locals['done']}")

class TensorboardCallback(BaseCallback):
    """
    Custom callback for plotting additional values in tensorboard.
    """

    def __init__(self, verbose=0):
        super().__init__(verbose)

    def _on_training_start(self) -> None:
        hparam_dict = {
            "algorithm": self.model.__class__.__name__,
            "learning rate": self.model.learning_rate,
            "gamma": self.model.gamma,
            "gae_lambda": self.model.gae_lambda,
            "n_steps": self.model.n_steps,
            "batch_size": self.model.batch_size,
            "n_epochs": self.model.n_epochs,
            "ent_coef": self.model.ent_coef,
            "vf_coef": self.model.vf_coef,
        }

        metric_dict = {
            "rollout/ep_len_mean": 0,
            "rollout/ep_rew_mean": 0,
        }
        self.logger.record(
            "hparams",
            HParam(hparam_dict, metric_dict),
            exclude=("stdout", "log", "json", "csv"),
        )
        
    def _on_step(self) -> bool:
        # if self.training_env.get_attr("reset_stats_next_step"):
        #     rewards_this_episode = self.training_env.get_attr("reward_this_episode")
        #     steps_this_episode = self.training_env.get_attr("steps_this_episode")
        #     for i in range(self.locals['env'].num_envs):
        #         self.logger.record("env_stats/rew_per_eps", rewards_this_episode[i])
        #         self.logger.record("env_stats/steps_per_eps", steps_this_episode[i])
        return True

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

def train(file_name, new=True):
    log_dir = "tensor_dir_opt"
    env = MinesweeperEnv(render_mode=None)
    num_cpu = 3
    # vec_env = SubprocVecEnv([make_env(env, i) for i in range(num_cpu)], start_method="spawn")

    if new:
        model = PPO(
            "MlpPolicy",
            env,
            verbose=2,
            stats_window_size=100,
            tensorboard_log=log_dir,
            learning_rate=.0002626,
            gamma=.9798,
            # gae_lambda=.95,
            # n_steps=2048,
            # batch_size=128,
            # n_epochs=3,
            ent_coef=.0053143,
            vf_coef=.98106,
        )
    else:
        model = PPO.load(file_name, env=env)
    
    for i in range(1):
        model.learn(
            total_timesteps=1_000_000,
            callback=TensorboardCallback(),
            tb_log_name=file_name,
            reset_num_timesteps=(i==0 and new)
        )
        model.save(file_name)
        # run(file_name)

def run(file_name):
    env = MinesweeperEnv(render_mode="human")
    m_env = Monitor(env)
    model = PPO.load(file_name, env=m_env)
    mean_reward, _ = evaluate_policy(
        model,
        m_env,
        deterministic=False,
        n_eval_episodes=10,
        callback=eval_callback
    )
    print(f"mean_reward: {mean_reward}")
    # obs = vec_env.reset()
    # games = 0
    # while games < 6:
        # action, _states = model.predict(obs)
    #     obs, rewards, dones, info = vec_env.step(action)
    #     print(f"Reward: {rewards} Dones: {dones} Action: {action}")
    #     if dones: games += 1

if __name__ == "__main__":
    # file_name = "test7"

    # train(file_name, new=False)

    # run(file_name)
    