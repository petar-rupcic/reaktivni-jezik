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

    def detect_cycles(self):
        visited = set()
        stack = set()

        def dfs(node):
            if node in stack:
                return True  

            if node in visited:
                return False

            visited.add(node)
            stack.add(node)

            for neigh in self.graph.get(node, []):
                if dfs(neigh):
                    return True

            stack.remove(node)
            return False

        for node in self.graph:
            if dfs(node):
                raise Exception(f"Semantic error: circular dependency detected starting at '{node}'")