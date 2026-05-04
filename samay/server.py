import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("samay")
STRATEGIES_DIR = Path(__file__).parent.parent / "strategies"
LAST_RESULT_PATH = Path.home() / ".samay" / "last_result.json"


@mcp.tool()
def run_backtest(description: str, tickers: str, from_date: str, to_date: str) -> str:
    """Run a backtest from a plain English strategy description."""
    from samay.agent import generate_strategy
    from samay.backtest.engine import BacktestConfig, BacktestEngine

    try:
        ticker_list = [t.strip() for t in tickers.split(",")]
        _, strategy_class = generate_strategy(description)
        strategy = strategy_class()

        config = BacktestConfig(
            strategy=strategy,
            tickers=ticker_list,
            start_date=from_date,
            end_date=to_date,
        )

        engine = BacktestEngine(config)
        result = engine.run()

        return json.dumps({
            "strategy_name": result.strategy_name,
            "metrics": result.metrics,
            "tickers": result.tickers,
            "start_date": result.start_date,
            "end_date": result.end_date,
        }, indent=2)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def get_last_results() -> str:
    """Get results of the last backtest."""
    if LAST_RESULT_PATH.exists():
        return LAST_RESULT_PATH.read_text()
    return "No results found. Run a backtest first."


@mcp.tool()
def list_strategies() -> str:
    """List all available community strategies."""
    if not STRATEGIES_DIR.exists():
        return "No strategies directory found."

    strategies = []
    for meta_file in STRATEGIES_DIR.glob("*/*/metadata.json"):
        try:
            meta = json.loads(meta_file.read_text())
            strategies.append({
                "id": f"{meta_file.parent.parent.name}/{meta_file.parent.name}",
                "name": meta.get("name"),
                "description": meta.get("description"),
                "region": meta.get("region"),
            })
        except Exception:
            continue

    return json.dumps(strategies, indent=2)


@mcp.tool()
def search_strategies(query: str) -> str:
    """Search community strategies by keyword."""
    if not STRATEGIES_DIR.exists():
        return "No strategies directory found."

    query_lower = query.lower()
    matches = []

    for meta_file in STRATEGIES_DIR.glob("*/*/metadata.json"):
        try:
            meta = json.loads(meta_file.read_text())
            searchable = json.dumps(meta).lower()
            if query_lower in searchable:
                matches.append({
                    "id": f"{meta_file.parent.parent.name}/{meta_file.parent.name}",
                    "name": meta.get("name"),
                    "description": meta.get("description"),
                    "tags": meta.get("tags", []),
                })
        except Exception:
            continue

    return json.dumps(matches, indent=2) if matches else f"No strategies found matching '{query}'"


@mcp.tool()
def get_leaderboard() -> str:
    """Get top strategies by Sharpe ratio."""
    if not STRATEGIES_DIR.exists():
        return "No strategies directory found."

    entries = []
    for results_file in STRATEGIES_DIR.glob("*/*/results.json"):
        try:
            results = json.loads(results_file.read_text())
            meta_file = results_file.parent / "metadata.json"
            meta = json.loads(meta_file.read_text()) if meta_file.exists() else {}
            entries.append({
                "name": meta.get("name", results_file.parent.name),
                "sharpe_ratio": results.get("sharpe_ratio", 0),
                "cagr_pct": results.get("cagr_pct", 0),
                "max_drawdown_pct": results.get("max_drawdown_pct", 0),
                "region": meta.get("region", ""),
                "verified": results.get("verified", False),
            })
        except Exception:
            continue

    entries.sort(key=lambda x: x["sharpe_ratio"], reverse=True)
    return json.dumps(entries[:10], indent=2)


def run_server():
    print("samay is running. Time to find alpha.")
    mcp.run()
