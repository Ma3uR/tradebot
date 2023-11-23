import pandas as pd
import numpy as np
from .strategy import Strategy
from indicators import(
    SnATradeIndicator,
    B2TradeIndicator,
)

class Backtester:
    def __init__(self, strategy, initial_balance:float=100_000.00, fee_percentage:float=2, long_sl_percent_margin=None, short_sl_percent_margin=None, volumes:list=[]):
         
        self.strategy = strategy
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.fee_percentage = fee_percentage / 100
        self.long_sl_percent_margin = long_sl_percent_margin
        self.short_sl_percent_margin = short_sl_percent_margin
        self.positions = []
        self.current_position = None
        self.wins = 0
        self.losses = 0
        self.profit_factor = 0
        self.total_losses = 0
        self.total_profit = 0
        
        # Marga 

        self.volumes = volumes
        self.current_volume_index = 0
        self.consecutive_losses = 0
        
    def backtest(self, test_data):
        signals = self.strategy.get_signals(test_data)

        for index, signal in signals.iterrows():
            if self.current_position:
                # Long
                if self.current_position['side'] == 'long':
                    # В беззбитковий режим
                    
                    if signal['source'] >= self.current_position['take_profit']:
                        self.take_profit()
                    elif signal['source'] <= self.current_position['stop_loss']:
                        self.stop_loss()
                    elif self.long_sl_percent_margin:
                        if self.current_position['entry_price'] == self.current_position['stop_loss']:
                            continue
                        curr_price = signal['source']
                        position_price = self.current_position['entry_price'] 
                        treshold = position_price * (self.long_sl_percent_margin / 100) * (1 + self.fee_percentage)
                        if curr_price >= position_price + treshold:
                            new_sl_price = self.current_position['entry_price'] #* (1 - self.fee_percentage)
                            print(
                                'Long беззбитковий режим:\n'
                                f'було вх ціна: {position_price}\tстоплосс: {self.current_position["stop_loss"]}\n'
                                f'стало поточна ціна: {curr_price}\tстоплосс: {new_sl_price}'
                                )
                            self.current_position['stop_loss'] = new_sl_price
                else:
                    if signal['source'] <= self.current_position['take_profit']:
                        self.take_profit()
                    elif signal['source'] >= self.current_position['stop_loss']:
                        self.stop_loss()
                    elif self.short_sl_percent_margin:
                        if self.current_position['entry_price'] == self.current_position['stop_loss']:
                            continue
                        curr_price = signal['source']
                        position_price = self.current_position['entry_price'] 
                        treshold = position_price * (self.short_sl_percent_margin / 100) * (1 + self.fee_percentage)
                        
                        if curr_price <= position_price - treshold:
                            new_sl_price = self.current_position['entry_price']# *(1 - self.fee_percentage)
                            print(
                                'Short беззбитковий режим:\n'
                                f'було вх ціна: {position_price}\tстоплосс: {self.current_position["stop_loss"]}\n'
                                f'стало поточна ціна: {curr_price}\tстоплосс: {new_sl_price}'
                                )
                            self.current_position['stop_loss'] = new_sl_price
            else:
                if signal['long_conditions']:
                    self.current_position = {
                        'side': 'long',
                        'entry_price': signal['source'],
                        'stop_loss': signal['stop_loss'],
                        'take_profit': signal['take_profit'],
                    }
                if signal['short_conditions']:
                    
                    self.current_position = {
                        'side': 'short',
                        'entry_price': signal['source'],
                        'stop_loss': signal['stop_loss'],
                        'take_profit': signal['take_profit'],
                    }
        self.calculate_statistics()
        return self.balance
    
    def stop_loss(self):
        if self.current_position:
            loss = abs(self.current_position['stop_loss'] - self.current_position['entry_price']) * self.curr_volume * (1 - self.fee_percentage)
            self.balance -= loss
            self.total_losses += loss
            self.losses += 1
            self.current_position = None
            self.consecutive_losses += 1
            # print(f'losses serie: {self.consecutive_losses}, volume: {self.curr_volume}')
    
    def take_profit(self):
        if self.current_position:
            profit = abs(self.current_position['take_profit'] - self.current_position['entry_price']) * self.curr_volume * (1 - self.fee_percentage)
            self.balance += profit
            self.total_profit += profit
            self.wins += 1
            self.current_position = None
            self.consecutive_losses = 0
            
    def calculate_statistics(self):
        total_trades = self.wins + self.losses
        if total_trades > 0:
            self.win_rate = (self.wins / total_trades) * 100
            
            self.profit_factor = ( self.total_profit / self.total_losses )
        else:
            self.win_rate = 0
            self.profit_factor = 0
            
    @property        
    def curr_volume(self):
        if self.volumes:
            return self.volumes[self.consecutive_losses%len(self.volumes)]
        return 1