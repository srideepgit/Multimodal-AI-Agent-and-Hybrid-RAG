from app.response.context_builder import ContextBuilder


class Chunk:

    def __init__(self, text):
        self.text = text


def test_context_builder():

    builder = ContextBuilder()

    state = {
        "retrieved_chunks": [
            Chunk("Chunk One"),
            Chunk("Chunk Two"),
        ],
        "sql_result": [
            {
                "count": 10
            }
        ],
        "calculator_result": 25,
    }

    context = builder.build(state)

    assert "Chunk One" in context
    assert "Chunk Two" in context
    assert "count" in context
    assert "25" in context