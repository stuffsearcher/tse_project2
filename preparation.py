import numpy as np
import pandas as pd
from scipy.special import gamma


def prepare_main_data(data_name: str, annual=False):
    data_df = pd.read_csv(f"cwd/{data_name}.csv")

    # Name and type handling
    data_df.columns = ["date", "speed", "wnd_direction"]
    data_df["date"] = pd.to_datetime(data_df["date"])
    data_df.dropna(inplace=True)

    if annual:
        data_df = prepare_for_annual(data_df)

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
        np.log(turbine_height / open_flat_roughness)
        / np.log(data_height / open_flat_roughness)
    )


def prepare_for_annual(dataframe):
    mean = dataframe["speed"].mean()

    variations = {
        "summer": {
            "mean": mean,
            "start_date": "2016-06-01",
            "end_date": "2016-08-31",
        },
        "autumn": {
            "mean": mean * 1.05,
            "start_date": "2016-09-01",
            "end_date": "2016-11-30",
        },
        "winter": {
            "mean": mean * 1.1,
            "start_date": "2016-12-01",
            "end_date": "2017-02-28",
        },
        "spring": {
            "mean": mean * 1.05,
            "start_date": "2016-03-01",
            "end_date": "2016-05-31",
        },
    }

    new_df = pd.DataFrame({"date": [], "speed": [], "wnd_direction": []})

    for season in variations.items():
        datetime_series = pd.date_range(
            start=season[1]["start_date"], end=season[1]["end_date"], freq="10min"
        )
        if season[0] == "summer":
            # Define the date range to exclude
            start_drop = pd.Timestamp("2016-07-01")
            end_drop = pd.Timestamp("2016-08-01")

            # Filter the datetime_series to exclude the range
            datetime_series = datetime_series[
                (datetime_series < start_drop) | (datetime_series >= end_drop)
            ]

        desired_mean = season[1]["mean"]

        shape = 2.125117825030581
        scale = desired_mean / gamma(1 + 1 / shape)

        size = len(datetime_series)

        weibull_series = scale * np.random.weibull(shape, size)

        temp_df = pd.DataFrame({"date": datetime_series, "speed": weibull_series})
        new_df = pd.concat([new_df, temp_df], ignore_index=True)

    return new_df


if __name__ == "__main__":
    data = prepare_main_data(input("Enter main data document name: "))

    turbine_data = prepare_turbine_data(input("Enter turbine data document name: "))

    print(data.head(5))
    print(turbine_data.head(5))
