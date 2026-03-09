import pytest

from pydantic import ValidationError

from app.response.validator import (
    ResponseValidator,
)


def test_valid_response():

    validator = ResponseValidator()

    response = {

        "answer": "Employees receive 20 days leave.",

        "sources": [],

        "confidence": 0.95,

    }

    validated = validator.validate(response)

    assert validated.answer == "Employees receive 20 days leave."

    assert validated.confidence == 0.95


def test_invalid_response():

    validator = ResponseValidator()

    response = {

        "sources": [],

        "confidence": 0.95,

    }

    with pytest.raises(ValidationError):

        validator.validate(response)