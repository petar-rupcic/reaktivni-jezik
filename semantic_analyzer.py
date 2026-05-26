from ast_nodes import (
    LetStatement,
    ReactiveStatement,
    SetStatement,
    PrintStatement,
    VariableExpression,
    BinaryExpression,
)


class SemanticError(Exception):
    pass


class SemanticAnalyzer:
    def __init__(self):
        self.symbols = set()

    def analyze(self, program):
        for statement in program.statements:
            self.analyze_statement(statement)

    def analyze_statement(self, stmt):

        if isinstance(stmt, LetStatement):
            if stmt.name in self.symbols:
                raise SemanticError(
                    f"Variable '{stmt.name}' is already defined."
                )

            self.analyze_expression(stmt.expression)
            self.symbols.add(stmt.name)

        elif isinstance(stmt, ReactiveStatement):
            if stmt.name in self.symbols:
                raise SemanticError(
                    f"Variable '{stmt.name}' is already defined."
                )

            self.analyze_expression(stmt.expression)
            self.symbols.add(stmt.name)

        elif isinstance(stmt, SetStatement):
            if stmt.name not in self.symbols:
                raise SemanticError(
                    f"Variable '{stmt.name}' is not defined."
                )

            self.analyze_expression(stmt.expression)

        elif isinstance(stmt, PrintStatement):
            self.analyze_expression(stmt.expression)

    def analyze_expression(self, expr):

        if isinstance(expr, VariableExpression):
            if expr.name not in self.symbols:
                raise SemanticError(
                    f"Variable '{expr.name}' is not defined."
                )

        elif isinstance(expr, BinaryExpression):
            self.analyze_expression(expr.left)
            self.analyze_expression(expr.right)