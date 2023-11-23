from __future__ import annotations
from pandas import DataFrame
# from ..trade import Trade
from .indicator import ABCIndicator
from abc import ABC, abstractmethod


class ABCStrategy(ABC):
    @abstractmethod
    def __init__(
        self,
        indicators: list[ABCIndicator],
        **kwargs,
    ):
        ...
        
    @abstractmethod
    def get_signals(self, test_data: DataFrame,) -> list[DataFrame]:
        ...
        # signals = []
        # ...
        # return [Trade(**signal) for signal in signals]
