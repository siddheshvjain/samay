from abc import ABC, abstractmethod


class BrokerAdapter(ABC):
    @abstractmethod
    def get_account(self) -> dict:
        """Return account info: balance, buying_power, etc."""
        pass

    @abstractmethod
    def get_positions(self) -> list[dict]:
        """Return list of current positions."""
        pass

    @abstractmethod
    def place_order(
        self,
        ticker: str,
        qty: float,
        side: str,
        order_type: str = "market",
    ) -> dict:
        """Place an order. side: 'buy' or 'sell'."""
        pass

    @abstractmethod
    def get_orders(self) -> list[dict]:
        """Return list of orders."""
        pass

    @abstractmethod
    def is_paper(self) -> bool:
        """Returns True if this is a paper trading connection."""
        pass
