import pandas as pd

from samay.strategy.base import Strategy


class BollingerBandsQQQ(Strategy):
    name = "bollinger-bands-qqq"
    description = "Buy QQQ when price touches lower Bollinger Band (−2σ), sell at upper band (+2σ)"
    author = "samay-core"
    version = "1.0.0"

    WINDOW = 20
    NUM_STD = 2.0

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        close = data["close"]

        mid = close.rolling(self.WINDOW).mean()
        std = close.rolling(self.WINDOW).std()
        upper = mid + self.NUM_STD * std
        lower = mid - self.NUM_STD * std

        signals = pd.Series(0, index=data.index, dtype=int)

        for i in range(self.WINDOW, len(close)):
            if close.iloc[i] <= lower.iloc[i]:
                signals.iloc[i] = 1
            elif close.iloc[i] >= upper.iloc[i]:
                signals.iloc[i] = -1

        return signals
