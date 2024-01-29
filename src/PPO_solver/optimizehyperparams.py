from PPO_solver.minesweeper_env import MinesweeperEnv
from PPO_solver.train import TensorboardCallback

import optuna

from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor

def optimize_ppo(trial):
    """ Learning hyperparamters we want to optimise"""
    # Use a step and batch size factor here instead of getting the factor directly to
    # avoid trucated mini batches
    n_steps = trial.suggest_int('n_steps', 576, 9024, step=192)
    batch_size_factor = trial.suggest_int('batch_size_factor', 16, 64, step=16)
    return {
        'n_steps': n_steps,
        'n_epochs': trial.suggest_int('n_epochs', 3, 30),
        "batch_size": int(n_steps/batch_size_factor),
        'gamma': trial.suggest_float('gamma', .9, 0.9999),
        "gae_lambda": trial.suggest_float("gae_lambda", .9, 1),
        'learning_rate': trial.suggest_float('learning_rate', 1e-5, .0005),
        'clip_range': trial.suggest_float('cliprange', 0.1, 0.4),
        'ent_coef': trial.suggest_float('ent_coef', 1e-5, .05),
        'vf_coef': trial.suggest_float('vf_coef', 0.9, 1.)
    }

def objective(trial):
    """ Train the model and optimize
        Optuna maximises the negative log likelihood, so we
        need to negate the reward here
    """
    log_dir = "tensor_dir_opt_2"
    file_name = f"OPT_PPO_{trial.number}"
    model_params = optimize_ppo(trial)
    print(f"trial number: {trial.number} - {model_params}")

    env  = MinesweeperEnv(render_mode=None)
    model = PPO('MlpPolicy', env, verbose=2, tensorboard_log=log_dir, **model_params)
    model.learn(200_000, callback=TensorboardCallback(), tb_log_name=file_name)
    print(f"trial number : {trial.number} calling evaluate")

    m_env = Monitor(env)
    mean_reward, _ = evaluate_policy(model, m_env, deterministic=False, n_eval_episodes=100)
    print(f"trial number: {trial.number} mean_reward: {mean_reward}")
    return -1 * mean_reward


if __name__ == "__main__":
    study_name = "study_1"
    storage_name = "sqlite:///{}.db".format(study_name)
    study = optuna.create_study(
        study_name=study_name,
        storage=storage_name,
        load_if_exists=True,
    )
    try:
        study.optimize(objective, n_trials=100, n_jobs=1)
    except KeyboardInterrupt:
        print('Interrupted by keyboard.')

    print(f"best trails: {study.best_trials}")
    print(f"best params: {study.best_params}")
    print(f"best trial: {study.best_trial}")
    print(f"best value: {study.best_value}")