import pandas as pd

from samay.strategy.base import Strategy


class GoldenCrossSPY(Strategy):
    name = "golden-cross-spy"
    description = "Buy SPY on 50/200 SMA golden cross, sell on death cross"
    author = "samay-core"
    version = "1.0.0"

    FAST = 50
    SLOW = 200

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        close = data["close"]

        fast_sma = close.rolling(self.FAST).mean()
        slow_sma = close.rolling(self.SLOW).mean()

        signals = pd.Series(0, index=data.index, dtype=int)

        for i in range(1, len(close)):
            if fast_sma.iloc[i - 1] <= slow_sma.iloc[i - 1] and fast_sma.iloc[i] > slow_sma.iloc[i]:
                signals.iloc[i] = 1
            elif fast_sma.iloc[i - 1] >= slow_sma.iloc[i - 1] and fast_sma.iloc[i] < slow_sma.iloc[i]:
                signals.iloc[i] = -1

        return signals
