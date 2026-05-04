# Community Strategy Registry

The heart of samay. A public commons where quant strategies live forever.

## Contributing a Strategy

### 1. Create the directory

```
strategies/{category}/{strategy-name}/
```

Example: `strategies/momentum/nifty-top10/`

### 2. Write strategy.py

A Python file with a Strategy subclass:

```python
from samay.strategy.base import Strategy
import pandas as pd

class MyStrategy(Strategy):
    name = "my-strategy"
    description = "What this strategy does"
    author = "your_github_username"
    version = "1.0.0"
    
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        # data columns: open, high, low, close, volume
        # Returns: 1 (buy), -1 (sell), 0 (hold)
        signals = pd.Series(0, index=data.index)
        # ... your logic ...
        return signals
```

### 3. Create metadata.json

```json
{
  "name": "my-strategy",
  "description": "Strategy description",
  "author": "your_github_username",
  "version": "1.0.0",
  "asset_class": "equity",
  "region": "us",
  "tickers": ["SPY", "QQQ"],
  "backtest_from": "2018-01-01",
  "backtest_to": "2024-01-01",
  "tags": ["momentum", "weekly"],
  "contributed_date": "2025-01-01"
}
```

### 4. Submit PR

GitHub Actions will auto-verify your strategy and generate `results.json`.

## results.json (AUTO-GENERATED)

Never hand-write this file. CI generates it automatically:

```json
{
  "total_return_pct": 187.3,
  "cagr_pct": 19.4,
  "sharpe_ratio": 1.34,
  "max_drawdown_pct": 23.1,
  "win_rate_pct": 58.2,
  "num_trades": 312,
  "verified": true,
  "verified_at": "2025-01-01T00:00:00Z",
  "samay_version": "0.1.0"
}
```

## Testing Locally

```bash
samay publish path/to/strategy.py --name your-strategy-name
samay backtest strategies/your-strategy-name/strategy.py --from 2018-01-01 --to 2024-01-01 --tickers SPY
```

## Categories

- `momentum/` — Trend-following, relative strength, return-based ranking
- `mean-reversion/` — RSI, Bollinger Bands, z-score
- `value/` — P/E ratios, fundamentals, contrarian
- `arbitrage/` — Cross-market, statistical
- `hybrid/` — Multi-factor, ensemble

## Best Practices

- **Honest results** — Include strategies that failed. They're valuable.
- **Validate assumptions** — Test in/out of sample. Beware overfitting.
- **Document edge cases** — What breaks this strategy?
- **Model realistic costs** — Commission, slippage, taxes matter.
- **Cite your sources** — Link to papers, other strategies, lessons you learned from.
- **Version your strategy** — If you improve it, bump the version.

*Alpha is a public good. Share it.*
