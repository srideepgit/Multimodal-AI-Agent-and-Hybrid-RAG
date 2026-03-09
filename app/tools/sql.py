from sqlalchemy import text
from sqlalchemy.engine import Engine


class SQLTool:
    """
    Executes read-only SQL queries.
    """

    def __init__(self, engine: Engine):
        self.engine = engine

    def execute(self, query: str):
        """
        Execute a SELECT query.
        """

        # Safety Check
        if not query.strip().lower().startswith("select"):
            raise ValueError(
                "Only SELECT queries are allowed."
            )

        with self.engine.connect() as connection:

            result = connection.execute(
                text(query)
            )

            return [
                dict(row._mapping)
                for row in result
            ]