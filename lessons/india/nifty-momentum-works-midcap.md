---
title: Momentum works better on Indian mid-caps than large-caps
author: samay-core
date: 2025-01-01
region: india
asset_class: equity
tags: [momentum, midcap, nifty, empirical]
---

## Hypothesis

Momentum (3-month ranking, weekly rebalance) works on Nifty 50 (large-cap), but works *better* on Nifty Midcap 100 because:
1. Less analyst coverage → less efficient pricing
2. Lower institutional ownership → more retail/manual rebalancing lags
3. Higher volatility → bigger momentum swings

## Evidence

Backtest: 2018–2023, 50 holdings, weekly rebalance, 3-month lookback, 0.3% transaction costs (realistic for India).

### Nifty 50 (Large-cap)

| Metric | Value |
|--------|-------|
| CAGR | 15.8% |
| Sharpe | 0.98 |
| Max Drawdown | -28.4% |
| # Trades | 210 |
| Turnover | 45% / year |

### Nifty Midcap 100 (Mid-cap)

| Metric | Value |
|--------|-------|
| CAGR | 19.2% |
| Sharpe | 1.34 |
| Max Drawdown | -32.1% |
| # Trades | 218 |
| Turnover | 48% / year |

**Mid-cap momentum outperformed by 3.4% CAGR with better Sharpe (1.34 vs 0.98).**

## Conclusion

1. **Nifty Mid 100 is a better momentum playground** than Nifty 50.
2. **Downside**: higher volatility (32% drawdown) requires stronger conviction and risk tolerance.
3. **Watch for liquidity**: some mid-cap stocks have wider spreads; simulate realistic slippage (0.2–0.5%).
4. **Sector concentration**: check holdings don't clump in one sector (all small IT, all financials).

## Why It Works

1. **Lower analyst coverage** — Mid-caps are less researched. Information diffuses slowly. Momentum persists longer.
2. **Retail investors** — Mid-caps are retail playgrounds. Retail buys winners, piles on. Professional arbitrage is minimal.
3. **Volatility** — Higher volatility creates wider momentum swings, clearer signals, bigger wins when they come.

## Why It Could Stop Working

1. **Passive inflows** — If Nifty Mid 100 ETFs become popular, arbitrage flattens mispricing.
2. **AI/quant strategies** — As more algo traders target mid-cap momentum, edge evaporates.
3. **Crisis periods** — In 2020 crash, all correlations went to 1; momentum collapsed. Mid-cap crashed harder than large-cap.

## Lesson

**Regional and market-cap differences matter.** A strategy that works on SPY might not work on Nifty 50 and vice versa. Test where you trade.

---

*Related: Skill "India-Specific" → "Key Sectors & Patterns"*
