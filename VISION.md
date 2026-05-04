# samay — Vision

> **Find alpha. Together.**

## Mission

Make professional-grade quantitative research accessible to everyone — not just hedge funds.

## The problem

Quantitative trading — the practice of using data and code to find market edges — has historically been **gatekept**. The reasons:

- **Knowledge sits in PDFs and Bloomberg terminals**, not on GitHub. A junior analyst at Renaissance learns more in their first week than most retail traders learn in a decade.
- **Backtesting infrastructure is expensive**. Bloomberg charges ~$25k/year. QuantConnect charges per backtest. Building your own takes months.
- **Strategies die in private**. When a hedge fund retires a strategy, the *lesson* — what worked, what broke, why — vanishes with it.
- **AI assistants don't understand finance well**. Asking ChatGPT for a momentum strategy gives you generic code that wouldn't survive a single backtest.

Result: **the gap between professional and retail quant is wider than it has ever been**, even though the data and the compute are now free.

## The bet

Three things changed in 2024–2025:

1. **AI got good enough to write production-quality strategy code** — when given the right context.
2. **Open finance data hit critical mass** — yfinance, Alpaca, IBKR APIs, Indian broker APIs all free or near-free.
3. **The open-source playbook works for hard domains** — Linux, PostgreSQL, Hugging Face all proved that.

samay's bet: combine these into a **knowledge commons + AI agent + execution layer** that lets anyone:

- Describe a strategy in plain English
- Get production-quality code back, grounded in real research
- Backtest it on real data in seconds
- Paper-trade it through real brokers
- Publish what worked (and what didn't) for everyone else

## Who benefits

- **Retail traders** who want a real edge, not Reddit tips.
- **Students** learning quant without a $25k Bloomberg license.
- **Indian markets** specifically — currently underserved by global tools (most US-built platforms have no Nifty support).
- **Researchers** who want to publish reproducible strategies the way ML researchers publish models on Hugging Face.
- **Funds** that want a community-vetted starting point before committing internal R&D budget.

## 3-year vision

**By 2027, samay is to quant research what Hugging Face is to machine learning** — the default place where strategies, data, and knowledge are shared, versioned, and verified.

Specifically:
- 1,000+ community-contributed strategies, CI-verified
- Skills library covering every major asset class and region
- "Graveyard" of failed strategies more valuable than the wins (because we learn more from failure)
- Paper trading bridges to every major broker globally
- AI agents that *cite* the skills and lessons they used — full provenance

## Anti-goals (what we will *not* do)

- **We are not a brokerage.** We integrate with brokers; we never custody money.
- **We are not a signal-selling service.** Strategies are open and free. No one pays for tips.
- **We will not optimize for "outperformance" over honesty.** Failed strategies get equal billing with winners. Survivorship bias is the enemy.
- **We will not gate features behind a paywall.** Sustainability comes from grants, sponsorships, and (eventually) optional managed compute — never from locking down the core.
- **We do not give financial advice.** samay is research infrastructure, not a robo-advisor.

## Operating principles

1. **Reproducibility over flash.** Every backtest result must be re-runnable from a single command.
2. **Cite your sources.** Strategies reference the skills and papers they're built on.
3. **Publish failure.** The graveyard is a feature, not a bug.
4. **Respect the data.** Transaction costs, slippage, and survivorship bias are simulated honestly — we don't sell hopium.
5. **Local-first.** Your strategies, your data, your keys — never on our servers unless you explicitly publish.

---

samay is a Sanskrit word meaning *time, season, opportunity*. In markets, time is everything. We think the time is now.
