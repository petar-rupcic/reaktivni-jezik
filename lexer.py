from vepar import *


class T(TipoviTokena):
    LET = 'let'
    REACTIVE = 'reactive'
    SET = 'set'
    PRINT = 'print'
    SOURCE = 'source'
    EMIT = 'emit'
    DEPENDENCIES = 'dependencies'
    TRACE = 'trace'

    NUMBER = r'\d+(\.\d+)?'
    STRING = r'"[^"]*"'
    IDENT = r'[A-Za-z_][A-Za-z0-9_]*'

    EQEQ = '=='
    NEQ = '!='
    GE = '>='
    LE = '<='
    EQUAL = '='
    GT = '>'
    LT = '<'
    PLUS = '+'
    MINUS = '-'
    STAR = '*'
    SLASH = '/'

    LPAREN = '('
    RPAREN = ')'


@lexer
def reactive_lexer(lex):
    for znak in lex:
        if znak.isspace():
            lex.zanemari()

        elif znak.isalpha() or znak == '_':
            lex.zvijezda(lambda z: z.isalnum() or z == '_')
            yield lex.literal_ili(T.IDENT)

        elif znak.isdigit():
            lex.zvijezda(str.isdigit)

            if lex >= '.':
                lex.zvijezda(str.isdigit)

            yield lex.token(T.NUMBER)

        elif znak == '"':
            lex.zvijezda(lambda z: z != '"')
            lex >> '"'
            yield lex.token(T.STRING)

        elif znak == '=':
            if lex >= '=':
                yield lex.token(T.EQEQ)
            else:
                yield lex.token(T.EQUAL)

        elif znak == '!':
            lex >> '='
            yield lex.token(T.NEQ)

        elif znak == '>':
            if lex >= '=':
                yield lex.token(T.GE)
            else:
                yield lex.token(T.GT)

        elif znak == '<':
            if lex >= '=':
                yield lex.token(T.LE)
            else:
                yield lex.token(T.LT)

        elif znak == '+':
            yield lex.token(T.PLUS)

        elif znak == '-':
            yield lex.token(T.MINUS)

        elif znak == '*':
            yield lex.token(T.STAR)

        elif znak == '/':
            yield lex.token(T.SLASH)

        elif znak == '(':
            yield lex.token(T.LPAREN)

        elif znak == ')':
            yield lex.token(T.RPAREN)

        else:
            raise lex.greška(f"Neočekivani znak: {znak}")