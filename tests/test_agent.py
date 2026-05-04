import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from samay.agent import _description_to_slug, _load_skills


def test_description_to_slug_basic():
    slug = _description_to_slug("momentum on Nifty 50")
    assert "momentum" in slug
    assert " " not in slug


def test_description_to_slug_special_chars():
    slug = _description_to_slug("RSI strategy: buy < 30!")
    assert " " not in slug
    assert "!" not in slug


def test_description_to_slug_max_length():
    long_desc = "a" * 200
    slug = _description_to_slug(long_desc)
    assert len(slug) <= 50


def test_load_skills_momentum():
    skills = _load_skills("momentum strategy on top 10 stocks")
    assert isinstance(skills, str)


def test_load_skills_india():
    skills = _load_skills("nifty 50 mean reversion india")
    assert isinstance(skills, str)


def test_load_skills_always_loads_risk_management():
    skills = _load_skills("some random strategy description")
    assert isinstance(skills, str)


@patch("anthropic.Anthropic")
def test_generate_strategy_calls_api(MockAnthropic):
    import os
    os.environ["ANTHROPIC_API_KEY"] = "test-key"

    mock_client = MagicMock()
    MockAnthropic.return_value = mock_client

    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="""from samay.strategy.base import Strategy
import pandas as pd

class TestStrategy(Strategy):
    name = "test"
    description = "test strategy"
    author = "test"
    version = "0.1.0"

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        return pd.Series(0, index=data.index)
""")]
    mock_client.messages.create.return_value = mock_message

    from samay.agent import generate_strategy
    filepath, strategy_class = generate_strategy("simple buy and hold")

    assert strategy_class is not None
    assert mock_client.messages.create.called
