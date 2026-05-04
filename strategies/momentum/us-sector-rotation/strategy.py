import pandas as pd

from samay.strategy.base import Strategy


class USSectorRotation(Strategy):
    name = "us-sector-rotation"
    description = "Monthly rotation into SPDR sector ETFs with positive 3-month momentum"
    author = "samay-core"
    version = "1.0.0"

    LOOKBACK = 63
    REBALANCE = 21

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        signals = pd.Series(0, index=data.index, dtype=int)

        close = data["close"]
        momentum = close.pct_change(self.LOOKBACK)

        for i in range(self.REBALANCE, len(close)):
            if i % self.REBALANCE == 0:
                if momentum.iloc[i] > 0:
                    signals.iloc[i] = 1
                else:
                    signals.iloc[i] = -1

        return signals
