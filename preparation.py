import pandas as pd
import numpy as np


def prepare_main_data(data_name: str):
    data_df = pd.read_csv(f"cwd/{data_name}.csv")

    # Name and type handling
    data_df.columns = ["date", "speed", "wnd_direction"]
    data_df["date"] = pd.to_datetime(data_df["date"])

    # Speed and direction data binning
    max_speed = int(np.round(data_df["speed"].max()))
    data_df["speed_bins"] = pd.cut(data_df["speed"], [x for x in range(max_speed + 1)])
    data_df["wnd_direction_bins"] = pd.cut(
        data_df["wnd_direction"], [x for x in range(375)[0:375:15]]
    )

    return data_df


def prepare_turbine_data(data_name: str):
    turbine_data = pd.read_csv(f"cwd/{data_name}.csv")

    return turbine_data


def log_law(vel: np.float64, turbine_height: float):
    data_height = 20
    open_flat_roughness = 0.03

    return vel * (
        np.log(data_height / open_flat_roughness)
        / np.log(turbine_height / open_flat_roughness)
    )


if __name__ == "__main__":
    data = prepare_main_data(input("Enter main data document name: "))

    turbine_data = prepare_turbine_data(input("Enter turbine data document name: "))

    print(data.head(5))
    print(turbine_data.head(5))
