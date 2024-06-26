import os
import pickle
import click

from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error
from sklearn.metrics import root_mean_squared_error

import mlflow


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)

def run_train(data_path: str):
    mlflow.set_tracking_uri("sqlite:///mlflow.db")

    # Enable MLflow autologging for scikit-learn
    mlflow.sklearn.autolog(log_datasets=False)
    
    # Start an MLflow run
    with mlflow.start_run():
        X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
        X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)

        # rmse = mean_squared_error(y_val, y_pred, squared=False)
        rmse = root_mean_squared_error(y_val, y_pred)
        
        # Log the RMSE manually
        mlflow.log_metric("rmse", rmse)


if __name__ == '__main__':
    run_train()

