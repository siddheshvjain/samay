import importlib.util
import os
import re
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.syntax import Syntax

from samay.strategy.base import Strategy

load_dotenv()
console = Console()

SKILLS_DIR = Path(__file__).parent.parent / "skills"
GENERATED_DIR = Path(__file__).parent / "strategy" / "generated"

SYSTEM_PROMPT = """You are a quantitative trading researcher. Generate a Python Strategy class based on the user's description.

The class must inherit from samay.strategy.base.Strategy and implement generate_signals().

Return ONLY the Python code, no explanation, no markdown fences.

The generated code must:
1. Import: from samay.strategy.base import Strategy
2. Import: import pandas as pd
3. Define a class that inherits from Strategy
4. Set name, description, author, version class attributes
5. Implement generate_signals(self, data: pd.DataFrame) -> pd.Series
   - data has columns: open, high, low, close, volume with DatetimeIndex
   - Returns pd.Series of signals: 1=buy, -1=sell, 0=hold, indexed by date
"""


def _load_skills(description: str) -> str:
    desc_lower = description.lower()
    skill_paths = []

    if any(kw in desc_lower for kw in ["momentum", "trend", "relative strength", "ranking"]):
        skill_paths.append(SKILLS_DIR / "momentum" / "SKILL.md")
    if any(kw in desc_lower for kw in ["mean reversion", "rsi", "bollinger", "oversold", "overbought"]):
        skill_paths.append(SKILLS_DIR / "mean-reversion" / "SKILL.md")
    if any(kw in desc_lower for kw in ["india", "nifty", "nse", "bse", "sensex", "reliance"]):
        skill_paths.append(SKILLS_DIR / "india-specific" / "SKILL.md")
    if any(kw in desc_lower for kw in ["value", "p/e", "pe ratio", "fundamental"]):
        skill_paths.append(SKILLS_DIR / "value-investing" / "SKILL.md")

    skill_paths.append(SKILLS_DIR / "risk-management" / "SKILL.md")

    skill_content = ""
    for path in skill_paths:
        if path.exists():
            skill_content += f"\n\n--- SKILL: {path.parent.name} ---\n"
            skill_content += path.read_text()

    return skill_content


def _description_to_slug(description: str) -> str:
    slug = re.sub(r"[^a-z0-9\s-]", "", description.lower())
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = slug[:50]
    return slug or "strategy"


def generate_strategy(description: str) -> tuple[str, type]:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")

    client = anthropic.Anthropic(api_key=api_key)

    skills = _load_skills(description)

    user_message = f"Strategy description: {description}"
    if skills:
        user_message += f"\n\nRelevant quant knowledge:\n{skills}"

    console.print("[dim]Generating strategy with Claude...[/dim]")

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    code = message.content[0].text.strip()

    if code.startswith("```"):
        lines = code.split("\n")
        code = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    slug = _description_to_slug(description)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = GENERATED_DIR / f"{slug}_{timestamp}.py"
    filepath.write_text(code)

    console.print(f"\n[dim]Generated strategy saved to:[/dim] {filepath}")
    console.print()
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
    console.print(syntax)
    console.print()

    strategy_class = _load_strategy_class(code, filepath)
    return str(filepath), strategy_class


def _load_strategy_class(code: str, filepath: Path) -> type:
    spec = importlib.util.spec_from_file_location("generated_strategy", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, Strategy) and obj is not Strategy:
            return obj

    raise ValueError("No Strategy subclass found in generated code")
