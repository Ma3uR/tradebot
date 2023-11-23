import os

from zoneinfo import ZoneInfo
from binance.client import Client
from dotenv import load_dotenv
from config.settings import load_settings
from .settings import ROOT_PATH

load_dotenv()

# Program main settings

PROGRAM_NAME = os.getenv('PROGRAM_NAME', 'DAITEX')
PROGRAM_MODE = os.getenv('PROGRAM_MODE', 'trading')
LOCAL_TIMEZONE = ZoneInfo(os.getenv('LOCAL_TIMEZONE', 'Europe/Kyiv'))

# # Telegram Bot settings
# LOGGER_TELEGRAM_API_TOKEN = os.getenv('LOGGER_TELEGRAM_API_TOKEN')
# LOGGER_TELEGRAM_CHAT_ID = int(os.getenv('LOGGER_TELEGRAM_CHAT_ID'))

# Strategy settings
_settings = load_settings()

STRATEGY_NAME = os.getenv('STRATEGY_NAME', 'trade')
SYMBOL = os.getenv('SYMBOL', 'BTCUSDT')

_strategy_settings = _settings.get('strategies', {}).get(STRATEGY_NAME)

BUY_TRIGGER = _strategy_settings.get('buy_trigger')
SELL_TRIGGER = _strategy_settings.get('sell_trigger')

# Backtesting settings
_backtest_settings = _settings.get('backtesting', {})

BACKTEST_PERIOD = _backtest_settings.get('backtest_period')
BACKTEST_INTERVAL = _backtest_settings.get('backtest_interval')
BACKTEST_QUANTITY = _backtest_settings.get('backtest_quantity')
BACKTEST_LIMIT_FEE = _backtest_settings.get('backtest_limit_fee')
BACKTEST_MARKET_FEE = _backtest_settings.get('backtest_market_fee')
BACKTEST_FREQUENCY = _backtest_settings.get('backtest_frequency')
BACKTEST_UNBALANCE_LIMIT = _backtest_settings.get('backtest_unbalance_limit')

# Trading settings
_trading_settings = _settings.get('trading', {})

TRADING_PERIOD = _trading_settings.get('trading_period')
TRADING_INTERVAL = _trading_settings.get('trading_interval')
TRADING_QUANTITY = _trading_settings.get('trading_quantity')
TRADING_FREQUENCY = _trading_settings.get('trading_frequency')
TRADING_UNBALANCE_LIMIT = _trading_settings.get('trading_unbalance_limit')

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BINANCE_CLIENT = Client(API_KEY, API_SECRET)
COMMISSION_RATE = 0.03

# Database settings
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_NAME = os.getenv('POSTGRES_NAME', 'postgres')
