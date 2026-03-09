from unittest.mock import MagicMock

from app.response.generator import ResponseGenerator


def test_generate():

    llm = MagicMock()

    llm.invoke.return_value = "Enterprise AI"

    generator = ResponseGenerator(llm)

    answer = generator.generate(

        question="What is AI?",

        context="AI Context",

        sql_result=[],

        calculator_result=None,

    )

    assert answer == "Enterprise AI"

    llm.invoke.assert_called_once()