import optuna
from optuna.study import StudyDirection

from PPO_solver.optimizehyperparams import objective

if __name__ == "__main__":
    study_name = "study_3"
    storage_name = "sqlite:///{}.db".format(study_name)
    study = optuna.create_study(
        study_name=study_name,
        storage=storage_name,
        load_if_exists=True,
        directions=[StudyDirection.MAXIMIZE, StudyDirection.MAXIMIZE],
    )
    try:
        study.optimize(
            objective,
            n_trials=100,
            n_jobs=1,
        )
    except KeyboardInterrupt:
        print('Interrupted by keyboard.')

    print(f"best trials: {study.best_trials}")
    print(f"best params: {study.best_params}")
    print(f"best trial: {study.best_trial}")
    print(f"best value: {study.best_value}")