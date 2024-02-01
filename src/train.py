from PPO_solver.train import train, EvaluteModel

if __name__ == "__main__":
    file_name = "test14"
    log_dir = "tensor_dir_new_env"

    # train(200_000, file_name, log_dir, new=True, mines_overide=6)

    win_rate, mean_reward = EvaluteModel().run(file_name, eval_episodes=1000, render_mode=None, mines_overide=6)
    print(f"mean_reward: {mean_reward} win_rate: {win_rate}")
