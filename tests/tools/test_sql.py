import pytest
from unittest.mock import MagicMock

from app.tools.sql import SQLTool


def test_execute_select():

    # Mock database row
    mock_row = MagicMock()
    mock_row._mapping = {
        "name": "Rahul",
        "department": "HR",
    }

    # Mock query result
    mock_result = [mock_row]

    # Mock connection
    mock_connection = MagicMock()
    mock_connection.execute.return_value = mock_result

    # Mock context manager
    mock_engine = MagicMock()

    mock_engine.connect.return_value.__enter__.return_value = (
        mock_connection
    )

    tool = SQLTool(mock_engine)

    rows = tool.execute(
        "SELECT * FROM employees"
    )

    assert len(rows) == 1

    assert rows[0]["name"] == "Rahul"

    assert rows[0]["department"] == "HR"




import pytest
from unittest.mock import MagicMock

from app.tools.sql import SQLTool


def test_reject_delete():

    tool = SQLTool(
        MagicMock()
    )

    with pytest.raises(ValueError):

        tool.execute(
            "DELETE FROM employees"
        )


def test_reject_update():

    tool = SQLTool(
        MagicMock()
    )

    with pytest.raises(ValueError):

        tool.execute(
            "UPDATE employees SET salary=0"
        )



def test_reject_insert():

    tool = SQLTool(
        MagicMock()
    )

    with pytest.raises(ValueError):

        tool.execute(
            "INSERT INTO employees VALUES(1)"
        )



def test_reject_drop():

    tool = SQLTool(
        MagicMock()
    )

    with pytest.raises(ValueError):

        tool.execute(
            "DROP TABLE employees"
        )

        