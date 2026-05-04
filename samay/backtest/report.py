import pandas as pd
from rich import box
from rich.console import Console
from rich.table import Table

from samay.backtest.engine import BacktestResult

console = Console()


def print_report(result: BacktestResult):
    console.print()
    console.rule(f"[bold blue]{result.strategy_name}[/bold blue]")

    console.print(f"[dim]Period:[/dim] {result.start_date} → {result.end_date}")
    console.print(f"[dim]Tickers:[/dim] {', '.join(result.tickers)}")
    console.print()

    _print_equity_curve(result.equity_curve)
    console.print()

    _print_metrics(result.metrics)
    console.print()

    if len(result.trades) > 0:
        _print_trades(result.trades)


def _print_equity_curve(equity: pd.Series):
    width = 60
    height = 12

    values = equity.values
    min_val = values.min()
    max_val = values.max()

    if max_val == min_val:
        console.print("[dim]Equity curve: flat[/dim]")
        return

    indices = [int(i * (len(values) - 1) / (width - 1)) for i in range(width)]
    sampled = [values[i] for i in indices]

    chart = []
    for row in range(height):
        line = []
        threshold = max_val - (row / (height - 1)) * (max_val - min_val)
        for val in sampled:
            if val >= threshold:
                line.append("█")
            else:
                line.append(" ")
        chart.append("".join(line))

    initial = values[0]
    final = values[-1]
    color = "green" if final >= initial else "red"

    console.print(f"[{color}]{'─' * (width + 2)}[/{color}]")
    for row in chart:
        console.print(f"[{color}]│{row}│[/{color}]")
    console.print(f"[{color}]{'─' * (width + 2)}[/{color}]")

    start_str = f"${initial:,.0f}"
    end_str = f"${final:,.0f}"
    console.print(f"{start_str:<{width // 2}}{end_str:>{width // 2 + 2}}")


def _print_metrics(metrics: dict):
    table = Table(title="Performance Metrics", box=box.ROUNDED)
    table.add_column("Metric", style="dim")
    table.add_column("Value", justify="right")

    def sharpe_color(v):
        if v >= 1.0:
            return "green"
        elif v >= 0.5:
            return "yellow"
        return "red"

    def drawdown_color(v):
        if abs(v) < 20:
            return "green"
        elif abs(v) < 40:
            return "yellow"
        return "red"

    rows = [
        ("Total Return", f"{metrics.get('total_return_pct', 0):.2f}%", None),
        ("CAGR", f"{metrics.get('cagr_pct', 0):.2f}%", None),
        ("Sharpe Ratio", f"{metrics.get('sharpe_ratio', 0):.3f}", sharpe_color(metrics.get('sharpe_ratio', 0))),
        ("Sortino Ratio", f"{metrics.get('sortino_ratio', 0):.3f}", None),
        ("Max Drawdown", f"{metrics.get('max_drawdown_pct', 0):.2f}%", drawdown_color(metrics.get('max_drawdown_pct', 0))),
        ("Max Drawdown Duration", f"{metrics.get('max_drawdown_duration_days', 0)} days", None),
        ("Calmar Ratio", f"{metrics.get('calmar_ratio', 0):.3f}", None),
        ("Win Rate", f"{metrics.get('win_rate_pct', 0):.2f}%", None),
        ("# Trades", str(metrics.get('num_trades', 0)), None),
        ("Avg Trade Duration", f"{metrics.get('avg_trade_duration_days', 0):.1f} days", None),
        ("Profit Factor", str(metrics.get('profit_factor', 0)), None),
    ]

    for label, value, color in rows:
        if color:
            table.add_row(label, f"[{color}]{value}[/{color}]")
        else:
            table.add_row(label, value)

    console.print(table)


def _print_trades(trades: pd.DataFrame):
    top5 = trades.nlargest(5, "pnl")
    _print_trade_table(top5, "Top 5 Trades by P&L", "green")

    bot5 = trades.nsmallest(5, "pnl")
    _print_trade_table(bot5, "Bottom 5 Trades by P&L", "red")


def _print_trade_table(trades: pd.DataFrame, title: str, color: str):
    table = Table(title=title, box=box.SIMPLE)
    table.add_column("Ticker")
    table.add_column("Entry")
    table.add_column("Exit")
    table.add_column("P&L", justify="right")
    table.add_column("Duration", justify="right")

    for _, row in trades.iterrows():
        pnl_str = f"[{color}]${row['pnl']:,.2f}[/{color}]"
        table.add_row(
            str(row.get("ticker", "")),
            str(row.get("entry_date", ""))[:10],
            str(row.get("exit_date", ""))[:10],
            pnl_str,
            f"{row.get('duration_days', 0)} days",
        )

    console.print(table)
