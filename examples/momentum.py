"""
Momentum Strategy Example
=========================
Ranks stocks by M-month return and holds the top N.
Rebalances weekly.

Research shows momentum works well with:
- 3-12 month lookback (1-month often reverses)
- Weekly or monthly rebalance
- Top 10-20% of universe

Warning: momentum crashes hard after bear markets. Always check
2008, 2020 performance. Model realistic transaction costs.
"""

import pandas as pd
from samay.strategy.base import Strategy


class MomentumStrategy(Strategy):
    name = "momentum-weekly"
    description = "Top momentum weekly rebalance, 3-month lookback"
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
