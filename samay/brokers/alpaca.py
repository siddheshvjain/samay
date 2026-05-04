import os

from samay.brokers.base import BrokerAdapter

PAPER_URL = "https://paper-api.alpaca.markets"


class AlpacaAdapter(BrokerAdapter):
    def __init__(self, paper: bool = True):
        import alpaca_trade_api as tradeapi

        api_key = os.getenv("ALPACA_API_KEY")
        secret_key = os.getenv("ALPACA_SECRET_KEY")

        if not api_key or not secret_key:
            raise ValueError("ALPACA_API_KEY and ALPACA_SECRET_KEY must be set")

        base_url = PAPER_URL if paper else "https://api.alpaca.markets"
        self._api = tradeapi.REST(api_key, secret_key, base_url=base_url)
        self._paper = paper

    def get_account(self) -> dict:
        acc = self._api.get_account()
        return {
            "equity": float(acc.equity),
            "cash": float(acc.cash),
            "buying_power": float(acc.buying_power),
            "portfolio_value": float(acc.portfolio_value),
        }

    def get_positions(self) -> list[dict]:
        positions = self._api.list_positions()
        return [
            {
                "ticker": p.symbol,
                "qty": float(p.qty),
                "avg_entry_price": float(p.avg_entry_price),
                "current_price": float(p.current_price),
                "unrealized_pl": float(p.unrealized_pl),
            }
            for p in positions
        ]

    def place_order(
        self,
        ticker: str,
        qty: float,
        side: str,
        order_type: str = "market",
    ) -> dict:
        order = self._api.submit_order(
            symbol=ticker,
            qty=qty,
            side=side,
            type=order_type,
            time_in_force="day",
        )
        return {
            "id": order.id,
            "ticker": order.symbol,
            "qty": float(order.qty),
            "side": order.side,
            "status": order.status,
        }

    def get_orders(self) -> list[dict]:
        orders = self._api.list_orders()
        return [
            {
                "id": o.id,
                "ticker": o.symbol,
                "qty": float(o.qty),
                "side": o.side,
                "status": o.status,
                "order_type": o.type,
            }
            for o in orders
        ]

    def is_paper(self) -> bool:
        return self._paper
