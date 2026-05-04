from samay.brokers.base import BrokerAdapter


class IBKRAdapter(BrokerAdapter):
    def __init__(self, port: int = 7497, client_id: int = 1):
        from ib_insync import IB

        self._ib = IB()
        self._ib.connect("127.0.0.1", port, clientId=client_id)
        self._port = port

    def get_account(self) -> dict:
        values = self._ib.accountValues()
        account_data = {}
        for v in values:
            if v.tag in ("NetLiquidation", "TotalCashValue", "BuyingPower"):
                account_data[v.tag] = float(v.value)
        return account_data

    def get_positions(self) -> list[dict]:
        positions = self._ib.positions()
        return [
            {
                "ticker": p.contract.symbol,
                "qty": p.position,
                "avg_entry_price": p.avgCost,
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
        from ib_insync import MarketOrder, Stock

        contract = Stock(ticker, "SMART", "USD")
        action = "BUY" if side == "buy" else "SELL"
        order = MarketOrder(action, qty)
        trade = self._ib.placeOrder(contract, order)
        return {
            "order_id": trade.order.orderId,
            "ticker": ticker,
            "qty": qty,
            "side": side,
            "status": trade.orderStatus.status,
        }

    def get_orders(self) -> list[dict]:
        trades = self._ib.trades()
        return [
            {
                "order_id": t.order.orderId,
                "ticker": t.contract.symbol,
                "qty": t.order.totalQuantity,
                "side": t.order.action.lower(),
                "status": t.orderStatus.status,
            }
            for t in trades
        ]

    def is_paper(self) -> bool:
        return self._port == 7497

    def disconnect(self):
        self._ib.disconnect()
