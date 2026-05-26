from ast_nodes import (
    LetStatement,
    ReactiveStatement,
    SetStatement,
    PrintStatement,
    DependenciesStatement,
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

        elif isinstance(stmt, DependenciesStatement):
            self.handle_dependencies(stmt.name)

    def handle_dependencies(self, name):
        if not self.graph:
            print(f"{name} depends on: (no graph)")
            return

        deps = self.graph.graph.get(name, set())

        if not deps:
            print(f"{name} has no dependencies")
        else:
            print(f"{name} depends on: {', '.join(sorted(deps))}")