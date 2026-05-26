from ast_nodes import (
    LetStatement,
    ReactiveStatement,
    SetStatement,
    PrintStatement,
    SourceStatement,
    EmitStatement,
    DependenciesStatement,
    TraceStatement,
    VariableExpression,
    BinaryExpression,
)


class Interpreter:
    def __init__(self, runtime, dependency_graph=None):
        self.runtime = runtime
        self.graph = dependency_graph

    def execute(self, program):
        for stmt in program.statements:
            self.execute_statement(stmt)

    def execute_statement(self, stmt):

        if isinstance(stmt, LetStatement):
            value = self.runtime.evaluate(stmt.expression)
            self.runtime.set_expression(stmt.name, stmt.expression)
            self.runtime.set_value(stmt.name, value)

        elif isinstance(stmt, ReactiveStatement):
            value = self.runtime.evaluate(stmt.expression)
            self.runtime.set_expression(stmt.name, stmt.expression)
            self.runtime.set_value(stmt.name, value)

        elif isinstance(stmt, SetStatement):
            value = self.runtime.evaluate(stmt.expression)

            self.runtime.set_value(stmt.name, value)
            self.runtime.propagate(stmt.name)

        elif isinstance(stmt, PrintStatement):
            value = self.runtime.evaluate(stmt.expression)
            print(value)

        elif isinstance(stmt, SourceStatement):
            # Source predstavlja vanjski izvor podataka.
            # Početno ga postavljamo na 0 jer prava vrijednost dolazi preko emit naredbe.
            self.runtime.set_value(stmt.name, 0)

        elif isinstance(stmt, EmitStatement):
            # Emit simulira dolazak nove vrijednosti iz vanjskog izvora.
            # Nakon promjene vrijednosti pokreće se propagacija.
            value = self.runtime.evaluate(stmt.expression)

            self.runtime.set_value(stmt.name, value)
            self.runtime.propagate(stmt.name)

        elif isinstance(stmt, DependenciesStatement):
            self.handle_dependencies(stmt.name)

        elif isinstance(stmt, TraceStatement):
            self.handle_trace(stmt.name)

    def handle_dependencies(self, name):
        if not self.graph:
            print(f"{name} depends on: (no graph)")
            return

        deps = self.graph.graph.get(name, set())

        if not deps:
            print(f"{name} has no dependencies")
        else:
            print(f"{name} depends on: {', '.join(sorted(deps))}")

    def handle_trace(self, name):
        expression = self.runtime.expressions.get(name)

        if expression is None:
            print(f"No trace available for {name}")
            return

        print(f"Trace for {name}:")
        print(f"{name} = {self.expression_to_string(expression)}")

        variables = self.collect_variables(expression)

        for variable in sorted(variables):
            value = self.runtime.values.get(variable, 0)
            print(f"{variable} = {value}")

        value = self.runtime.values.get(name, 0)
        print(f"{name} = {value}")

    def collect_variables(self, expr):
        if isinstance(expr, VariableExpression):
            return {expr.name}

        if isinstance(expr, BinaryExpression):
            left_vars = self.collect_variables(expr.left)
            right_vars = self.collect_variables(expr.right)
            return left_vars | right_vars

        return set()

    def expression_to_string(self, expr):
        if isinstance(expr, VariableExpression):
            return expr.name

        if isinstance(expr, BinaryExpression):
            left = self.expression_to_string(expr.left)
            right = self.expression_to_string(expr.right)
            return f"({left} {expr.operator} {right})"

        if hasattr(expr, "value"):
            if isinstance(expr.value, str):
                return f'"{expr.value}"'
            return str(expr.value)

        return str(expr)