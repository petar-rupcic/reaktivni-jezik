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
    """
    provodi evaluaciju izraza, odrzava vrijednosti varijabli, handlea updateove reaktivnih varijabli,
    izvrsava source/emit sistem, debugging naredbe 
    """
    def __init__(self, runtime, dependency_graph=None):
        self.runtime = runtime
        self.graph = dependency_graph # koristen kod poziva dependencies naredbe

    def execute(self, program):
        # izvrsi sve izraze u 
        for stmt in program.statements:
            self.execute_statement(stmt)

    def execute_statement(self, stmt):

        # let a = expr
        if isinstance(stmt, LetStatement):
            value = self.runtime.evaluate(stmt.expression)
            self.runtime.set_expression(stmt.name, stmt.expression)
            self.runtime.set_value(stmt.name, value)

        # reactive a = expr
        elif isinstance(stmt, ReactiveStatement):
            value = self.runtime.evaluate(stmt.expression)
            self.runtime.set_expression(stmt.name, stmt.expression)
            self.runtime.set_value(stmt.name, value)

        # set a = expr (aktivira propagaciju)
        elif isinstance(stmt, SetStatement):
            value = self.runtime.evaluate(stmt.expression)

            self.runtime.set_value(stmt.name, value)
            self.runtime.propagate(stmt.name)

        # ispisi vrijednost izraza
        elif isinstance(stmt, PrintStatement):
            value = self.runtime.evaluate(stmt.expression)
            print(value)

        #source uvodi vanjsku reaktivnu varijablu
        elif isinstance(stmt, SourceStatement):
            # source predstavlja vanjski izvor podataka.
            # pocetno ga postavljamo na 0 jer prava vrijednost dolazi preko emit naredbe.
            self.runtime.set_value(stmt.name, 0)

        # emit simulira uvodjenje nove vrijednosti iz vanjskog izvora
        elif isinstance(stmt, EmitStatement):
            # nakon promjene vrijednosti pokreće se propagacija
            value = self.runtime.evaluate(stmt.expression)

            self.runtime.set_value(stmt.name, value)
            self.runtime.propagate(stmt.name)

        # ispisuje dependency informaciju iz dependency grafa
        elif isinstance(stmt, DependenciesStatement):
            self.handle_dependencies(stmt.name)

        # ispisuje trace izracune reaktivnog izraza
        elif isinstance(stmt, TraceStatement):
            self.handle_trace(stmt.name)

    def handle_dependencies(self, name):
        # za danu varijablu, pokazi dependencyije s drugim varijablama 
        if not self.graph:
            print(f"{name} depends on: (no graph)")
            return

        deps = self.graph.graph.get(name, set())

        if not deps:
            print(f"{name} has no dependencies")
        else:
            print(f"{name} depends on: {', '.join(sorted(deps))}")

    def handle_trace(self, name):
        # rekonstruira detalje evaluacije izraza (za debugging)
        expression = self.runtime.expressions.get(name)

        if expression is None:
            print(f"No trace available for {name}")
            return

        print(f"Trace for {name}:")
        print(f"{name} = {self.expression_to_string(expression)}")

        variables = self.collect_variables(expression)

        # prikazi trenutne vrijednosti svih varijabli koristenih u izrazu
        for variable in sorted(variables):
            value = self.runtime.values.get(variable, 0)
            print(f"{variable} = {value}")

        value = self.runtime.values.get(name, 0)
        print(f"{name} = {value}")

    def collect_variables(self, expr):
        # prikazi sve varijable iskoristene u izrazu
        if isinstance(expr, VariableExpression):
            return {expr.name}

        if isinstance(expr, BinaryExpression):
            left_vars = self.collect_variables(expr.left)
            right_vars = self.collect_variables(expr.right)
            return left_vars | right_vars

        return set()

    def expression_to_string(self, expr):
        # AST izraza pretvori nazad u string format 
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