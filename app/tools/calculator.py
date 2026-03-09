import ast
import operator
import re


class CalculatorTool:
    """
    Safe calculator for arithmetic expressions.

    Accepts either a bare expression ("2+3") or a natural language
    question that contains one ("please calculate 2+3 for me"), and
    evaluates it using a restricted AST walker (no eval/exec, so
    arbitrary code such as __import__(...) can never run).
    """

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    # Only digits, whitespace, parentheses, and arithmetic operators
    # are allowed in an extracted expression.
    _EXPRESSION_PATTERN = re.compile(r"[-+*/%().\d\s]+")

    def calculate(self, expression: str):
        """
        Evaluate a mathematical expression safely.

        Raises:
            ValueError: if no valid arithmetic expression can be found,
                or if the expression uses unsupported syntax.
        """

        cleaned = self._extract_expression(expression)

        try:
            node = ast.parse(cleaned, mode="eval").body
        except (SyntaxError, ValueError) as exc:
            raise ValueError(
                f"Could not parse a valid math expression from: {expression!r}"
            ) from exc

        return self._evaluate(node)

    def _extract_expression(self, text: str) -> str:
        """
        Pull the arithmetic-looking portion out of free-form text.
        """

        text = text.strip()

        matches = self._EXPRESSION_PATTERN.findall(text)

        # Keep only matches that actually contain a digit (skip stray
        # punctuation-only matches) and pick the longest candidate.
        candidates = [m.strip() for m in matches if any(c.isdigit() for c in m)]

        if not candidates:
            raise ValueError(
                f"No arithmetic expression found in: {text!r}"
            )

        return max(candidates, key=len).strip()

    def _evaluate(self, node):

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Unsupported constant in expression")

        if isinstance(node, ast.BinOp):

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            op_type = type(node.op)

            if op_type not in self.OPERATORS:
                raise ValueError("Unsupported operator")

            return self.OPERATORS[op_type](left, right)

        if isinstance(node, ast.UnaryOp):

            operand = self._evaluate(node.operand)

            op_type = type(node.op)

            if op_type not in self.OPERATORS:
                raise ValueError("Unsupported operator")

            return self.OPERATORS[op_type](operand)

        raise ValueError("Unsupported expression")
