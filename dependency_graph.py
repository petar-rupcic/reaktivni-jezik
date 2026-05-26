from ast_nodes import (
    ReactiveStatement,
    VariableExpression,
    BinaryExpression,
)


class DependencyGraph:
    def __init__(self):
        self.graph = {}

    def build(self, program):

        for statement in program.statements:

            if isinstance(statement, ReactiveStatement):

                dependencies = self.extract_dependencies(
                    statement.expression
                )

                self.graph[statement.name] = dependencies

    def extract_dependencies(self, expr):

        dependencies = set()

        if isinstance(expr, VariableExpression):
            dependencies.add(expr.name)

        elif isinstance(expr, BinaryExpression):
            dependencies |= self.extract_dependencies(expr.left)
            dependencies |= self.extract_dependencies(expr.right)

        return dependencies

    def print_graph(self):

        print("Dependency graph:")

        for variable, deps in self.graph.items():
            print(f"{variable} depends on: {', '.join(deps)}")