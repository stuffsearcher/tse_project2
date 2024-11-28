import numpy
import pandas
from matplotlib import pyplot
import seaborn

import preparation

data_df = preparation.prepare_main_data("data")

data_df = data_df.rename(columns={"speed": "WindSpd", "wnd_direction": "WindDir"})
seaborn.set_style("ticks")

data_df.head(8)

total_count = data_df.shape[0]
calm_count = data_df.query("WindSpd == 0").shape[0]

print("Of {} total observations, {} have calm winds.".format(total_count, calm_count))


def speed_labels(bins, units):
    labels = []
    for left, right in zip(bins[:-1], bins[1:]):
        if left == bins[0]:
            labels.append("calm".format(right))
        elif numpy.isinf(right):
            labels.append(">{} {}".format(left, units))
        else:
            labels.append("{} - {} {}".format(left, right, units))

    return list(labels)


def _convert_dir(directions, N=None):
    if N is None:
        N = directions.shape[0]
    barDir = directions * numpy.pi / 180.0 - numpy.pi / N
    barWidth = 2 * numpy.pi / N
    return barDir, barWidth


spd_bins = [-1, 0, 5, 10, 15, 20, 25, 30, numpy.inf]
spd_labels = speed_labels(spd_bins, units="meter/second")

dir_bins = numpy.arange(-7.5, 370, 15)
dir_labels = (dir_bins[:-1] + dir_bins[1:]) / 2

rose = (
    data_df.assign(
        WindSpd_bins=lambda df: pandas.cut(
            df["WindSpd"], bins=spd_bins, labels=spd_labels, right=True
        )
    )
    .assign(
        WindDir_bins=lambda df: pandas.cut(
            df["WindDir"], bins=dir_bins, labels=dir_labels, right=False
        )
    )
    .replace({"WindDir_bins": {360: 0}})
    .groupby(by=["WindSpd_bins", "WindDir_bins"])
    .size()
    .unstack(level="WindSpd_bins")
    .fillna(0)
    .assign(calm=lambda df: calm_count / df.shape[0])
    .sort_index(axis=1)
    .applymap(lambda x: x / total_count * 100)
)


def wind_rose(rosedata, wind_dirs, palette=None):
    if palette is None:
        palette = seaborn.color_palette("inferno", n_colors=rosedata.shape[1])

    bar_dir, bar_width = _convert_dir(wind_dirs)

    fig, ax = pyplot.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.set_theta_direction("clockwise")
    ax.set_theta_zero_location("N")

    for n, (c1, c2) in enumerate(zip(rosedata.columns[:-1], rosedata.columns[1:])):
        if n == 0:
            # first column only
            ax.bar(
                bar_dir,
                rosedata[c1].values,
                width=bar_width,
                color=palette[0],
                edgecolor="none",
                label=c1,
                linewidth=0,
            )

        # all other columns
        ax.bar(
            bar_dir,
            rosedata[c2].values,
            width=bar_width,
            bottom=rosedata.cumsum(axis=1)[c1].values,
            color=palette[n + 1],
            edgecolor="none",
            label=c2,
            linewidth=0,
        )

    leg = ax.legend(loc=(0.75, 0.95), ncol=2)
    xtl = ax.set_xticklabels(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
    ax.set_title("Wind Rose at 20 meters")
    return fig


directions = numpy.arange(0, 360, 15)
fig = wind_rose(rose, directions)
fig.show()
