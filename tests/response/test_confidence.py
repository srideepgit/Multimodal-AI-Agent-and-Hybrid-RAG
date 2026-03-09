from app.response.confidence import (
    ConfidenceScorer,
)


class Chunk:

    def __init__(self, score):

        self.rerank_score = score


def test_confidence_score():

    scorer = ConfidenceScorer()

    chunks = [

        Chunk(0.90),

        Chunk(0.80),

        Chunk(1.00),

    ]

    score = scorer.calculate(chunks)

    assert score == 0.9


def test_empty_chunks():

    scorer = ConfidenceScorer()

    score = scorer.calculate([])

    assert score == 0.0


def test_none_chunks_does_not_crash():

    scorer = ConfidenceScorer()

    assert scorer.calculate(None) == 0.0