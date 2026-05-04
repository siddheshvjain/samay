import importlib.util
import json
from pathlib import Path

import typer
from dotenv import load_dotenv
from rich import box
from rich.console import Console
from rich.table import Table

load_dotenv()

app = typer.Typer(
    name="samay",
    help="Decentralized quant research for everyone.",
    no_args_is_help=True,
)
console = Console()

_last_result_path = Path.home() / ".samay" / "last_result.json"


def _save_last_result(result_dict: dict):
    _last_result_path.parent.mkdir(parents=True, exist_ok=True)
    clean = {k: v for k, v in result_dict.items() if isinstance(v, (str, int, float, list, dict, bool, type(None)))}
    _last_result_path.write_text(json.dumps(clean, indent=2))


def _load_last_result() -> dict | None:
    if _last_result_path.exists():
        return json.loads(_last_result_path.read_text())
    return None


@app.command()
def research(
    description: str = typer.Argument(..., help="Plain English strategy description"),
    from_date: str = typer.Option("2018-01-01", "--from", help="Start date (YYYY-MM-DD)"),
    to_date: str = typer.Option("2024-01-01", "--to", help="End date (YYYY-MM-DD)"),
    tickers: str = typer.Option("SPY", "--tickers", help="Comma-separated tickers"),
):
    """Generate a strategy from plain English, run backtest, print report."""
    from samay.agent import generate_strategy
    from samay.backtest.engine import BacktestConfig, BacktestEngine
    from samay.backtest.report import print_report

    ticker_list = [t.strip() for t in tickers.split(",")]

    try:
        strategy_path, strategy_class = generate_strategy(description)
        strategy = strategy_class()

        config = BacktestConfig(
            strategy=strategy,
            tickers=ticker_list,
            start_date=from_date,
            end_date=to_date,
        )

        console.print("[dim]Running backtest...[/dim]")
        engine = BacktestEngine(config)
        result = engine.run()

        print_report(result)

        _save_last_result({
            "strategy_name": result.strategy_name,
            "strategy_path": strategy_path,
            "tickers": result.tickers,
            "start_date": result.start_date,
            "end_date": result.end_date,
            "metrics": result.metrics,
        })

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def backtest(
    strategy_path: str = typer.Argument(..., help="Path to strategy.py"),
    from_date: str = typer.Option("2018-01-01", "--from", help="Start date"),
    to_date: str = typer.Option("2024-01-01", "--to", help="End date"),
    tickers: str = typer.Option("SPY", "--tickers", help="Comma-separated tickers"),
    capital: float = typer.Option(100_000.0, "--capital", help="Initial capital"),
):
    """Run a strategy file directly against historical data."""
    from samay.backtest.engine import BacktestConfig, BacktestEngine
    from samay.backtest.report import print_report
    from samay.strategy.base import Strategy

    path = Path(strategy_path)
    if not path.exists():
        console.print(f"[red]File not found:[/red] {strategy_path}")
        raise typer.Exit(1)

    spec = importlib.util.spec_from_file_location("user_strategy", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    strategy_class = None
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, Strategy) and obj is not Strategy:
            strategy_class = obj
            break

    if strategy_class is None:
        console.print("[red]No Strategy subclass found in file.[/red]")
        raise typer.Exit(1)

    ticker_list = [t.strip() for t in tickers.split(",")]
    strategy = strategy_class()

    config = BacktestConfig(
        strategy=strategy,
        tickers=ticker_list,
        start_date=from_date,
        end_date=to_date,
        initial_capital=capital,
    )

    console.print(f"[dim]Running backtest for {strategy.name}...[/dim]")
    engine = BacktestEngine(config)
    result = engine.run()
    print_report(result)

    _save_last_result({
        "strategy_name": result.strategy_name,
        "strategy_path": str(path.absolute()),
        "tickers": result.tickers,
        "start_date": result.start_date,
        "end_date": result.end_date,
        "metrics": result.metrics,
    })


