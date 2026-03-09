from app.agent.nodes import AgentNodes


def create_node():

    return AgentNodes(

        knowledge_tool=None,

        sql_tool=None,

        calculator_tool=None,

        llm=None,

    )


def test_knowledge_tool():

    node = create_node()

    state = {

        "question": "What is leave policy?"

    }

    result = node.planner_node(state)

    assert result["tool"] == "knowledge"


def test_sql_tool():

    node = create_node()

    state = {

        "question": "employee salary"

    }

    result = node.planner_node(state)

    assert result["tool"] == "sql"


def test_calculator_tool():

    node = create_node()

    state = {

        "question": "25*18"

    }

    result = node.planner_node(state)

    assert result["tool"] == "calculator"