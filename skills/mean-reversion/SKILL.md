---
name: mean-reversion
description: Use this skill when the strategy involves mean reversion, RSI, Bollinger Bands, z-score, or oversold/overbought conditions
tags: [mean-reversion, rsi, bollinger-bands, zscore, oscillators]
contributed_by: samay-core
---

# Mean Reversion

## What it is

Mean reversion is the opposite of momentum. Assets that have fallen sharply tend to bounce back, and assets that have risen sharply tend to pull back. It's modeled by oscillators like RSI (Relative Strength Index) or Bollinger Bands.

## Approaches

**RSI (Relative Strength Index)**
- RSI < 30: oversold → potential buy
- RSI > 70: overbought → potential sell
- Period: 14 is standard (can tune 7–21)

**Bollinger Bands**
- Close > 2-sigma upper: overbought → sell
- Close < 2-sigma lower: oversold → buy
- Period: 20-day MA, 2 standard deviations

**Z-score**
- Z = (price - MA) / std_dev
- Z > 2: overbought → sell
- Z < -2: oversold → buy

## When it works

- **Ranging, choppy markets** — When price oscillates between support and resistance
- **Single liquid assets** — SPY, QQQ, major commodities (crude, gold)
- **Daily or weekly timeframes** — Longer timeframes dilute the signal
- **After extreme moves** — The sharper the drop, the more likely a snap-back

## When it fails

**Trending markets** — In a strong uptrend (2017, 2021), an oversold RSI is still in a healthy pullback before resuming higher. Shorting oversold = fighting the trend = losses.

**Crisis periods** — During COVID crash (Mar 2020), RSI stayed < 30 for weeks. Buying every "oversold" signal meant doubling down into a bear market.

**Time-of-day effects** — Intraday mean reversion works better because humans panic-sell then buy back the same day. Overnight, gaps don't revert.

## What to check in backtests

1. **Regime detection** — Is the strategy winning only in sideways markets and losing in trends? If so, add a trend filter (e.g., only trade if MA(50) < MA(200)).

2. **Worst-case losses** — Find the largest single trade loss. If it's 5%+ of capital, the strategy is too aggressive. Mean reversion can fail hard.

3. **Holding period** — How long does it take to exit? If it's holding oversold positions for weeks waiting for recovery, the equity curve will be volatile and drawdowns deep.

4. **Volatility regime** — Low-vol periods (2017) are great for mean reversion. High-vol periods (2022) are terrible. Does the strategy adapt?

## Parameters

**Oversold threshold** — RSI < 30 is common. Some traders use < 25 (more extreme, fewer signals) or < 35 (more aggressive, more noise).

**Overbought threshold** — RSI > 70 is common. Some use > 75 or > 65.

**Holding period** — How long to hold after entry? Sell after N days? Sell on the opposite signal? Let it run?

## Empirical evidence

- **Bondt & Thaler (1985)**: Winner stocks outperform loser stocks over 3–5 years (long-term momentum dominates short-term reversion)
- **Jegadeesh (1990)**: 1-month reversals in stock returns (mean reversion at 1M horizon)
- **Blitz et al. (2011)**: Mean reversion is stronger for value stocks (low P/B) than growth stocks

## See also

- Skill: "Momentum" — The opposite effect
- Strategy: `mean-reversion/rsi-spy` — Example RSI strategy
- Lesson: "Transaction costs matter" — High-frequency mean reversion dies to costs
