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

        while not self >= KRAJ:
            statements.append(self.statement())

        return Program(statements)

    def statement(self):
        if self >= T.LET:
            name = (self >> T.IDENT).sadržaj
            self >> T.EQUAL
            expression = self.expression()
            return LetStatement(name, expression)

        if self >= T.REACTIVE:
            name = (self >> T.IDENT).sadržaj
            self >> T.EQUAL
            expression = self.expression()
            return ReactiveStatement(name, expression)

        if self >= T.SET:
            name = (self >> T.IDENT).sadržaj
            self >> T.EQUAL
            expression = self.expression()
            return SetStatement(name, expression)

        if self >= T.PRINT:
            expression = self.expression()
            return PrintStatement(expression)

        if self >= T.SOURCE:
            name = (self >> T.IDENT).sadržaj
            return SourceStatement(name)

        if self >= T.EMIT:
            name = (self >> T.IDENT).sadržaj
            self >> T.EQUAL
            expression = self.expression()
            return EmitStatement(name, expression)

        if self >= T.DEPENDENCIES:
            name = (self >> T.IDENT).sadržaj
            return DependenciesStatement(name)

        if self >= T.TRACE:
            name = (self >> T.IDENT).sadržaj
            return TraceStatement(name)

        raise self.greška()

    def expression(self):
        return self.comparison()

    def comparison(self):
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
        if number := self >= T.NUMBER:
            if "." in number.sadržaj:
                return NumberLiteral(float(number.sadržaj))
            return NumberLiteral(int(number.sadržaj))

        if string := self >= T.STRING:
            return StringLiteral(string.sadržaj[1:-1])

        if ident := self >= T.IDENT:
            if ident.sadržaj == "true":
                return BooleanLiteral(True)
            if ident.sadržaj == "false":
                return BooleanLiteral(False)
            return VariableExpression(ident.sadržaj)

        if self >= T.LPAREN:
            expression = self.expression()
            self >> T.RPAREN
            return expression

        raise self.greška()