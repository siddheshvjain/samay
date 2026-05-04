# Quant Skills Library

Mental models. Trading wisdom. Hard-won empirical discoveries.

Skills teach Claude how to generate better strategies by understanding the principles that work.

## Contributing a Skill

Add a file: `skills/{topic}/SKILL.md`

```markdown
---
name: momentum
description: Use this skill when the strategy involves momentum, trend following, or ranking
tags: [momentum, trend, relative-strength]
contributed_by: your_github_username
---

# Skill Title

## What it is
Explain the core concept...

## Key parameters
Important variables or thresholds...

## Known failure modes
When and why this breaks...

## Empirical evidence
What backtests show...

## See also
Links to related skills, lessons, strategies...
```

## Existing Skills

- `momentum/SKILL.md` — Trend-following and ranking strategies
- `mean-reversion/SKILL.md` — Oscillator-based reversals
- `value-investing/SKILL.md` — Fundamental analysis
- `risk-management/SKILL.md` — Position sizing and risk
- `india-specific/SKILL.md` — Indian market quirks and opportunities
