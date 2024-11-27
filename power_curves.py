import preparation

import matplotlib.pyplot as plt

plt.style.use("fivethirtyeight")


turbine_data = preparation.prepare_turbine_data(data_name="turbine_data")

enercon_data = turbine_data[turbine_data["Turbine"] == "Enercon E-53"]
gamesa_data = turbine_data[turbine_data["Turbine"] == "Gamesa G97 (2000kW)"]
vestas_data = turbine_data[turbine_data["Turbine"] == "Vestas V-117 (4.2MW)"]

plt.plot(enercon_data["Wind [m/s]"], enercon_data["Power P [kW]"], label="ENERCON")
plt.plot(gamesa_data["Wind [m/s]"], gamesa_data["Power P [kW]"], label="GAMESA")
plt.plot(vestas_data["Wind [m/s]"], vestas_data["Power P [kW]"], label="VESTAS")

plt.title("Power curves for all three turbines")

plt.annotate(
    "ENERCON and GAMESA turbines\nhave a cut-off speed of 26 m/s",
    xy=(26, 0),
    xycoords="data",
    xytext=(-40, 0),
    textcoords="offset points",
    arrowprops=dict(facecolor="black", shrink=0.05),
    horizontalalignment="right",
    verticalalignment="center",
    bbox=dict(boxstyle="round4,pad=.5", fc="0.8"),
)

plt.annotate(
    "VESTAS turbine does not\nexhibit a known cut-off speed",
    xy=(30, 3212),
    xycoords="data",
    xytext=(0, -70),
    textcoords="offset points",
    arrowprops=dict(facecolor="black", shrink=0.05),
    horizontalalignment="center",
    verticalalignment="bottom",
    bbox=dict(boxstyle="round4,pad=.5", fc="0.8"),
)

ves_gam_p_delta = vestas_data["Power P [kW]"].max() - gamesa_data["Power P [kW]"].max()

plt.annotate(
    f"ΔPₘₐₓ of {ves_gam_p_delta} kW",
    xy=(16.5, 3000),
    xytext=(16.5, 3000),
    xycoords="data",
    textcoords="data",
    bbox=dict(boxstyle="LArrow", fc="0.8"),
)

plt.annotate(
    "",
    xy=(16, 2000),
    xytext=(16, 4200),
    xycoords="data",
    textcoords="data",
    arrowprops=dict(color="black", arrowstyle="<->", lw=2),
)

gam_ene_p_delta = gamesa_data["Power P [kW]"].max() - enercon_data["Power P [kW]"].max()

plt.annotate(
    f"ΔPₘₐₓ of {gam_ene_p_delta} kW",
    xy=(16.5, 1400),
    xytext=(16.5, 1400),
    xycoords="data",
    textcoords="data",
    bbox=dict(boxstyle="LArrow", fc="0.8"),
)

plt.annotate(
    "",
    xy=(16, 810),
    xytext=(16, 2000),
    xycoords="data",
    textcoords="data",
    arrowprops=dict(color="black", arrowstyle="<->", lw=2),
)

plt.annotate(
    "ENERCON reaches\nPₘₐₓ at 13 m/s",
    xy=(13, 810),
    xycoords="data",
    xytext=(13, 300),
    textcoords="data",
    arrowprops=dict(facecolor="black", shrink=0.05),
    horizontalalignment="center",
    verticalalignment="center",
    bbox=dict(boxstyle="round4,pad=.5", fc="0.8"),
)

plt.annotate(
    "GAMESA reaches\nPₘₐₓ at 14 m/s",
    xy=(14, 2000),
    xycoords="data",
    xytext=(13, 1400),
    textcoords="data",
    arrowprops=dict(facecolor="black", shrink=0.05),
    horizontalalignment="center",
    verticalalignment="center",
    bbox=dict(boxstyle="round4,pad=.5", fc="0.8"),
)

plt.annotate(
    "GAMESA reaches\nPₘₐₓ at 14 m/s",
    xy=(15, 4200),
    xycoords="data",
    xytext=(13, 3000),
    textcoords="data",
    arrowprops=dict(facecolor="black", shrink=0.05),
    horizontalalignment="center",
    verticalalignment="center",
    bbox=dict(boxstyle="round4,pad=.5", fc="0.8"),
)

plt.ylabel("Power [kW]")
plt.xlabel("Wind Speed [m/s]")
plt.legend(loc="upper left", borderaxespad=2, title="Turbines", reverse=True)

plt.show()
