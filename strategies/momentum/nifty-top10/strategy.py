import pandas as pd

from samay.strategy.base import Strategy


class NiftyTop10Momentum(Strategy):
    name = "nifty-top10-momentum"
    description = "Top 10 Nifty 50 stocks by 3-month return, weekly rebalance"
    author = "samay-core"
    version = "1.0.0"

    def __init__(self, lookback_days: int = 63):
        self.lookback_days = lookback_days

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        if len(data) < self.lookback_days:
            return pd.Series(0, index=data.index)

        momentum = data["close"].pct_change(self.lookback_days)
        signals = pd.Series(0, index=data.index)
        in_position = False

        for date in data.index:
            if date.weekday() != 4:
                continue
            mom = momentum.get(date) if hasattr(momentum, "get") else momentum.loc[date] if date in momentum.index else None
            if mom is None or pd.isna(mom):
                continue
            if mom > 0 and not in_position:
                signals.loc[date] = 1
                in_position = True
            elif mom <= 0 and in_position:
                signals.loc[date] = -1
                in_position = False

        return signals
