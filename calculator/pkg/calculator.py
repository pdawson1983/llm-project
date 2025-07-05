# calculator.py
import random

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "%": lambda a, b: a % b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "%": 2,
        }
        self.quotes = [
            "Pure mathematics is, in its way, the poetry of logical ideas. - Albert Einstein",
            "Mathematics is not about numbers, equations, computations, or algorithms: it is about understanding. - William Paul Thurston",
            "The only way to learn mathematics is to do mathematics. - Paul Halmos",
            "Mathematics is the most beautiful and most powerful creation of the human spirit. - Stefan Banach",
        ]

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None, self._get_quote()
        tokens = expression.strip().split()
        result = self._evaluate_infix(tokens)
        return result, self._get_quote()

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))

    def _get_quote(self):
        return random.choice(self.quotes)
