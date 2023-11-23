import pandas as pd
from modules.backtester import Backtester
from indicators import (
    SnATradeIndicator,
    B2TradeIndicator,
)
from modules import Strategy
from config import ROOT_PATH
from pathlib import Path
from os import path
from typing import Union

if __name__ == "__main__":
    root = Path(__file__).parent
    dataframe = pd.read_csv(Path(root, "data", "test_dataBTCUSDT_1m_09_10_23.csv"))
    sna_indicator = SnATradeIndicator(dataframe, source="close")
    sna_data = sna_indicator.apply_indicator()
    r_filter = sna_data["range_filter"]
    h_target = sna_data["high_band"]
    l_target = sna_data["low_band"]
    # 10$
    # 20$
    # 40$
    # 80$
    # 160$
    # 320$
    # 640$
    # 1280$
    # 2560$
    volumes = [ 10, 20, 40, 80, 160, 320, 640, 1280, 2560 ]
    strategy = Strategy(
        indicators=[
            SnATradeIndicator,
            B2TradeIndicator,
        ],
        indicator_settings={
            "SnATradeIndicator": {
                "source": "hlc3",
            },
            "B2TradeIndicator": {
                "source": "another_source",
                "another_source": r_filter,
            },
        },
        price_settings={},
    )
    backtester = Backtester(
        strategy, 
        # volumes=volumes
        long_sl_percent_margin=0.001,
        # short_sl_percent_margin=0.004,
        )
    backtester.backtest(dataframe)
    print(f"Initial Balance: {backtester.initial_balance:.2f}")
    print(f"Final Balance: {backtester.balance:.2f}")
    print(f"Win Rate: {backtester.win_rate:.2f}%")
    print(f"Count of Wins: {backtester.wins}")
    print(f"Count of Losses: {backtester.losses}")
    print(f"Profit Factor: {backtester.profit_factor:.2f}")
