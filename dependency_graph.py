from ast_nodes import (
    ReactiveStatement,
    VariableExpression,
    BinaryExpression,
)


class DependencyGraph:
    """
    Gradi graf ovisnosti iz reaktivnih varijabli.
    Koristi se za propagaciju promjena, odredjivanje redoslijeda izracunavanja
    i detekciju kruznih ovisnosti
    """
    def __init__(self):
        self.graph = {}

    def build(self, program):
        # iz AST-a izgradi graf ovisnosti

        for statement in program.statements:

            if isinstance(statement, ReactiveStatement):

                dependencies = self.extract_dependencies(
                    statement.expression
                )

                self.graph[statement.name] = dependencies

    def extract_dependencies(self, expr):
        # rekurzivno pronalazi sve varijable koristene u izrazu

        dependencies = set()

        if isinstance(expr, VariableExpression):
            dependencies.add(expr.name)

        elif isinstance(expr, BinaryExpression):
            dependencies |= self.extract_dependencies(expr.left)
            dependencies |= self.extract_dependencies(expr.right)

        return dependencies

    def print_graph(self):
        # ispis grafa

        print("Dependency graph:")

        for variable, deps in self.graph.items():
            print(f"{variable} depends on: {', '.join(deps)}")

    def detect_cycles(self):
        # detekcija ciklusa koristeci DFS - ako tijekom DFS-a posjetimo cvor koji
        # se vec nalazi na trenutnom putu pretrage, ciklus postoji

        visited = set()
        stack = set()

        def dfs(node):

            # cvor je pronadjen na trenutnom DFS putu
            if node in stack:
                return True  

            # cvor je vec obradjen
            if node in visited:
                return False

            visited.add(node)
            stack.add(node)

            for neigh in self.graph.get(node, []):
                if dfs(neigh):
                    return True

            # zavrsetak obrade cvora
            stack.remove(node)
            return False

        # pokreni DFS iz svakog cvora
        for node in self.graph:
            if dfs(node):
                raise Exception(f"Semantic error: circular dependency detected starting at '{node}'")