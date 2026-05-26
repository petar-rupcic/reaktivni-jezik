from collections import defaultdict


class ReactiveRuntime:
    def __init__(self, dependency_graph):
        self.deps = dependency_graph.graph
        self.reverse = self.build_reverse_graph(self.deps)

        self.values = {}
        self.expressions = {}

    def build_reverse_graph(self, deps):
        reverse = defaultdict(set)

        for var, depends_on in deps.items():
            for d in depends_on:
                reverse[d].add(var)

        return reverse

    def set_expression(self, name, expr):
        self.expressions[name] = expr

    def set_value(self, name, value):
        self.values[name] = value

    def recompute(self, name):
        expr = self.expressions.get(name)

        if expr is None:
            return

        new_value = self.evaluate(expr)
        old_value = self.values.get(name)

        self.values[name] = new_value

        if old_value != new_value:
            print(f"{name} recomputed: {new_value}")

    def propagate(self, changed_var):
        order = self.topological_sort(changed_var)

        if changed_var in order:
            order.remove(changed_var)

        for var in order:
            self.recompute(var)

    def evaluate(self, expr):
        from ast_nodes import (
            NumberLiteral,
            VariableExpression,
            BinaryExpression
        )

        if isinstance(expr, NumberLiteral):
            return expr.value

        if isinstance(expr, VariableExpression):
            return self.values.get(expr.name, 0)

        if isinstance(expr, BinaryExpression):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)

            if expr.operator == "+":
                return left + right
            if expr.operator == "-":
                return left - right
            if expr.operator == "*":
                return left * right
            if expr.operator == "/":
                return left / right

        raise Exception(f"Unknown expression: {expr}")

    def topological_sort(self, start_var):
        from collections import deque

        graph = self.reverse

        visited = set()
        nodes = set()

        def dfs(node):
            if node in visited:
                return

            visited.add(node)

            for neigh in graph.get(node, []):
                nodes.add(neigh)
                dfs(neigh)

        dfs(start_var)

        in_degree = {node: 0 for node in nodes}

        for node in nodes:
            for dep in graph.get(node, []):
                if dep in nodes:
                    in_degree[dep] += 1

        queue = deque([n for n in nodes if in_degree[n] == 0])
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)

            for neigh in graph.get(node, []):
                if neigh in nodes:
                    in_degree[neigh] -= 1
                    if in_degree[neigh] == 0:
                        queue.append(neigh)

        return order