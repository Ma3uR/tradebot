import json
import logging
from modules import (
    Strategy,
    # Bot,
    # Trade,
    Backtester,
)
import pandas as pd
from indicators import B2TradeIndicator, SnATradeIndicator
from pprint import pprint
from config import ROOT_PATH

def main():
    # try:
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        # logging.basicConfig(level=logging.INFO)
        with open("settings.json", "r") as _:
            settings = json.load(_)
        dataframe = pd.read_csv(
            'data/test_dataBTCUSDT_1m_09_10_23.csv'
            # 'indicators/binance_data_cci.csv'
        )
        # for i in settings:
        # try:
        indicators = {
            "b2":{
                'settings': settings.get('b2'),
                'indicator': B2TradeIndicator,
            },
            "s&a":{
                'settings': settings.get('s&a'),
                'indicator': SnATradeIndicator,
            }
        }
        up_down_multipliers = {
            'long_tp_multiplier': settings.get('long_tp_multiplier'), 
            'long_sl_multiplier': settings.get('long_sl_multiplier'), 
            'short_tp_multiplier': settings.get('short_tp_multiplier'),  
            'short_sl_multiplier': settings.get('short_sl_multiplier'), 

        }
        strategy = Strategy(
            dataframe,
            indicators=indicators,
            **up_down_multipliers,
        )

        backtester = Backtester(
            initial_balance=settings.get('initial_balance') or 10000,
            strategy=strategy,
            limit_fee=settings.get('limit_fee') or 0.012,
            market_fee=settings.get('market_fee') or 0.03,
            historical_quotes=dataframe,
        )
        # logging.info(f"{backtester.current_balance=}")
        statistics = backtester.backtest()
        # statistics = backtester.calculate_statistics()
        print(f"{statistics=}")
        logging.info(f"{statistics=}")
            # pprint(backtester.trade_list)
            # logging.info(f"{backtester.current_balance=}")
            # logging.info(f"{backtester.trade_list=}")
        # except Exception as e:
        #     print(f"{e=}")
        #     logging.warning(f"{e=}")
            # exit()
        # bot = Bot()

        # while True:
        #     signals = [Trade(**signal) for signal in strategy.get_signals()]
        #     bot.trades.extend(signals)
        #     bot.monitor()
    # except Exception as e:
    #     print(e)

main()
