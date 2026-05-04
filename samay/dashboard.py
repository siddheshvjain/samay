import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

from samay.agent import Agent
from samay.backtest.engine import BacktestConfig, BacktestEngine
from samay.data.yfinance_provider import YFinanceProvider
from samay.strategy.base import Strategy

load_dotenv()

st.set_page_config(page_title="samay", layout="wide", initial_sidebar_state="expanded")
st.markdown(
    """
    <style>
        .metric-container { text-align: center; padding: 10px; }
        .negative { color: #d32f2f; }
        .positive { color: #388e3c; }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_all_strategies() -> list[dict]:
    """Load all community strategies from strategies/ directory."""
    strategies_dir = Path(__file__).parent.parent / "strategies"
    strategies = []

    for category_dir in strategies_dir.iterdir():
        if not category_dir.is_dir() or category_dir.name == "__pycache__":
            continue
        for strategy_dir in category_dir.iterdir():
            if not strategy_dir.is_dir() or strategy_dir.name == "__pycache__":
                continue
            metadata_file = strategy_dir / "metadata.json"
            results_file = strategy_dir / "results.json"
            if metadata_file.exists() and results_file.exists():
                with open(metadata_file) as f:
                    metadata = json.load(f)
                with open(results_file) as f:
                    results = json.load(f)
                strategies.append({**metadata, **results, "id": f"{category_dir.name}/{strategy_dir.name}"})

    return strategies


def run_community_backtest(strategy_id: str, capital: float = 100000) -> object:
    """Import and run a community strategy dynamically."""
    parts = strategy_id.split("/")
    category, slug = parts[0], parts[1]

    strategy_file = (
        Path(__file__).parent.parent / "strategies" / category / slug / "strategy.py"
    )

    with open(strategy_file) as f:
        code = f.read()

    exec_globals = {}
    exec(code, exec_globals)

    strategy_class = None
    for name, obj in exec_globals.items():
        if isinstance(obj, type) and issubclass(obj, Strategy) and obj != Strategy:
            strategy_class = obj
            break

    if not strategy_class:
        st.error(f"Could not find Strategy subclass in {strategy_file}")
        return None

    strategy = strategy_class()
    tickers = [strategy_id.split("/")[1]]
    metadata_file = Path(__file__).parent.parent / "strategies" / strategy_id / "metadata.json"
    with open(metadata_file) as f:
        metadata = json.load(f)
    tickers = metadata.get("tickers", tickers)

    config = BacktestConfig(
        strategy=strategy,
        tickers=tickers,
        start_date=metadata.get("backtest_from", "2020-01-01"),
        end_date=metadata.get("backtest_to", "2024-01-01"),
        initial_capital=capital,
        commission=0.001,
        slippage=0.0005,
    )

    provider = YFinanceProvider()
    engine = BacktestEngine(config, provider)
    return engine.run()


def compute_drawdown(equity: pd.Series) -> pd.Series:
    """Compute drawdown from equity curve."""
    running_max = equity.cummax()
    return (equity / running_max - 1) * 100


def monthly_returns(equity: pd.Series) -> pd.DataFrame:
    """Compute monthly returns from equity curve."""
    monthly_eq = equity.resample("ME").last()
    returns = monthly_eq.pct_change() * 100
    returns.index = returns.index.to_period("M")
    df = pd.DataFrame({"return": returns})
    df["year"] = df.index.year
    df["month"] = df.index.month
    pivot = df.pivot_table(values="return", index="year", columns="month", aggfunc="first")
    pivot.columns = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    return pivot


def page_leaderboard():
    """Page 1: Leaderboard of community strategies."""
    st.title("🏆 Strategy Leaderboard")

    strategies = load_all_strategies()

    if not strategies:
        st.warning("No strategies found.")
        return

    df_data = []
    for s in strategies:
        df_data.append({
            "Strategy": s.get("name", "Unknown"),
            "Region": s.get("region", "").upper(),
            "CAGR %": f"{s.get('cagr_pct', 0):.2f}",
            "Sharpe": f"{s.get('sharpe_ratio', 0):.3f}",
            "Max DD %": f"{s.get('max_drawdown_pct', 0):.2f}",
            "Win Rate %": f"{s.get('win_rate_pct', 0):.2f}",
            "Verified": "✅" if s.get("verified") else "❌",
        })

    df = pd.DataFrame(df_data)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Strategies", len(strategies))
    best_sharpe = max([s.get("sharpe_ratio", 0) for s in strategies])
    col2.metric("Best Sharpe Ratio", f"{best_sharpe:.3f}")
    best_cagr = max([s.get("cagr_pct", 0) for s in strategies])
    col3.metric("Best CAGR", f"{best_cagr:.2f}%")
    avg_wr = sum([s.get("win_rate_pct", 0) for s in strategies]) / len(strategies)
    col4.metric("Avg Win Rate", f"{avg_wr:.2f}%")

    st.subheader("All Strategies")
    st.dataframe(df, use_container_width=True, hide_index=True)


def page_backtest_viewer():
    """Page 2: Backtest a community strategy."""
    st.title("📊 Backtest Viewer")

    strategies = load_all_strategies()
    strategy_names = [s["name"] for s in strategies]

    if not strategy_names:
        st.warning("No strategies found.")
        return

    with st.sidebar:
        st.subheader("Configuration")
        selected_name = st.selectbox("Select Strategy", strategy_names)
        capital = st.number_input("Capital ($)", value=100000, min_value=10000)

        selected = next((s for s in strategies if s["name"] == selected_name), None)
        if selected:
            st.write(f"**Description:** {selected.get('description')}")
            st.write(f"**Tickers:** {', '.join(selected.get('tickers', []))}")

    if st.button("Run Backtest", use_container_width=True):
        with st.spinner("Running backtest..."):
            result = run_community_backtest(selected["id"], capital)

        if result:
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("CAGR", f"{result.metrics['cagr_pct']:.2f}%")
            col2.metric("Sharpe", f"{result.metrics['sharpe_ratio']:.3f}")
            col3.metric("Max DD", f"{result.metrics['max_drawdown_pct']:.2f}%")
            col4.metric("Win Rate", f"{result.metrics['win_rate_pct']:.2f}%")
            col5.metric("# Trades", result.metrics["num_trades"])

            st.subheader("Equity Curve")
            fig_eq = px.line(
                x=result.equity_curve.index,
                y=result.equity_curve.values,
                labels={"x": "Date", "y": "Portfolio Value ($)"},
            )
            fig_eq.update_traces(line_color="#1f77b4")
            st.plotly_chart(fig_eq, use_container_width=True)

            st.subheader("Drawdown")
            dd = compute_drawdown(result.equity_curve)
            fig_dd = px.area(x=dd.index, y=dd.values, labels={"x": "Date", "y": "Drawdown (%)"})
            fig_dd.update_traces(fillcolor="rgba(211, 47, 47, 0.5)", line_color="#d32f2f")
            st.plotly_chart(fig_dd, use_container_width=True)

            st.subheader("Monthly Returns")
            monthly = monthly_returns(result.equity_curve)
            fig_hm = px.imshow(
                monthly,
                labels=dict(x="Month", y="Year", color="Return %"),
                color_continuous_scale="RdYlGn",
                zmin=-10,
                zmax=10,
            )
            st.plotly_chart(fig_hm, use_container_width=True)

            st.subheader("Trade Log")
            st.dataframe(result.trades, use_container_width=True, hide_index=True)


def page_ai_research():
    """Page 3: AI-powered strategy generation."""
    st.title("🤖 AI Strategy Research")

    with st.form("research_form"):
        description = st.text_area(
            "Describe your strategy in plain English:",
            placeholder="e.g., 'Buy SPY when it crosses above its 200-day moving average'",
            height=100,
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            tickers = st.text_input("Tickers (comma-separated):", value="SPY")
        with col2:
            from_date = st.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
        with col3:
            to_date = st.date_input("End Date", value=pd.to_datetime("2024-01-01"))

        col1, col2 = st.columns(2)
        with col1:
            capital = st.number_input("Capital ($)", value=100000, min_value=10000)
        with col2:
            st.write("")
            st.write("")
            submit = st.form_submit_button("Generate & Backtest", use_container_width=True)

    if submit and description:
        with st.spinner("Claude is thinking..."):
            try:
                agent = Agent()
                strategy = agent.generate_strategy(description)

                ticker_list = [t.strip() for t in tickers.split(",")]
                config = BacktestConfig(
                    strategy=strategy,
                    tickers=ticker_list,
                    start_date=str(from_date),
                    end_date=str(to_date),
                    initial_capital=capital,
                )

                provider = YFinanceProvider()
                engine = BacktestEngine(config, provider)
                result = engine.run()

                col1, col2, col3, col4, col5 = st.columns(5)
                col1.metric("CAGR", f"{result.metrics['cagr_pct']:.2f}%")
                col2.metric("Sharpe", f"{result.metrics['sharpe_ratio']:.3f}")
                col3.metric("Max DD", f"{result.metrics['max_drawdown_pct']:.2f}%")
                col4.metric("Win Rate", f"{result.metrics['win_rate_pct']:.2f}%")
                col5.metric("# Trades", result.metrics["num_trades"])

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Equity Curve")
                    fig_eq = px.line(
                        x=result.equity_curve.index,
                        y=result.equity_curve.values,
                        labels={"x": "Date", "y": "Portfolio Value ($)"},
                    )
                    st.plotly_chart(fig_eq, use_container_width=True)

                with col2:
                    st.subheader("Drawdown")
                    dd = compute_drawdown(result.equity_curve)
                    fig_dd = px.area(x=dd.index, y=dd.values, labels={"x": "Date", "y": "Drawdown %"})
                    fig_dd.update_traces(fillcolor="rgba(211, 47, 47, 0.5)", line_color="#d32f2f")
                    st.plotly_chart(fig_dd, use_container_width=True)

                with st.expander("View Generated Code"):
                    strategy_code = inspect.getsource(strategy.__class__)
                    st.code(strategy_code, language="python")

            except Exception as e:
                st.error(f"Error: {str(e)}")


def page_knowledge():
    """Page 4: Knowledge commons (skills, lessons, graveyard)."""
    st.title("🧠 Knowledge Commons")

    tab1, tab2, tab3 = st.tabs(["📚 Skills", "📖 Lessons", "🪦 Graveyard"])

    base_path = Path(__file__).parent.parent

    with tab1:
        st.subheader("Skills")
        skills_dir = base_path / "skills"
        skill_files = sorted(skills_dir.rglob("SKILL.md"))

        if skill_files:
            selected_skill = st.selectbox(
                "Select Skill", [f.parent.name for f in skill_files]
            )
            for skill_file in skill_files:
                if skill_file.parent.name == selected_skill:
                    with open(skill_file) as f:
                        st.markdown(f.read())
        else:
            st.info("No skills found.")

    with tab2:
        st.subheader("Lessons")
        lessons_dir = base_path / "lessons"
        lesson_files = sorted(lessons_dir.rglob("*.md"))

        if lesson_files:
            selected_lesson = st.selectbox(
                "Select Lesson", [f.stem for f in lesson_files if f.name != "README.md"]
            )
            for lesson_file in lesson_files:
                if lesson_file.stem == selected_lesson:
                    with open(lesson_file) as f:
                        st.markdown(f.read())
        else:
            st.info("No lessons found.")

    with tab3:
        st.subheader("🪦 Graveyard (Failed Strategies)")
        graveyard_dir = base_path / "graveyard"
        graveyard_files = sorted(graveyard_dir.rglob("*.md"))

        if graveyard_files:
            selected_grave = st.selectbox(
                "Select Failed Strategy", [f.stem for f in graveyard_files if f.name != "README.md"]
            )
            for grave_file in graveyard_files:
                if grave_file.stem == selected_grave:
                    with open(grave_file) as f:
                        st.markdown(f.read())
        else:
            st.info("No failed strategies documented yet.")


if __name__ == "__main__":
    import inspect

    st.sidebar.image(
        "https://img.shields.io/badge/samay-alpha-orange",
        width=200,
    )

    page = st.sidebar.radio(
        "Navigate",
        ["🏆 Leaderboard", "📊 Backtest Viewer", "🤖 AI Research", "🧠 Knowledge Commons"],
    )

    if page == "🏆 Leaderboard":
        page_leaderboard()
    elif page == "📊 Backtest Viewer":
        page_backtest_viewer()
    elif page == "🤖 AI Research":
        page_ai_research()
    else:
        page_knowledge()
