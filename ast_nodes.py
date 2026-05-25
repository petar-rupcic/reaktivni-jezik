from dataclasses import dataclass
from typing import List, Any


@dataclass
class Program:
    statements: List[Any]


@dataclass
class LetStatement:
    name: str
    expression: Any


@dataclass
class ReactiveStatement:
    name: str
    expression: Any


@dataclass
class SetStatement:
    name: str
    expression: Any


@dataclass
class PrintStatement:
    expression: Any


@dataclass
class SourceStatement:
    name: str


@dataclass
class EmitStatement:
    name: str
    expression: Any


@dataclass
class DependenciesStatement:
    name: str


@dataclass
class TraceStatement:
    name: str


@dataclass
class NumberLiteral:
    value: float


@dataclass
class StringLiteral:
    value: str


@dataclass
class BooleanLiteral:
    value: bool


@dataclass
class VariableExpression:
    name: str


@dataclass
class BinaryExpression:
    left: Any
    operator: str
    right: Any