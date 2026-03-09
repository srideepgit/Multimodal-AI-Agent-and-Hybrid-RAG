import pytest

from app.tools.calculator import CalculatorTool
from app.response.context_builder import ContextBuilder
from app.response.confidence import ConfidenceScorer
from app.response.validator import ResponseValidator


@pytest.fixture
def calculator():
    """
    Calculator fixture.
    """
    return CalculatorTool()


@pytest.fixture
def context_builder():
    """
    Context builder fixture.
    """
    return ContextBuilder()


@pytest.fixture
def confidence_scorer():
    """
    Confidence scorer fixture.
    """
    return ConfidenceScorer()


@pytest.fixture
def response_validator():
    """
    Response validator fixture.
    """
    return ResponseValidator()