@app.command()
def report():
    """Show results of last backtest."""
    data = _load_last_result()
    if data is None:
        console.print("[yellow]No backtest results found. Run 'samay research' or 'samay backtest' first.[/yellow]")
        raise typer.Exit(1)

    table = Table(title=f"Last Backtest: {data.get('strategy_name', 'Unknown')}", box=box.ROUNDED)
    table.add_column("Metric")
    table.add_column("Value", justify="right")

    metrics = data.get("metrics", {})
    for k, v in metrics.items():
        table.add_row(k.replace("_", " ").title(), str(v))

    console.print(f"[dim]Tickers:[/dim] {', '.join(data.get('tickers', []))}")
    console.print(f"[dim]Period:[/dim] {data.get('start_date')} → {data.get('end_date')}")
    console.print()
    console.print(table)


@app.command()
def paper(
    broker: str = typer.Option("alpaca", "--broker", help="Broker: alpaca, zerodha"),
    strategy_path_override: str = typer.Option(None, "--strategy", help="Override strategy path"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without placing orders"),
):
    """Paper trade the last backtested strategy."""
    from samay.brokers.alpaca import AlpacaAdapter
    from samay.brokers.zerodha import ZerodhaAdapter
    from samay.paper import PaperTrader
    from samay.strategy.base import Strategy

    last_result = _load_last_result()
    if last_result is None:
        console.print(
            "[red]No backtest results found.[/red] Run 'samay research' or 'samay backtest' first."
        )
        raise typer.Exit(1)

    strategy_path = strategy_path_override or last_result.get("strategy_path")
    if not strategy_path:
        console.print(
            "[red]Strategy path not found in last result.[/red] Run 'samay research' or 'samay backtest' again."
        )
        raise typer.Exit(1)

    path = Path(strategy_path)
    if not path.exists():
        console.print(f"[red]Strategy file not found:[/red] {strategy_path}")
        raise typer.Exit(1)

    spec = importlib.util.spec_from_file_location("user_strategy", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    strategy_class = None
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, Strategy) and obj is not Strategy:
            strategy_class = obj
            break

    if strategy_class is None:
        console.print("[red]No Strategy subclass found in strategy file.[/red]")
        raise typer.Exit(1)

    strategy = strategy_class()
    tickers = last_result.get("tickers", [])

    if broker == "alpaca":
        adapter = AlpacaAdapter(paper=True)
    elif broker == "zerodha":
        adapter = ZerodhaAdapter()
    else:
        console.print(f"[red]Unknown broker:[/red] {broker}")
        raise typer.Exit(1)

    console.print(f"[dim]Trading {strategy.name} via {broker}...[/dim]")
    if dry_run:
        console.print("[yellow]DRY RUN[/yellow] — no orders will be placed")

    trader = PaperTrader(strategy, adapter, tickers)

    try:
        orders = trader.run_once(dry_run=dry_run)

        if orders:
            table = Table(title="Orders Placed", box=box.ROUNDED)
            table.add_column("Ticker")
            table.add_column("Qty", justify="right")
            table.add_column("Side")
            table.add_column("Action")
            for order in orders:
                table.add_row(
                    order.get("ticker", "?"),
                    str(order.get("qty", "?")),
                    order.get("side", "?"),
                    order.get("action", "?"),
                )
            console.print(table)
        else:
            console.print("[dim]No orders placed (no signals or already in position).[/dim]")

        status = trader.status()
        account = status["account"]

        console.print()
        console.print("[bold]Account Status[/bold]")
        console.print(f"  Equity: ${account.get('equity', account.get('portfolio_value', 0)):,.2f}")
        console.print(f"  Cash: ${account.get('cash', account.get('available_cash', 0)):,.2f}")

        if status["positions"]:
            console.print()
            pos_table = Table(title="Open Positions", box=box.ROUNDED)
            pos_table.add_column("Ticker")
            pos_table.add_column("Qty", justify="right")
            pos_table.add_column("Entry Price", justify="right")
            pos_table.add_column("Current Price", justify="right")
            for pos in status["positions"]:
                pos_table.add_row(
                    pos.get("ticker", "?"),
                    str(pos.get("qty", "?")),
                    f"${pos.get('avg_entry_price', pos.get('last_price', 0)):.2f}",
                    f"${pos.get('current_price', pos.get('last_price', 0)):.2f}",
                )
            console.print(pos_table)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def pull(
    strategy_id: str = typer.Argument(..., help="Strategy ID, e.g. momentum/nifty-top10"),
):
    """Pull a community strategy from the registry."""
    strategies_dir = Path(__file__).parent.parent / "strategies"
    strategy_path = strategies_dir / strategy_id

    if not strategy_path.exists():
        console.print(f"[red]Strategy not found:[/red] {strategy_id}")
        raise typer.Exit(1)

    console.print(f"[green]Strategy found:[/green] {strategy_id}")

    meta_path = strategy_path / "metadata.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
        console.print(f"[bold]{meta.get('name', strategy_id)}[/bold]")
        console.print(f"[dim]{meta.get('description', '')}[/dim]")
        console.print(f"[dim]Author:[/dim] {meta.get('author', 'unknown')}")

    results_path = strategy_path / "results.json"
    if results_path.exists():
        results = json.loads(results_path.read_text())
        console.print(
            f"[dim]Sharpe:[/dim] {results.get('sharpe_ratio', 'N/A')}  "
            f"[dim]CAGR:[/dim] {results.get('cagr_pct', 'N/A')}%  "
            f"[dim]Max DD:[/dim] {results.get('max_drawdown_pct', 'N/A')}%"
        )

    console.print(f"\nTo run: samay backtest {strategy_path / 'strategy.py'}")


@app.command()
def publish(
    strategy_file: str = typer.Argument(..., help="Path to strategy.py"),
    name: str = typer.Option(..., "--name", help="Strategy name"),
):
    """Prepare a strategy for contribution."""
    import shutil
    from datetime import date

    from samay.strategy.base import Strategy

    path = Path(strategy_file)
    if not path.exists():
        console.print(f"[red]File not found:[/red] {strategy_file}")
        raise typer.Exit(1)

    spec = importlib.util.spec_from_file_location("pub_strategy", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    strategy_class = None
    for attr in dir(module):
        obj = getattr(module, attr)
        if isinstance(obj, type) and issubclass(obj, Strategy) and obj is not Strategy:
            strategy_class = obj
            break

    if strategy_class is None:
        console.print("[red]No Strategy subclass found.[/red]")
        raise typer.Exit(1)

    s = strategy_class()
    metadata = {
        "name": name,
        "description": s.description or "Add description",
        "author": "your_github_username",
        "version": s.version,
        "asset_class": "equity",
        "region": "us",
        "tickers": ["SPY"],
        "backtest_from": "2018-01-01",
        "backtest_to": "2024-01-01",
        "tags": [],
        "contributed_date": str(date.today()),
    }

    out_dir = Path(f"strategies/{name}")
    out_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy(path, out_dir / "strategy.py")
    (out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))

    console.print(f"[green]Strategy prepared:[/green] {out_dir}/")
    console.print("[dim]Edit metadata.json, then open a PR to contribute.[/dim]")


@app.command()
def serve():
    """Start MCP server so Claude Desktop can use samay as a tool."""
    from samay.server import run_server
    console.print("[green]Starting samay MCP server...[/green]")
    run_server()


@app.command()
def leaderboard():
    """Show top 10 community strategies by Sharpe ratio."""
    strategies_dir = Path(__file__).parent.parent / "strategies"

    if not strategies_dir.exists():
        console.print("[yellow]No strategies directory found.[/yellow]")
        raise typer.Exit(1)

    entries = []
    for results_file in strategies_dir.glob("*/*/results.json"):
        try:
            results = json.loads(results_file.read_text())
            meta_file = results_file.parent / "metadata.json"
            meta = json.loads(meta_file.read_text()) if meta_file.exists() else {}
            entries.append({
                "name": meta.get("name", results_file.parent.name),
                "sharpe": results.get("sharpe_ratio", 0),
                "cagr": results.get("cagr_pct", 0),
                "max_dd": results.get("max_drawdown_pct", 0),
                "region": meta.get("region", ""),
                "verified": results.get("verified", False),
            })
        except Exception:
            continue

    entries.sort(key=lambda x: x["sharpe"], reverse=True)
    top10 = entries[:10]

    table = Table(title="samay Strategy Leaderboard", box=box.ROUNDED)
    table.add_column("#", justify="right")
    table.add_column("Strategy")
    table.add_column("Sharpe", justify="right")
    table.add_column("CAGR %", justify="right")
    table.add_column("Max DD %", justify="right")
    table.add_column("Region")

    for i, entry in enumerate(top10, 1):
        table.add_row(
            str(i),
            entry["name"],
            str(entry["sharpe"]),
            f"{entry['cagr']}%",
            f"{entry['max_dd']}%",
            entry["region"],
        )

    console.print(table)
