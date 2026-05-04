# Lessons from the Market

Empirical discoveries backed by backtests. Shared honestly.

Each lesson is a markdown file documenting something a strategy author learned — what worked, what didn't, and why.

## Contributing a Lesson

Add a file: `lessons/{region}/{title}.md`

```markdown
---
title: What You Discovered
author: your_github_username
date: 2025-01-01
region: universal | us | india | ...
asset_class: equity | crypto | options | ...
tags: [tag1, tag2]
---

## Hypothesis
What you thought would happen...

## Evidence
Backtest results, charts, data...

## Conclusion
What you learned...

## Implications
Why this matters...
```

Examples:
- `lessons/universal/transaction-costs-matter.md` — Costs impact all strategies
- `lessons/india/nifty-momentum-works-midcap.md` — Regional insight
- `lessons/us/spy-mean-reversion-fails-trending.md` — Context-dependent strategy

## Why Lessons?

- Document discoveries so others don't repeat mistakes
- Build collective knowledge about what works and when
- Provide evidence, not opinion
- Make strategies more robust by understanding their limits

*The best traders learn from their failures and share them.*
