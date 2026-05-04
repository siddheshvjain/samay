---
name: value-investing
description: Use this skill when the strategy involves value investing, P/E ratios, fundamentals, or contrarian approaches
tags: [value, pe-ratio, fundamentals, contrarian, dividend]
contributed_by: samay-core
---

# Value Investing

## What it is

Buy stocks trading below their intrinsic value. Sell when they reach fair value or above.

Metrics:
- **P/E ratio** — Earnings yield (earnings / price)
- **P/B ratio** — Book value (assets - liabilities / shares)
- **P/S ratio** — Sales multiple
- **Dividend yield** — Annual dividend / price
- **FCF yield** — Free cash flow / market cap

## Principles

1. **Buy low, sell high** — Literal application; wait for crashes to buy
2. **Margin of safety** — Buy at > 30% discount to fair value
3. **Contrarian** — Ignored stocks, beaten-down sectors are your friends
4. **Long-term** — Holding period: 3–5 years or more

## When it works

- **Mean-reverting markets** — Cheap stocks mean-revert to fair value over years
- **After crashes** — 2009, 2020: value investors who bought had huge gains over next 3 years
- **Cyclical troughs** — Banks in 2008 (cheap), energy stocks (oil crashes), industrials (recession)
- **Neglected stocks** — Small-cap value, international (Europe, Japan)

## When it fails

- **Value traps** — Cheap for a reason; the company is dying (Kodak, Blockbuster, Twitter)
- **Structural shifts** — Disruption kills value (print media, retail, video rental)
- **Growth > value regimes** — 2010–2022 saw massive underperformance of value. Expensive growth (TSLA, NVDA, AMZN) beat cheap value
- **Short-term** — If you need the money in 2 years and the stock takes 5 to recover, you'll be forced to sell at a loss

## What to check in backtests

1. **Holding period** — Are you holding for 3+ years? If you're flipping monthly, it's not value; it's speculation.

2. **Value trap filter** — Add a quality filter (earnings growth, debt ratio, ROE) to avoid cheap stocks that are cheap because they're broken.

3. **Market regime** — Value outperforms growth in low-rate environments (favorable to cheapness). In high rates, growth outperforms. Does your backtest cover both?

4. **Valuation mean reversion speed** — How long until fair value is reached? If it's >10 years, you're trading something for something else.

## Parameters

**Valuation threshold** — How cheap is cheap?
- P/E < 10: very cheap (risk: value trap)
- P/E 10–15: moderately cheap (good risk/reward)
- P/B < 1.0: trading below book value (classic value signal)
- Dividend yield > 4%: good income (utility stocks)

**Quality filter** — To avoid value traps:
- Earnings growth > 0 last 3 years
- ROE > 10%
- Debt / equity < 2.0

## Empirical evidence

- **Fama & French (1992)**: Value (high B/M) outperforms growth by ~5% per year, 1926–1990
- **Blitz et al. (2013)**: Quality + Value = best risk-adjusted returns (combining cheap + high ROE)
- **Arnott et al. (2016)**: Value has underperformed for a decade; mean reversion likely but timing uncertain

## See also

- Skill: "Risk management" — Position sizing for mean-reverting value bets
- Skill: "Momentum" — Momentum and value are often opposites; some blend them
