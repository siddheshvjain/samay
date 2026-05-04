---
name: Trend-Following
description: Momentum and trend-following strategies using moving averages, breakouts, and channel systems
tags: [trend-following, momentum, moving-average, breakout, channel]
contributed_by: samay-core
contributed_date: "2026-05-04"
---

# Trend-Following

## What it is

Trend-following identifies and trades in the direction of the prevailing market trend. Common approaches include:

- **Moving average crossovers**: Golden cross (fast SMA > slow SMA) signals uptrend entry; death cross signals exit.
- **Breakouts**: Buy when price breaks above a resistance level; sell on breakdown below support.
- **Channel systems**: Trade the slope and reversals within price channels (e.g., Donchian channels, Keltner channels).
- **Time-series momentum**: Rank assets by their past N-month returns and overweight outperformers.

The core principle: "The trend is your friend." Trend-following avoids predicting reversals and instead rides established trends.

## Key parameters

- **Lookback period** (20–200 days): Longer lookbacks capture macro trends but lag entry/exit; shorter ones are more responsive but prone to whipsaws.
- **Rebalance frequency** (daily, weekly, monthly): How often signals update. Monthly rebalancing suits portfolio rotation; daily suits liquid single-stock systems.
- **Crossover thresholds**: For moving average crossovers, confirm with a second filter (e.g., price above/below a longer SMA) to reduce false signals.
- **Stop-loss and profit-taking levels**: Essential in trend-following; a hard stop at -5% to -10% per position limits outsized losses from whipsaws.

## Known failure modes

- **Choppy/sideways markets**: In range-bound environments (e.g., 2015, parts of 2023), trend-following generates constant false signals and chops up capital in commissions/slippage.
- **Whipsaws on reversals**: A rapid trend reversal can catch trend-followers at the worst time—entering near the peak of an old trend.
- **Lag in signal generation**: Moving average crossovers lag the actual reversal by definition. By the time a death cross forms, the trend may already be reversing.
- **Over-optimization**: Tuning lookback and rebalance periods on historical data often leads to curve-fitting and poor out-of-sample performance.
- **High turnover cost**: Frequent rebalancing incurs commissions, slippage, and (in some regions) transaction taxes that erode returns.

## Empirical evidence

- **Moskowitz, Ooi, and Pedersen (2012)**: "Time Series Momentum" (AQR Research). Shows that time-series momentum (past 12-month returns predict next month) outperforms buyand-hold with a Sharpe ratio ~1.0 globally across equity indices, FX, commodities, and bonds.
- **AQR Managed Futures Strategy**: Uses multi-asset trend-following (50/200 SMA on stocks, FX, commodities) with positive returns in crisis periods (2008, 2020) when buy-and-hold breaks down.
- **Faber (2007), "Ivy Portfolio"**: Simple 200-day SMA rule on large-cap equities improves risk-adjusted returns and reduces drawdowns vs. buy-and-hold.

## See also

- `skills/momentum/SKILL.md` — Shorter-term relative-strength momentum vs. absolute trend-following.
- `skills/risk-management/SKILL.md` — Position sizing and stops critical in trend-following.
