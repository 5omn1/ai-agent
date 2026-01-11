class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
                values.append(int(token))
            elif token in self.operators:
                while (operators and operators[-1] in self.precedence and
                       self.precedence[operators[-1]] >= self.precedence[token]):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                raise ValueError(f"Unknown token: {token}")

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("Invalid expression")

        return values[0]
