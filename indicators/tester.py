import numpy as np
import time
from s_n_a import SnATradeIndicator
from b2 import B2TradeIndicator
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
from s_n_a_tester import plot_s_n_a
from b2_tester import plot_dataframe as plot_b2


def apply_plot(*indicators):
    plot_s_n_a(indicators[0].apply_indicator(), [
            "Close",
            "high_band",
            "low_band",
            "up_ward",
            "down_ward",
            "range_filter",
            "long_conditions",
            "short_conditions",
        ],)
    plot_b2(indicators[1].apply_indicator().ffill(), [
            # "Close",
            "Up",
            "Dn",
        ], )


def show_candles_on_plot(historical_data):
    for i in range(len(historical_data.index)):

        if historical_data.get('Close')[i] > historical_data.get('Open')[i]:
            plt.plot([i + 1, i + 1], [historical_data.get('High')[i], historical_data.get('Low')[i]],
                     color='green', linewidth=1)
            plt.plot([i + 1, i + 1], [historical_data.get('Close')[i], historical_data.get('Open')[i]],
                     color='green', linewidth=9)

        else:
            plt.plot([i + 1, i + 1], [historical_data.get('High')[i], historical_data.get('Low')[i]],
                     color='red', linewidth=1)
            plt.plot([i + 1, i + 1], [historical_data.get('Close')[i], historical_data.get('Open')[i]],
                     color='red', linewidth=9)


def show_candles_on_plot1(historical_data):
  
    # col1 = 'orangered'
    # col2 = 'lime'
    col1 = 'peru'
    col2 = 'cadetblue'

    # Set the width of candlestick elements
    width = 1.1
    width2 = 0.3

    up = historical_data.where(historical_data['Close'] >= historical_data['Open'], None)    
    down = historical_data.where(historical_data['Close'] < historical_data['Open'], None)
    # Plot the up prices of the stock
    plt.bar(historical_data.index, up['Close'] - up['Open'], width, bottom=up['Open'], color=col2, alpha=0.6)
    plt.bar(historical_data.index, up['High'] - up['Close'], width2, bottom=up['Close'], color=col2)
    plt.bar(historical_data.index, up['Low'] - up['Open'], width2, bottom=up['Open'], color=col2)

    # Plot the down prices of the stock
    plt.bar(historical_data.index, down['Close'] - down['Open'], width, bottom=down['Open'], color=col1, alpha=0.6)
    plt.bar(historical_data.index, down['High'] - down['Open'], width2, bottom=down['Open'], color=col1)
    plt.bar(historical_data.index, down['Low'] - down['Close'], width2, bottom=down['Close'], color=col1)


if __name__ == "__main__":
    df = pd.read_csv("../data/test_dataBTCUSDT_1m_04_10_23.csv", index_col="DateTime")

    s_n_a = SnATradeIndicator(df, "close")
    b2 = B2TradeIndicator(df, "close")

    # show_candles_on_plot(df)
    show_candles_on_plot1(df)
    apply_plot(s_n_a, b2)
    
    ax = plt.gca()
    # Set the x-axis locator to MaxNLocator with the desired number of ticks
    ax.xaxis.set_major_locator(MaxNLocator(nbins=50))
    plt.xticks(rotation=90)    
    plt.legend()
    plt.ylabel("Price")
    plt.xlabel("Time")
    plt.grid(color="lightblue", linestyle="-", linewidth=0.2, alpha=1)
    plt.show()