import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt


def plot_dataframe_base(
    dataframe: pd.DataFrame,
    src: [str] = None,
    prct: float | int = 40,
):
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

    fig, signals_ax = plt.subplots()
    x = dataframe["DateTime"]
    plt.scatter(
        x,
        np.where(dataframe["Side"]=="LONG", dataframe["Close"], None),
        marker="^",
        color="red",
        label="LONG Signal",

    )
    plt.scatter(
        x,
        np.where(dataframe["Side"]=="SHORT", dataframe["Close"], None),
        marker="v",
        color="blue",
        label="SHORT Signal",
    )        
    # plt.scatter(
    #     x,
    #     np.where(dataframe["Side"]=="LONG", dataframe["Close"], None),
    #     marker="v",
    #     color="red",
    #     label="Sell Signal",

    # )
    # plt.scatter(
    #     x,
    #     np.where(dataframe["Side"]=="SHORT", dataframe["Close"], None),
    #     marker="^",
    #     color="blue",
    #     label="Buy Signal",
    # )        
    for parameter in dataframe.columns:
        if src:
            if parameter in src:
                if parameter == "Close":
                    plt.plot(
                        x,
                        dataframe[parameter],
                        label=parameter,
                    )

                else:
                    plt.scatter(
                        x,
                        dataframe[parameter],
                        label=parameter,
                    )
        else:
            plt.plot(
                x,
                dataframe[parameter],
                label=parameter,
            )
            
    
    ax = plt.gca()
    
    
    # Set the x-axis locator to MaxNLocator with the desired number of ticks
    ax.xaxis.set_major_locator(MaxNLocator(nbins=50))
    # Rotate the x-axis labels for better visibility
    plt.xticks(rotation=90)
    plt.legend()
    plt.ylabel("Price")
    plt.xlabel("Time")
    plt.show()
