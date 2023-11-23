from b2 import B2TradeIndicator as Indicator


import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import timeit

# plt.style.use('dark_background')
# plt.rcParams.update(
#     {
#         "lines.color": "white",
#         "patch.edgecolor": "white",
#         "text.color": "black",
#         "axes.facecolor": "white",
#         "axes.edgecolor": "lightgray",
#         "axes.labelcolor": "white",
#         "xtick.color": "white",
#         "ytick.color": "white",
#         "grid.color": "lightgray",
#         "figure.facecolor": "black",
#         "figure.edgecolor": "black",
#         "savefig.facecolor": "black",
#         "savefig.edgecolor": "black",
#     }
# )



def plot_dataframe(
    dataframe: pd.DataFrame,
    src: [str],
):

    x = dataframe.index

    plt.scatter(
        x,
        np.where(dataframe["long_conditions"], dataframe["Up"], np.nan),
        marker="^",
        color="green",
        label="Long Signal",
    )
    plt.scatter(
        x,
        np.where(dataframe["short_conditions"], dataframe["Dn"], np.nan),
        marker="v",
        color="red",
        label="Short Signal",
    )
    for parameter in dataframe.columns:
        if parameter in src:
            if parameter in ["Dn"]:
                plt.plot(
                    x,
                    dataframe[parameter],
                    label=parameter,
                    color="red",
                    drawstyle="steps-post",
                )
            elif parameter in ["Up"]:
                plt.plot(
                    x,
                    dataframe[parameter],
                    label=parameter,
                    color="green",
                    drawstyle="steps-post",
                )
            else:
                plt.plot(
                    x,
                    dataframe[parameter],
                    label=parameter,
                )

    # ax = plt.gca()
    # # Set the x-axis locator to MaxNLocator with the desired number of ticks
    # ax.xaxis.set_major_locator(MaxNLocator(nbins=50))
    # # Rotate the x-axis labels for better visibility
    # plt.xticks(rotation=90)
    # plt.legend()
    # plt.ylabel("Price")
    # plt.xlabel("Time")
    # plt.grid(color="lightblue", linestyle="-", linewidth=0.5, alpha=0.2)
    # plt.show()


if __name__ == "__main__":
    
    df = pd.read_csv("../data/test_dataBTCUSDT_1m_09_10_23.csv")
    # df = pd.read_csv("../data/test_dataBTCUSDT_1m_04_10_23.csv")
    settings = {
        "periods": 100,
        "multiplier": 0.5,
        "changeATR": False,
        "showsignals": True,
    }
    indicator = Indicator(df, "close", **settings)
    dataframe = indicator.apply_indicator()
    print(f'{dataframe=}')
    plot_dataframe(
        dataframe.ffill(),
        [
            "Close",
            "Up",
            "Dn",
            # "Trend"
        ],
    )
