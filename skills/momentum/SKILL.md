---
name: momentum
description: Use this skill when the strategy involves momentum, trend following, relative strength, or return-based ranking
tags: [momentum, trend, relative-strength, ranking]
contributed_by: samay-core
---

# Momentum Investing

## What it is

Momentum is the tendency of assets that have performed well recently to continue performing well in the near future, and vice versa. It's one of the most robustly documented anomalies in finance — it works across assets, geographies, and time periods.

## Key parameters

**Lookback period** — How far back to measure returns?
- 3–12 months: most robust
- 1 month: often reverses (reversal effect is strong at 1M)
- 20+ years: not practical for rebalancing

**Rebalance frequency** — How often to update the ranking?
- Weekly or monthly: good balance of capturing momentum and avoiding whipsaw
- Daily: excessive turnover, kills returns to transaction costs
- Quarterly: works but may miss mean reversions

**Universe size** — Which stocks to pick?
- Top 10–20% by return: strongest signals
- Top 1%: too concentrated, more volatile
- Top 50%: too many non-movers, dilutes effect

## Known failure modes

**Momentum crashes** — After bear markets (2008, 2020), momentum strategies crash hard as reversals kill positions that were underwater. Many strategies fail here.

**High turnover kills returns** — If weekly rebalancing on a 50-stock portfolio, turnover explodes. At 0.1% commission, high-turnover momentum strategies evaporate in live trading.

**Fails in choppy, sideways markets** — When the market ranges rather than trends, momentum whipsaws: buy near the top of ranges, sell near bottoms.

**Concentrated betting** — If only a few stocks drive returns, luck matters more than skill. Diversify the universe.

## What to check in backtests

1. **2008 and 2020 survival** — Did it lose 50%+? If so, it's not robust. The best strategies survive crashes with manageable drawdowns.

2. **Turnover realism** — Count the number of trades per year. Multiply by 2 (each trade has an entry and exit). At 0.1% commission, what's the drag? It should be < 1% CAGR or the strategy isn't net positive.

3. **Out-of-sample test** — Train on 2010–2018, test on 2019–2024. Does it maintain Sharpe? If performance drops >50%, you've overfit.

4. **Rolling Sharpe ratio** — Plot Sharpe ratio year-by-year. Is it consistent? Or does it only work in trending years (2017, 2021) and fail in choppy ones (2015, 2018, 2022)?

5. **Sector concentration** — Does the strategy buy mostly tech in bull markets? If so, it's not momentum; it's just riding mega-cap narratives.

## Empirical evidence

- **Fama & French (2012)**: 17 different stock markets show momentum profits, even after costs.
- **Blitz et al. (2014)**: Momentum works better in higher-volatility regimes and with wider spreads between winners and losers.
- **Arnott et al. (2016)**: Momentum crashes after sharp bear markets. Position size needs to be dynamic.
- **Neffin & Scowcroft (2017)**: Mean reversion of momentum: momentum that outperforms the most tends to underperform next period.

## Common pitfalls

- Assuming momentum always works (it doesn't — see 2001, 2003, 2008 crashes)
- Using 1-month momentum (reversion effect dominates)
- Not accounting for bid-ask spread and market impact
- Ignoring correlation between top movers (they often move together; diversification is lower than you think)
- Rebalancing at the wrong time (if rebalancing on Fridays, you're buying what gapped up, selling what gapped down — wrong direction)

## See also

- Lesson: "Momentum works better on Indian mid-caps than large-caps"
- Skill: "Risk management" — How to size momentum positions safely
- Strategies: `momentum/nifty-top10`, other momentum-based strategies in the registry
