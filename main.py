from parser import ReactiveParser
from semantic_analyzer import SemanticAnalyzer
from dependency_graph import DependencyGraph
from reactive_runtime import ReactiveRuntime
from interpreter import Interpreter


def parse_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return ReactiveParser(file.read())


if __name__ == "__main__":

    program = parse_file("examples/10_full_language_demo.rlang")

    analyzer = SemanticAnalyzer()
    analyzer.analyze(program)

    graph = DependencyGraph()
    graph.build(program)

    runtime = ReactiveRuntime(graph)

    for stmt in program.statements:
        if hasattr(stmt, "name") and hasattr(stmt, "expression"):
            runtime.set_expression(stmt.name, stmt.expression)

    interpreter = Interpreter(runtime, graph)
    interpreter.execute(program)

    print("\nFinal values:", runtime.values)