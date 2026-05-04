import pandas as pd
import numpy as np
from samay.strategy.base import Strategy


class RSIMeanReversionStrategy(Strategy):
    name = "rsi-mean-reversion"
    description = "RSI-based mean reversion: buy when RSI < 30, sell when RSI > 70"
    author = "samay-core"
    version = "1.0.0"

    def __init__(self, period: int = 14, oversold: float = 30.0, overbought: float = 70.0):
        self.period = period
        self.oversold = oversold
        self.overbought = overbought

    def _compute_rsi(self, series: pd.Series) -> pd.Series:
        delta = series.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.ewm(com=self.period - 1, min_periods=self.period).mean()
        avg_loss = loss.ewm(com=self.period - 1, min_periods=self.period).mean()
        rs = avg_gain / avg_loss.replace(0, float("inf"))
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        rsi = self._compute_rsi(data["close"])
        signals = pd.Series(0, index=data.index)

        in_position = False
        for date in data.index:
            r = rsi.loc[date] if date in rsi.index else None
            if r is None or pd.isna(r):
                continue
            if r < self.oversold and not in_position:
                signals.loc[date] = 1
                in_position = True
            elif r > self.overbought and in_position:
                signals.loc[date] = -1
                in_position = False

        return signals
