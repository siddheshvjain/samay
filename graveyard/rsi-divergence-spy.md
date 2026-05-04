---
title: RSI divergence on SPY
author: samay-core
date: 2025-01-01
cause_of_death: "Worked 2010–2018, broke completely after 2019"
---

## What it was

**RSI Divergence Strategy:**
- Buy: price makes lower low, but RSI makes higher low (bullish divergence)
- Sell: price makes higher high, but RSI makes lower high (bearish divergence)
- Exit: opposite signal or 20-day stop

**Example:** SPY drops to $250 (lower low), RSI only drops to 35 (higher than previous 32). Signal: bullish divergence → buy.

## Why it looked good (2010–2018)

| Metric | Value |
|--------|-------|
| Backtest Period | 2010–2018 (8 years) |
| CAGR | 14.2% |
| Sharpe | 1.18 |
| Win Rate | 62% |
| Max Drawdown | -18% |
| # Trades | 87 |

The 2010s were a low-volatility bull market with shallow, predictable pullbacks. RSI divergences worked because:
1. Every dip was a buying opportunity (macro tailwind)
2. Mean reversion was strong (price snapped back quickly)
3. Volatility was low (VIX ~15 average)

## Why it died (2019–2024)

When forward-tested on 2019–2024:

| Metric | Value |
|--------|-------|
| CAGR | -2.3% |
| Sharpe | -0.42 |
| Win Rate | 38% |
| Max Drawdown | -47% |

What changed:
1. **Trending markets** — 2020 COVID crash: RSI divergence fired, but SPY crashed 30% anyway. Divergence meant nothing in a downtrend.
2. **Volatility regime** — VIX averaged 25+. Sharp whipsaws; divergence signals fired multiple times during a single decline.
3. **Structural change** — Post-2019, macro headwinds (rate hikes 2021–2022, Fed QT) broke the "all dips are buying opportunities" paradigm.

**Example failure:** March 2020:
- SPY drops 20%, RSI drops to 28
- Signal: divergence firing left and right
- Strategy: keep buying the dip
- Reality: SPY drops another 15% before recovering weeks later

## Post-mortem

The strategy was **regime-dependent.**
- It worked in low-vol bull markets with strong mean reversion
- It broke in high-vol, trending markets

The backtest (2010–2018) was cherry-picked:
- Cherry-picked the best possible decade (ultra-loose Fed, no trade wars, no pandemics)
- Didn't include 2008 (drawdown would have been -60%+)
- Didn't include 2022 (rate hike bear market)

## Lesson

1. **Test multiple regimes** — Bull, bear, sideways, high-vol, low-vol
2. **Out-of-sample is essential** — Train 2010–2018, test 2019–2024. If performance drops >50%, you've overfit
3. **Divergences are weak signals** — Divergence just means the oscillator disagrees with price. It doesn't mean price will reverse
4. **Mean reversion fails in trends** — Don't use mean-reversion strategies in trending markets
5. **Market regime matters** — Momentum rules in 2021, mean reversion in 2018. A strategy must adapt or survive both

## Related

- Skill: "Mean Reversion" → "When it fails" section
- Skill: "Risk Management" → always test worst-case scenarios
- Lesson: "Momentum works better on Indian mid-caps" → also regime/market specific

---

*In the graveyard, even failures have value.*
