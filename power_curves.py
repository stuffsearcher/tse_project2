import preparation

import matplotlib.pyplot as plt

turbine_data = preparation.prepare_turbine_data(data_name="turbine_data")

enercon_data = turbine_data[turbine_data["Turbine"] == "Enercon E-53"]
gamesa_data = turbine_data[turbine_data["Turbine"] == "Gamesa G97 (2000kW)"]
vestas_data = turbine_data[turbine_data["Turbine"] == "Vestas V-117 (4.2MW)"]

plt.plot(enercon_data["Wind [m/s]"], enercon_data["Power P [kW]"])
plt.plot(gamesa_data["Wind [m/s]"], gamesa_data["Power P [kW]"])
plt.plot(vestas_data["Wind [m/s]"], vestas_data["Power P [kW]"])

plt.show()
