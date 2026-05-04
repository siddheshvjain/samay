---
name: india-specific
description: Use this skill when trading Indian equities (NSE/BSE), Nifty indices, or strategies specific to India
tags: [india, nse, bse, nifty, sensex, fii, dii, strate-costs]
contributed_by: samay-core
---

# Indian Markets

## Data Access

**yfinance suffixes:**
- NSE (National Stock Exchange): `.NS` suffix
- Examples: `RELIANCE.NS`, `TCS.NS`, `INFY.NS`

**Key indices:**
- **Nifty 50** — Top 50 companies (^NSEI) — market-cap-weighted
- **Nifty Midcap 100** — Mid-cap universe (~50–500 crore market cap)
- **Nifty Smallcap 100** — Small-caps (< 50 crore, very volatile)
- **Sensex** — BSE's equivalent to Nifty 50 (^BSESN)

**Tip:** Nifty 50 and Sensex overlap > 80%; use Nifty for better historical data.

## Market Structure

**T+2 settlement** — You buy on Monday, money moves Wednesday. You can't short-sell easily (BTST rules are complex).

**Circuit breakers:**
- 10% limit up/down on single stock: trading halts 15 min
- 20% market-wide: halt ~2 hours
- Volatility explodes on bad news (e.g., HDFC merger day: 500 bps move)

**Lot sizes** — Contracts trade in standardized lots:
- Nifty 50: 75 shares/contract
- Index options: 100 shares
- For backtesting: 1 share minimum (yfinance handles this)

## Key Sectors & Patterns

**IT sector** — TCS, Infosys, Wipro
- Dollar-dependent (earnings in $, costs in ₹)
- Strong 2003–2007, again 2013–2021, weak 2022–2023
- Momentum-driven (buy TCS if it's up 20% YoY)

**Banks** — HDFC Bank, ICICI, Axis, Kotak
- RBI policy sensitive (rate hikes kill valuations)
- Dividend-yielders; typically 2–3% yield
- Value trap risk: cheap can be cheaper (if RBI hikes rates)

**Pharma** — Cipla, Dr. Reddy's, Aurobindo, Lupin
- USD-denominated exports (dollar strength = tailwind)
- Regulatory risk from FDA, European approvals
- Generic drugs = commoditized (price wars common)

**Auto & Ancillaries** — Maruti, Tata Motors, Hero
- Cyclical; booms in rate-cut cycles, crashes in rate-hike cycles
- GST sensitive (2017 implementation caused crash)

**Mid-caps** — L&T, Bajaj Auto, Godrej, Kite Pharma
- Lower analyst coverage (less efficient pricing)
- Momentum works better here than large-caps
- Higher volatility (30–40% annualized vs. 18% for Nifty 50)

## FII/DII Flows

Foreign Institutional Investors (FII) vs. Domestic Institutional Investors (DII).

- **FII inflows** (foreign buying): Nifty rallies
- **FII outflows** (foreign selling): Nifty crashes
- DII (domestic) often comes in on FII weakness (stabilizing force)

**Signal:**
- FII selling > $100M/day — bearish, watch out
- FII buying > $100M/day — bullish tailwind

## Transaction Costs

Higher than US. Budget realistically:

- **Brokerage**: flat ₹20 per trade (~0.02% for ₹100k trade)
- **STT (Securities Transaction Tax)**: 0.1% on sells only (not on buys)
- **GST**: 18% on brokerage fee
- **Effective cost per round-trip**: ~0.3–0.5%

**Example:**
- Buy 100 shares @ ₹1000 = ₹100,000
- Sell 100 shares @ ₹1050 = ₹105,000
- STT on sell: ₹105,000 * 0.1% = ₹105
- Brokerage: ₹20 * 2 = ₹40
- GST on brokerage: ₹40 * 18% = ₹7.20
- Total cost: ₹152.20 (~0.15%)
- Net profit: ₹5,000 - ₹152 = ₹4,848 (4.7% instead of 5%)

## Seasonal Patterns

- **April–June**: fiscal year end; tax-driven selling (year-end)
- **July–September**: monsoon (agricultural sentiment), FII summer holidays (low volume)
- **October–November**: Diwali rally (traditional buying)
- **December–March**: year-end buying, new fiscal year (April) enthusiasm

## What to check in backtests

1. **Sector concentration** — Does the strategy buy only IT or banks? If so, you're not diversified.

2. **Mid-cap vs. large-cap** — Nifty Mid 100 is more volatile but offers better momentum signals. Test on both.

3. **FII flows** — If your strategy only works in FII inflow periods, it's fragile. Ensure it works in outflow periods too.

4. **STT drag** — Explicitly model 0.1% STT on all sells. High-turnover strategies become unprofitable.

5. **Liquidity** — Mid-cap and small-cap stocks can have wide bid-ask spreads. Test with realistic slippage (0.2–0.5% for less liquid names).

## See also

- Lesson: "Momentum works better on Indian mid-caps than large-caps" — empirical evidence
- Strategy: `momentum/nifty-top10` — Example Nifty strategy
- Skill: "Risk management" — Essential for Indian volatility
