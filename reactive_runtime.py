from collections import defaultdict


class ReactiveRuntime:
    """
    runtime sustav za izvrsavanje reaktivnog programa.
    Sprema vrijednosti varijabli i AST izraze, evaluira izraze 
    te propagira promjene kroz graf ovisnosti
    """
    def __init__(self, dependency_graph):
        # usmjereni graf koji cuva ovisnosti/dependencyije
        self.deps = dependency_graph.graph

        # suprotno usmjeren graf
        self.reverse = self.build_reverse_graph(self.deps)

        # runtime stanje u kojem cuvamo trenutne vrijednosti varijabli
        self.values = {}

        # pohranjeni AST izrazi za reaktivne varijable
        self.expressions = {}

    def build_reverse_graph(self, deps):
        # iz danog usmjerenog grafa gradi suprotno usmjeren graf
        reverse = defaultdict(set)

        for var, depends_on in deps.items():
            for d in depends_on:
                reverse[d].add(var)

        return reverse

    def set_expression(self, name, expr):
        # cuva AST izraz za potrebe kasnijeg izracunavanja
        self.expressions[name] = expr

    def set_value(self, name, value):
        # azurira runtime vrijednost varijable
        self.values[name] = value

    def recompute(self, name):
        #racuna vrijednost varijable obzirom na pohranjeni izraz
        expr = self.expressions.get(name)

        if expr is None:
            return

        old_value = self.values.get(name)

        new_value = self.evaluate(expr)

        if old_value == new_value:
            return

        self.values[name] = new_value

        print(f"{name} recomputed: {new_value}")


    def propagate(self, changed_var):
        # propagira promjene u povezanim varijablama koristeci topoloski sort
        order = self.topological_sort(changed_var)

        for var in order:
            self.recompute(var)

    def evaluate(self, expr):
        # rekurzivno evaluira AST izraz
        from ast_nodes import (
            NumberLiteral,
            StringLiteral,
            BooleanLiteral,
            VariableExpression,
            BinaryExpression,
        )

        if isinstance(expr, NumberLiteral):
            return expr.value

        if isinstance(expr, StringLiteral):
            return expr.value

        if isinstance(expr, BooleanLiteral):
            return expr.value

        # provjera varijabli
        if isinstance(expr, VariableExpression):
            if expr.name not in self.values:
                raise Exception(f"Runtime error: undefined variable '{expr.name}'")
            return self.values[expr.name]

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
                if right == 0:
                    raise Exception("Runtime error: division by zero")
                return left / right

            if expr.operator == ">":
                return left > right

            if expr.operator == "<":
                return left < right

            if expr.operator == ">=":
                return left >= right

            if expr.operator == "<=":
                return left <= right

            if expr.operator == "==":
                return left == right

            if expr.operator == "!=":
                return left != right

            raise Exception(f"Unknown operator: {expr.operator}")

        raise Exception(f"Unknown expression: {expr}")

    def topological_sort(self, start_var):
        """
        vraca poredak izracunavanja koristeci DFS za cvorove koje mozemo doseći
        te Kahnov algoritam za topoloski sorting
        """
        from collections import deque

        graph = self.reverse

        # pohrani sve zahvacene cvorove
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

        # izracunaj broj ulaznih bridova za svaki cvor
        in_degree = {node: 0 for node in nodes}

        for node in nodes:
            for dep in graph.get(node, []):
                if dep in nodes:
                    in_degree[dep] += 1

        # pocni s cvorovima bez ovisnosti
        queue = deque([n for n in nodes if in_degree[n] == 0])
        order = []

        # Kahnov algoritam
        while queue:
            node = queue.popleft()
            order.append(node)

            for neigh in graph.get(node, []):
                if neigh in nodes:
                    in_degree[neigh] -= 1
                    if in_degree[neigh] == 0:
                        queue.append(neigh)

        return order