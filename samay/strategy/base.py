from abc import ABC, abstractmethod

import pandas as pd


class Strategy(ABC):
    name: str = "unnamed"
    description: str = ""
    author: str = ""
    version: str = "0.1.0"

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Input: OHLCV DataFrame with columns: open, high, low, close, volume
               DatetimeIndex
        Output: pd.Series of signals indexed by date
                1 = buy, -1 = sell, 0 = hold
        """
        pass

    def get_metadata(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "author": self.author,
            "version": self.version,
        }
