from unittest.mock import MagicMock

from app.agent.graph import EnterpriseAgentGraph


def create_mock_nodes():

    nodes = MagicMock()

    # Every node simply returns the state
    nodes.planner_node.side_effect = lambda state: state
    nodes.knowledge_node.side_effect = lambda state: state
    nodes.sql_node.side_effect = lambda state: state
    nodes.calculator_node.side_effect = lambda state: state
    nodes.response_node.side_effect = lambda state: state
    nodes.validation_node.side_effect = lambda state: state

    return nodes


def test_graph_build():

    nodes = create_mock_nodes()

    graph = EnterpriseAgentGraph(nodes)

    app = graph.build()

    assert app is not None


def test_route_knowledge():

    graph = EnterpriseAgentGraph(MagicMock())

    state = {
        "tool": "knowledge"
    }

    assert graph.route(state) == "knowledge"


def test_route_sql():

    graph = EnterpriseAgentGraph(MagicMock())

    state = {
        "tool": "sql"
    }

    assert graph.route(state) == "sql"


def test_route_calculator():

    graph = EnterpriseAgentGraph(MagicMock())

    state = {
        "tool": "calculator"
    }

    assert graph.route(state) == "calculator"