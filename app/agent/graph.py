from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from app.agent.state import AgentState


class EnterpriseAgentGraph:

    def __init__(self, nodes):

        self.nodes = nodes

    def build(self):

        graph = StateGraph(AgentState)

        # -----------------------
        # Nodes
        # -----------------------

        graph.add_node(
            "planner",
            self.nodes.planner_node,
        )

        graph.add_node(
            "knowledge",
            self.nodes.knowledge_node,
        )

        graph.add_node(
            "sql",
            self.nodes.sql_node,
        )

        graph.add_node(
            "calculator",
            self.nodes.calculator_node,
        )

        graph.add_node(
            "response",
            self.nodes.response_node,
        )

        graph.add_node(
            "validation",
            self.nodes.validation_node,
        )

        # -----------------------
        # Start
        # -----------------------

        graph.add_edge(
            START,
            "planner",
        )

        # -----------------------
        # Planner Routing
        # -----------------------

        graph.add_conditional_edges(
            "planner",
            self.route,
            {
                "knowledge": "knowledge",
                "sql": "sql",
                "calculator": "calculator",
            },
        )

        # -----------------------
        # Tool → Response
        # -----------------------

        graph.add_edge(
            "knowledge",
            "response",
        )

        graph.add_edge(
            "sql",
            "response",
        )

        graph.add_edge(
            "calculator",
            "response",
        )

        # -----------------------
        # Validation
        # -----------------------

        graph.add_edge(
            "response",
            "validation",
        )

        graph.add_edge(
            "validation",
            END,
        )

        return graph.compile()

    def route(
        self,
        state: AgentState,
    ):

        return state["tool"]