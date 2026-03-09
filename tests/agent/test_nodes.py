from unittest.mock import MagicMock

import pytest

from app.agent.nodes import AgentNodes


class Response:

    def __init__(self):
        self.answer = "Enterprise AI"
        self.sources = []
        self.confidence = 0.95


def create_nodes():

    knowledge = MagicMock()

    sql = MagicMock()

    calculator = MagicMock()

    llm = MagicMock()

    nodes = AgentNodes(

        knowledge_tool=knowledge,

        sql_tool=sql,

        calculator_tool=calculator,

        llm=llm,

    )

    # Inject response engine dependencies

    nodes.context_builder = MagicMock()

    nodes.generator = MagicMock()

    nodes.validator = MagicMock()

    nodes.citation_builder = MagicMock()

    nodes.confidence_scorer = MagicMock()

    return nodes


def test_planner_knowledge():

    nodes = create_nodes()

    state = {

        "question":"leave policy"

    }

    result = nodes.planner_node(state)

    assert result["tool"] == "knowledge"


def test_planner_sql():

    nodes = create_nodes()

    state = {

        "question":"employee salary"

    }

    result = nodes.planner_node(state)

    assert result["tool"] == "sql"


def test_planner_calculator():

    nodes = create_nodes()

    state = {

        "question":"25*18"

    }

    result = nodes.planner_node(state)

    assert result["tool"] == "calculator"


def test_knowledge_node():

    nodes = create_nodes()

    nodes.knowledge_tool.search.return_value = [

        "chunk1",

        "chunk2"

    ]

    state = {

        "question":"leave",

        "retrieved_chunks":[]

    }

    result = nodes.knowledge_node(state)

    assert len(result["retrieved_chunks"]) == 2


def test_sql_node():

    nodes = create_nodes()

    nodes.sql_tool.execute.return_value = [

        {

            "count":10

        }

    ]

    state = {

        "sql_result":[]

    }

    result = nodes.sql_node(state)

    assert result["sql_result"][0]["count"] == 10


def test_calculator_node():

    nodes = create_nodes()

    nodes.calculator_tool.calculate.return_value = 450

    state = {

        "question":"25*18"

    }

    result = nodes.calculator_node(state)

    assert result["calculator_result"] == 450


def test_response_node():

    nodes = create_nodes()

    nodes.context_builder.build.return_value = "context"

    nodes.generator.generate.return_value = "Enterprise AI"

    nodes.citation_builder.build.return_value = []

    nodes.confidence_scorer.calculate.return_value = 0.95

    nodes.validator.validate.return_value = Response()

    state = {

        "question":"leave",

        "retrieved_chunks":[],

        "sql_result":[],

        "calculator_result":None,

    }

    result = nodes.response_node(state)

    assert result["answer"] == "Enterprise AI"

    assert result["confidence"] == 0.95


def test_validation_node():

    nodes = create_nodes()

    state = {

        "answer":"hello"

    }

    assert nodes.validation_node(state) == state


def test_validation_node_error():

    nodes = create_nodes()

    state = {

        "answer":""

    }

    with pytest.raises(ValueError):

        nodes.validation_node(state)