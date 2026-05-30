from parser import ReactiveParser
from semantic_analyzer import SemanticAnalyzer
from dependency_graph import DependencyGraph
from reactive_runtime import ReactiveRuntime
from interpreter import Interpreter


def parse_file(path):
    # ucitaj izvorni program i parsiraj ga u AST
    with open(path, "r", encoding="utf-8") as file:
        return ReactiveParser(file.read())


if __name__ == "__main__":

    # izbor programa za izvrsavanje
    program = parse_file("examples/08_complex_dependency_chain.rlang")

    # semanticka analiza
    analyzer = SemanticAnalyzer()
    analyzer.analyze(program)

    # izgradi graf ovisnosti i provjeri cikluse
    graph = DependencyGraph()
    graph.build(program)
    graph.detect_cycles()

    # inicijalizacija runtime sustava
    runtime = ReactiveRuntime(graph)

    # pohrani sve AST izraze za ponovno racunanje reaktivnih varijabli
    for stmt in program.statements:
        if hasattr(stmt, "name") and hasattr(stmt, "expression"):
            runtime.set_expression(stmt.name, stmt.expression)

    # izvrsavanje pomocu interpretera
    interpreter = Interpreter(runtime, graph)
    interpreter.execute(program)

    # prikazi konacno stanje svih varijabli
    print("\nFinal values:", runtime.values)