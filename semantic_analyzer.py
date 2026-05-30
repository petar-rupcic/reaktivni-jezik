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


class SemanticError(Exception):
    pass


class SemanticAnalyzer:
    """
    Provjerava semantiku kroz AST.

    Analyzer provjerava redefinicije varijabli, 
    koristenje vec postojecih varijabli u naredbama 
    i validnost source, emit, dependency i trace izraza
    """

    def __init__(self):
        self.symbols = set()

    def analyze(self, program):
        for statement in program.statements:
            self.analyze_statement(statement)

    def analyze_statement(self, stmt):

        #deklaracija varijable mora biti jedinstvena    
        if isinstance(stmt, LetStatement):
            if stmt.name in self.symbols:
                raise SemanticError(
                    f"Variable '{stmt.name}' is already defined."
                )

            self.analyze_expression(stmt.expression)
            self.symbols.add(stmt.name)
    
        #reaktivna varijabla mora biti jedinstvena
        elif isinstance(stmt, ReactiveStatement):
            if stmt.name in self.symbols:
                raise SemanticError(
                    f"Variable '{stmt.name}' is already defined."
                )

            self.symbols.add(stmt.name)

        #pridruzivanje je dozvoljeno samo za deklarirane varijable
        elif isinstance(stmt, SetStatement):
            if stmt.name not in self.symbols:
                raise SemanticError(
                    f"Variable '{stmt.name}' is not defined."
                )

            self.analyze_expression(stmt.expression)

        elif isinstance(stmt, PrintStatement):
            self.analyze_expression(stmt.expression)

        #source uvodi vanjski izvor podataka
        elif isinstance(stmt, SourceStatement):
            if stmt.name in self.symbols:
                raise SemanticError(
                    f"Variable '{stmt.name}' is already defined."
                )

            self.symbols.add(stmt.name)

        #emit pridruzuje vrijednost prethodno deklariranoj varijabli
        elif isinstance(stmt, EmitStatement):
            if stmt.name not in self.symbols:
                raise SemanticError(
                    f"Source '{stmt.name}' is not defined."
                )

            self.analyze_expression(stmt.expression)

        #dependency naredba mora se pozvati na postojecu varijablu
        elif isinstance(stmt, DependenciesStatement):
            if stmt.name not in self.symbols:
                raise SemanticError(
                    f"Variable '{stmt.name}' is not defined."
                )

        #trace naredba mora se pozvati na postojecu varijablu
        elif isinstance(stmt, TraceStatement):
            if stmt.name not in self.symbols:
                raise SemanticError(
                    f"Variable '{stmt.name}' is not defined."
                )

    def analyze_expression(self, expr):
        #rekurzivno analizira izraz
        
        if isinstance(expr, VariableExpression):
            # reaktivni jezici dopustaju forward reference
            # korektnost se iscitava iz dependency grafa
            return

        elif isinstance(expr, BinaryExpression):
            self.analyze_expression(expr.left)
            self.analyze_expression(expr.right) 
