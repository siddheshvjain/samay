
from samay.brokers.base import BrokerAdapter
from samay.data.yfinance_provider import YFinanceProvider
from samay.strategy.base import Strategy


class PaperTrader:
    def __init__(
        self,
        strategy: Strategy,
        broker: BrokerAdapter,
        tickers: list[str],
        lookback_days: int = 252,
    ):
        self.strategy = strategy
        self.broker = broker
        self.tickers = tickers
        self.lookback_days = lookback_days
        self.provider = YFinanceProvider()

    def run_once(self, dry_run: bool = False) -> list[dict]:
        """Generate signals for today and place orders if needed."""
        import math

        orders_placed = []

        for ticker in self.tickers:
            try:
                data = self.provider.get_ohlcv(
                    ticker, lookback_days=self.lookback_days
                )
                signals = self.strategy.generate_signals(data)
                today_signal = signals.iloc[-1] if len(signals) > 0 else 0

                if today_signal == 0:
                    continue

                current_price = data["close"].iloc[-1]
                account = self.broker.get_account()
                positions = {p["ticker"]: p for p in self.broker.get_positions()}

                is_holding = ticker in positions
                current_qty = positions.get(ticker, {}).get("qty", 0)

                if today_signal == 1 and not is_holding:
                    cash = account.get("buying_power", account.get("available_cash", 0))
                    qty = int(math.floor(cash / (len(self.tickers) * current_price)))
                    if qty > 0 and not dry_run:
                        order = self.broker.place_order(ticker, qty, "buy")
                        orders_placed.append({**order, "action": "BUY"})

                elif today_signal == -1 and is_holding:
                    if not dry_run:
                        order = self.broker.place_order(
                            ticker, current_qty, "sell"
                        )
                        orders_placed.append({**order, "action": "SELL"})

            except Exception as e:
                print(f"Error processing {ticker}: {e}")
                continue

        return orders_placed

    def status(self) -> dict:
        """Get account status and positions."""
        return {
            "account": self.broker.get_account(),
            "positions": self.broker.get_positions(),
            "orders": self.broker.get_orders(),
        }
