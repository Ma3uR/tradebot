from typing import Union
from dataclasses import dataclass, field
import hashlib
from datetime import datetime
from typing import Literal
from pandas import DataFrame, Timestamp

@dataclass
class Trade:
    symbol: str
    side: Literal["SHORT", "LONG"]
    entry_order_type: Literal["MARKET", "LIMIT"]
    entry_order_price: float
    entry_order_id: Union[int, str, None] = None
    stop_loss_id: Union[int, str, None] = None
    take_profit_id: Union[int, str, None] = None
    tp_order_price: float = 0.0
    sl_order_price: float = 0.0
    trade_status: Literal["NEW", "PLACED", "OPENED", "CLOSED", "FAILED", "REJECTED"] = "NEW"
    trade_results: float = 0.0
    total_order: float = 0.0
    fee_paid: float = 0.0
    balance: float = 0.0
    current_balance: float = 0.0
    current_position: int = 0
    comment: str = ""
    trade_quantity: Union[int, float] = field(default=0)  # Default value added
