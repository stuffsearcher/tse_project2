import preparation

from scipy.stats import weibull_min
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import reliability

data_df = preparation.prepare_main_data(data_name="data")

data_df.dropna(inplace=True)

speed_arr = np.array(data_df["speed"])

# Using maximum likelihood estimation (MLE)
weibull_parameters = reliability.Fitters.Fit_Weibull_2P(
    speed_arr, show_probability_plot=False
)

# Weibull scale parameter
alpha = weibull_parameters.alpha
# Weibull shape parameter
beta = weibull_parameters.beta


def calculate_weibull_distribution(vel: np.float64):
    return (
        (beta / alpha)
        * np.power(vel / alpha, beta - 1)
        * np.exp(-np.power(vel / alpha, beta))
    )


data_df["weibull_dist"] = data_df["speed"].apply(calculate_weibull_distribution)
weibull_dist_series = data_df.sort_values("speed")["weibull_dist"]

bar_data = data_df["speed_bins"].value_counts(normalize=True).sort_index()

max_speed = int(np.round(data_df["speed"].max()))
speed_bins = [x for x in range(max_speed + 1)]

bar_x_axis = [str(x) for x in bar_data.index]

shape, loc, scale = weibull_min.fit(data_df["speed"], loc=-1)

x = np.linspace(data_df["speed"].min(), data_df["speed"].max(), len(data_df["speed"]))
pdf = weibull_min.pdf(x, beta, loc, alpha)
plt.plot(x, pdf * 100, "r--", label="Fitted Weibull PDF")
plt.bar(bar_x_axis, bar_data.values * 100, edgecolor="black")
plt.title("prueba")
plt.xticks(rotation=90)
plt.show()


plt.hist(
    data_df["speed"],
    bins=speed_bins,
    density=True,
    alpha=0.6,
    color="skyblue",
    label="Distribuion",
    edgecolor="black",
)
plt.plot(x, pdf, "r--", label="Fitted Weibull PDF")
plt.legend()
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
plt.show()