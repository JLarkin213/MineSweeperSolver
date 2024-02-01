from PPO_solver.minesweeper_env import MinesweeperEnv

from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.logger import HParam
from stable_baselines3.common.monitor import Monitor

class TensorboardCallback(BaseCallback):
    """
    Custom callback for plotting additional values in tensorboard.
    """

    def __init__(self, verbose=0):
        self.total_episodes = []
        self.wins = []
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
            "custom/win_rate": 0,
        }
        self.logger.record(
            "hparams",
            HParam(hparam_dict, metric_dict),
            exclude=("stdout", "log", "json", "csv"),
        )

        self.logger.record("custom/total_episodes", 0)
        self.logger.record("custom/win_rate", 0)
        
    def _on_step(self) -> bool:
        dones = self.locals["dones"]
        infos = self.locals["infos"]
        for idx, done in enumerate(dones):
            if (done):
                try:
                    self.total_episodes[idx] += 1
                except IndexError:
                    self.total_episodes.append(1)

                if (infos[idx]["win"]):
                    try:
                        self.wins[idx] += 1
                    except IndexError:
                        self.wins.append(1)
                
                if (self.total_episodes[idx] % 100 == 0):
                    try:
                        wins = self.wins[idx]
                    except IndexError:
                        wins = 0
                        self.wins.append(0)

                    win_rate = wins/100
                    self.logger.record("custom/total_episodes", self.total_episodes[idx])
                    self.logger.record("custom/win_rate", win_rate)

                    self.wins[idx] = 0
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

def train(timesteps, file_name, log_dir, new=True, mines_overide=None, model_params=None):
    env = MinesweeperEnv(render_mode=None, mines_overide=mines_overide)
    check_env(env)
    num_cpu = 3
    # vec_env = SubprocVecEnv([make_env(env, i) for i in range(num_cpu)], start_method="spawn")
    if not model_params:
        model_params = {
            "learning_rate": .0003,
            "gamma": .985,
            "gae_lambda": .94,
            "n_steps": 4096,
            "batch_size": 128,
            "n_epochs": 30,
            "clip_range": .2,
            "ent_coef": .015,
            "vf_coef": .95,
        }

    if new:
        model = PPO(
            "MlpPolicy",
            env,
            verbose=2,
            stats_window_size=100,
            tensorboard_log=log_dir,
            **model_params
        )
    else:
        model = PPO.load(file_name)
        model.set_env(env)
    
    model.learn(
        total_timesteps=timesteps,
        callback=TensorboardCallback(),
        tb_log_name=file_name,
        reset_num_timesteps=new
    )
    model.save(file_name)
    del model

class EvaluteModel(object):
    def __init__(self) -> None:
        self.wins = 0

    def run(self, file_name, eval_episodes, render_mode="human", mines_overide=None):
        env = MinesweeperEnv(render_mode=render_mode, mines_overide=mines_overide)
        m_env = Monitor(env)
        model = PPO.load(file_name, env=env)
        mean_reward, _ = evaluate_policy(
            model,
            m_env,
            deterministic=False,
            n_eval_episodes=eval_episodes,
            callback=self._eval_callback
        )
        win_rate = self.wins/eval_episodes

        return win_rate, mean_reward

    def _eval_callback(self, locals, globals):
        if (locals["infos"][0]["win"]):
            self.wins += 1
        # print(f"locals: {locals['reward']} - {locals['done']}")
        # print(f"Obs Space: {locals['new_observations']}")
    