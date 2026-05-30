from vepar import *
from lexer import T
from ast_nodes import (
    Program,
    LetStatement,
    ReactiveStatement,
    SetStatement,
    PrintStatement,
    SourceStatement,
    EmitStatement,
    DependenciesStatement,
    TraceStatement,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    VariableExpression,
    BinaryExpression,
)


class ReactiveParser(Parser):
    def start(self):
        statements = []

        # parsiraj niz izraza dok ne dodjes do kraja inputa
        while not self >= KRAJ:
            statements.append(self.statement())

        return Program(statements)

    def statement(self):
        # let a =  expr
        if self >= T.LET:
            name = (self >> T.IDENT).sadržaj
            self >> T.EQUAL
            expression = self.expression()
            return LetStatement(name, expression)

        # reactive a = expr
        if self >= T.REACTIVE:
            name = (self >> T.IDENT).sadržaj
            self >> T.EQUAL
            expression = self.expression()
            return ReactiveStatement(name, expression)
        # set a = expr
        if self >= T.SET:
            name = (self >> T.IDENT).sadržaj
            self >> T.EQUAL
            expression = self.expression()
            return SetStatement(name, expression)

        # print expr
        if self >= T.PRINT:
            expression = self.expression()
            return PrintStatement(expression)

        # source a
        if self >= T.SOURCE:
            name = (self >> T.IDENT).sadržaj
            return SourceStatement(name)

        # emit a = expr
        if self >= T.EMIT:
            name = (self >> T.IDENT).sadržaj
            self >> T.EQUAL
            expression = self.expression()
            return EmitStatement(name, expression)

        # dependencies a
        if self >= T.DEPENDENCIES:
            name = (self >> T.IDENT).sadržaj
            return DependenciesStatement(name)

        # trace a
        if self >= T.TRACE:
            name = (self >> T.IDENT).sadržaj
            return TraceStatement(name)

        # greska u sintaksi
        raise self.greška()

    def expression(self):
        # pocetna tocka za izraze namanjeg prioriteta
        return self.comparison()

    def comparison(self):
        # handlea operatore usporedbe
        left = self.addition()

        if self >= T.GT:
            right = self.addition()
            return BinaryExpression(left, ">", right)

        if self >= T.LT:
            right = self.addition()
            return BinaryExpression(left, "<", right)

        if self >= T.EQEQ:
            right = self.addition()
            return BinaryExpression(left, "==", right)

        if self >= T.NEQ:
            right = self.addition()
            return BinaryExpression(left, "!=", right)

        if self >= T.GE:
            right = self.addition()
            return BinaryExpression(left, ">=", right)

        if self >= T.LE:
            right = self.addition()
            return BinaryExpression(left, "<=", right)

        return left

    def addition(self):
        # handlea + i - uz asocijativnost s lijeva
        left = self.multiplication()

        while True:
            if self >= T.PLUS:
                right = self.multiplication()
                left = BinaryExpression(left, "+", right)

            elif self >= T.MINUS:
                right = self.multiplication()
                left = BinaryExpression(left, "-", right)

            else:
                return left

    def multiplication(self):
        # handlea * i / uz veci prioritet od + i -
        left = self.primary()

        while True:
            if self >= T.STAR:
                right = self.primary()
                left = BinaryExpression(left, "*", right)

            elif self >= T.SLASH:
                right = self.primary()
                left = BinaryExpression(left, "/", right)

            else:
                return left

    def primary(self):
        # brojevi (int ili float)
        if number := self >= T.NUMBER:
            if "." in number.sadržaj:
                return NumberLiteral(float(number.sadržaj))
            return NumberLiteral(int(number.sadržaj))

        # string literal
        if string := self >= T.STRING:
            return StringLiteral(string.sadržaj[1:-1])

        # identifikator ili boolean literal
        if ident := self >= T.IDENT:
            if ident.sadržaj == "true":
                return BooleanLiteral(True)
            if ident.sadržaj == "false":
                return BooleanLiteral(False)
            return VariableExpression(ident.sadržaj)

        # zagrade
        if self >= T.LPAREN:
            expression = self.expression()
            self >> T.RPAREN
            return expression

        # greska u izrazu
        raise self.greška()