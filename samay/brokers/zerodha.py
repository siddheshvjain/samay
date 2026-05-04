import os

from samay.brokers.base import BrokerAdapter


class ZerodhaAdapter(BrokerAdapter):
    def __init__(self):
        from kiteconnect import KiteConnect

        api_key = os.getenv("KITE_API_KEY")
        access_token = os.getenv("KITE_ACCESS_TOKEN")

        if not api_key or not access_token:
            raise ValueError("KITE_API_KEY and KITE_ACCESS_TOKEN must be set")

        self._kite = KiteConnect(api_key=api_key)
        self._kite.set_access_token(access_token)

    def get_account(self) -> dict:
        profile = self._kite.profile()
        margins = self._kite.margins()
        return {
            "user_id": profile.get("user_id"),
            "available_cash": margins.get("equity", {}).get("available", {}).get("cash", 0),
            "used_margin": margins.get("equity", {}).get("utilised", {}).get("debits", 0),
        }

    def get_positions(self) -> list[dict]:
        positions = self._kite.positions()
        result = []
        for p in positions.get("net", []):
            result.append({
                "ticker": p.get("tradingsymbol"),
                "qty": p.get("quantity"),
                "avg_entry_price": p.get("average_price"),
                "last_price": p.get("last_price"),
                "pnl": p.get("pnl"),
            })
        return result

    def place_order(
        self,
        ticker: str,
        qty: float,
        side: str,
        order_type: str = "market",
    ) -> dict:
        transaction_type = (
            self._kite.TRANSACTION_TYPE_BUY
            if side == "buy"
            else self._kite.TRANSACTION_TYPE_SELL
        )
        kite_order_type = (
            self._kite.ORDER_TYPE_MARKET
            if order_type == "market"
            else self._kite.ORDER_TYPE_LIMIT
        )
        order_id = self._kite.place_order(
            variety=self._kite.VARIETY_REGULAR,
            exchange=self._kite.EXCHANGE_NSE,
            tradingsymbol=ticker,
            transaction_type=transaction_type,
            quantity=int(qty),
            order_type=kite_order_type,
            product=self._kite.PRODUCT_CNC,
        )
        return {"order_id": order_id, "ticker": ticker, "qty": qty, "side": side}

    def get_orders(self) -> list[dict]:
        orders = self._kite.orders()
        return [
            {
                "order_id": o.get("order_id"),
                "ticker": o.get("tradingsymbol"),
                "qty": o.get("quantity"),
                "side": o.get("transaction_type").lower(),
                "status": o.get("status"),
                "order_type": o.get("order_type"),
            }
            for o in orders
        ]

    def is_paper(self) -> bool:
        return False
