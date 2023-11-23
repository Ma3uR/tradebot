import numpy as np
from s_n_a import SnATradeIndicator as Indicator

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def plot_s_n_a(
        dataframe: pd.DataFrame,
        src: [str],
) -> None:
    """
    Plots data from a DataFrame.

    Parameters:
    - dataframe (pd.DataFrame): The DataFrame containing the data to be plotted.
    - src ([str]): A list of column names from the DataFrame to be plotted as lines.

    Returns:
    - None
    """


    # x = dataframe['DateTime']
    x = dataframe.index


    if 'range_filter' in dataframe.columns and 'range_filter' in src:
        if 'up_ward' in dataframe.columns and 'up_ward' in src:
            plt.plot(
                x,
                np.where(dataframe["up_ward"], dataframe['range_filter'], np.nan),
                label='up_ward',
                c='green')
        if 'down_ward' in dataframe.columns and 'down_ward' in src:
            plt.plot(
                x,
                np.where(dataframe["down_ward"], dataframe['range_filter'], np.nan),
                label='down_ward',
                c='red')
            if 'up_ward' in dataframe.columns and 'up_ward' in src:
                plt.plot(
                    x,
                    np.where(dataframe["down_ward"] == dataframe["up_ward"], dataframe['range_filter'], np.nan),
                    label='non_ward',
                    c='orange')

        if 'long_conditions' in dataframe.columns and 'long_conditions' in src:
            plt.scatter(
                x,
                np.where(dataframe["long_conditions"] == True, dataframe["range_filter"], None),
                marker='^',
                color='green',
                label='long'
            )
        if 'short_conditions' in dataframe.columns and 'short_conditions' in src:
            plt.scatter(
                x,
                np.where(dataframe["short_conditions"] == True, dataframe["range_filter"], None),
                marker='v',
                color='red',
                label='short'
            )
        dataframe.drop(['range_filter', 'down_ward', 'up_ward', "long_conditions", "short_conditions"],
                       axis=1, inplace=True)
    if ('high_band' in dataframe.columns and 'high_band' in src
            and 'low_band' in dataframe.columns and 'low_band' in src):
        plt.plot(x, dataframe['high_band'], c='lime')
        plt.plot(x, dataframe['low_band'], c='orangered')
        dataframe.drop(['high_band', 'low_band'], axis=1, inplace=True)

    

    for parameter in dataframe.columns:
        if parameter in src:
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
    # plt.grid(color="lightblue", linestyle="-", linewidth=0.2, alpha=1)
    # plt.show()


if __name__ == "__main__":

    df = pd.read_csv("../data/test_dataBTCUSDT_1m_2023-07-01_92days.csv")
    indicator = Indicator(df, "Close")

    plot_s_n_a(
        indicator.apply_indicator(),
        [
            "Close",
            "high_band",
            "low_band",
            "up_ward",
            "down_ward",
            "range_filter",
            "long_conditions",
            "short_conditions",
        ],
    )
