from PPO_solver.train import train, EvaluteModel

def optimize_ppo(trial):
    """ Learning hyperparamters we want to optimise"""
    # Use a step and batch size factor here instead of getting the factor directly to
    # avoid trucated mini batches
    # n_steps = trial.suggest_int('n_steps', 576, 9024, step=192)
    # batch_size_factor = trial.suggest_int('batch_size_factor', 16, 64, step=16)
    return {
        'n_steps': 4096, #n_steps,
        'n_epochs': trial.suggest_int('n_epochs', 3, 30),
        "batch_size": 128, #int(n_steps/batch_size_factor),
        'gamma': trial.suggest_float('gamma', .8, 0.9999),
        "gae_lambda": trial.suggest_float("gae_lambda", .9, 1),
        'learning_rate': trial.suggest_float('learning_rate', 1e-5, .0006),
        'clip_range': trial.suggest_float('cliprange', 0.1, 0.3, step=.1),
        'ent_coef': trial.suggest_float('ent_coef', 1e-5, .05),
        'vf_coef': trial.suggest_float('vf_coef', 0.5, 1.)
    }

def objective(trial):
    """ Train the model and optimize
        Optuna maximises the negative log likelihood, so we
        need to negate the reward here
    """
    log_dir = "tensor_dir_opt_4"
    file_name = f"{trial.number}_OPT_PPO"
    model_params = optimize_ppo(trial)
    print(f"trial number: {trial.number} - {model_params}")

    train(1_000_000, file_name, log_dir, mines_overide=6, model_params=model_params)
    print(f"trial number : {trial.number} calling evaluate")

    win_rate, mean_reward = EvaluteModel().run(file_name, eval_episodes=1000, render_mode=None, mines_overide=6)
    print(f"trial number: {trial.number} mean_reward: {mean_reward} win_rate: {win_rate}")
    return mean_reward, win_rate
