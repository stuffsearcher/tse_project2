import preparation

import numpy as np
import pandas as pd

data_df = preparation.prepare_main_data(data_name="data").dropna()
turbine_data = preparation.prepare_turbine_data(data_name="turbine_data")


def calculate_monthly_yield(wind_series: pd.core.series.Series, turbine_name: str):
    filt = turbine_data["Turbine"] == turbine_name
    turbine_height = turbine_data[filt]["Height [m]"].iloc[0]

    wnd_series_at_x_height = wind_series.apply(
        preparation.log_law, args=(turbine_height,)
    )

    power_curve = turbine_data[filt]["Power P [kW]"]

    wind_speeds = np.arange(1, 31)  # Wind speeds from 1 to 30 m/s

    power_output = np.interp(wnd_series_at_x_height, wind_speeds, power_curve)

    time_interval = 1 / 6  # Conversion from 10-minute intervals
    total_energy = np.sum(power_output) * time_interval

    max_power = power_curve.max()
    theoretical_maximum = max_power * 30 * 24
    capicity_factor = (total_energy / theoretical_maximum) * 100

    print(
        f"Total energy yield/capacity factor for {turbine_name} in one month: {total_energy:.2f} kWh / {capicity_factor:.2f}  "
    )
    return total_energy


for tb_name in turbine_data["Turbine"].unique():
    calculate_monthly_yield(turbine_name=tb_name, wind_series=data_df["speed"])
