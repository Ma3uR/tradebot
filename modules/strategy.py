import pandas as pd
import numpy as np
from modules import Trade
from indicators import (
    B2TradeIndicator,
    SnATradeIndicator,
)
from .interfaces import ABCStrategy


class Strategy(ABCStrategy):
    """
    Example
    --------
    ::
        if __name__ == "__main__":
            dataframe = pd.read_csv("{your_data_file}.csv")
            strategy = Strategy(
                indicators=[B2TradeIndicator, SnATradeIndicator],
                indicator_settings={
                    "B2TradeIndicator": {'source':'hlc3',},
                    "SnATradeIndicator": {'source':'close',},
                },
                price_settings= {}
            )
            signals = strategy.get_signals(dataframe)
    """

    def __init__(self, indicators, indicator_settings, price_settings={}):
        self.indicators = indicators
        self.indicator_settings = indicator_settings
        (
            self.long_sl_multiplier,
            self.long_tp_multiplier,
            self.short_sl_multiplier,
            self.short_tp_multiplier,
        ) = (
            price_settings.get("long_sl_multiplier", 0.01),
            price_settings.get("long_tp_multiplier", 0.01),
            price_settings.get("short_sl_multiplier", 0.01),
            price_settings.get("short_tp_multiplier", 0.01),
        )

        self.signals = None

    def init_indicators(self, test_data: pd.DataFrame) -> None:
        signals = test_data
        # conflicts = []
        # Comparing signals & conflicts excluding
        for indicator_class in self.indicators:
            indicator_name = indicator_class.__name__
            indicator_params = self.indicator_settings.get(indicator_name, {})
            indicator = indicator_class(dataframe=test_data, **indicator_params)

            indicator_data = indicator.apply_indicator()

            if "long_conditions" in signals:
                signals["long_conditions"] ^= indicator_data["short_conditions"]
            else:
                signals["long_conditions"] = indicator_data["long_conditions"]
                signals["source"] = indicator_data["source"]

            if "short_conditions" in signals:
                signals["short_conditions"] ^= indicator_data["long_conditions"]
            else:
                signals["short_conditions"] = indicator_data["short_conditions"]
                signals["source"] = indicator_data["source"]

        # Stop_loss and Take_profit setting
        idx = signals.index[signals["long_conditions"]]
        signals.loc[idx, "stop_loss"] = signals.loc[idx, "source"] * (
            1 - self.long_sl_multiplier
        )
        signals.loc[idx, "take_profit"] = signals.loc[idx, "source"] * (
            1 + self.long_tp_multiplier
        )

        idx = signals.index[signals["short_conditions"]]
        signals.loc[idx, "stop_loss"] = signals.loc[idx, "source"] * (
            1 + self.short_sl_multiplier
        )
        signals.loc[idx, "take_profit"] = signals.loc[idx, "source"] * (
            1 - self.short_tp_multiplier
        )
        self.signals = signals

    def get_signals(self, test_data: pd.DataFrame) -> pd.DataFrame:
        if self.signals is None:
            self.init_indicators(test_data)


        return self.signals


if __name__ == "__main__":
    dataframe = pd.read_csv("data/test_dataBTCUSDT_1m_09_10_23.csv")
    strategy = Strategy(
        indicators=[B2TradeIndicator, SnATradeIndicator],
        indicator_settings={
            "B2TradeIndicator": {
                "source": "hlc3",
            },
            "SnATradeIndicator": {
                "source": "close",
            },
        },
        price_settings={},
    )
    signals = strategy.get_signals(dataframe)
