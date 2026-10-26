from dataclasses import dataclass
from enum import Enum, auto
from types import MappingProxyType # to make dictionary read only

class TokenType(Enum):
    # Reserved Words
    IF = auto()
    THEN = auto()
    ELSE = auto()
    END = auto()
    REPEAT = auto()
    UNTIL = auto()
    READ = auto()
    WRITE = auto()
    
    # Special Symbols
    SEMICOLON = auto()
    ASSIGN = auto()
    LESSTHAN = auto()
    EQUAL = auto()
    PLUS = auto()
    MINUS = auto()
    MULT = auto()
    DIV = auto()
    OPENBRACKET = auto()
    CLOSEDBRACKET = auto()
    
    # Other
    IDENTIFIER = auto()
    NUMBER = auto()

@dataclass
class Token:
    type: TokenType
    value: str | int

RESERVED_WORDS = MappingProxyType({
    "if": TokenType.IF,
    "then": TokenType.THEN,
    "else": TokenType.ELSE,
    "end": TokenType.END,
    "repeat": TokenType.REPEAT,
    "until": TokenType.UNTIL,
    "read": TokenType.READ,
    "write": TokenType.WRITE
})

SPECIAL_SYMBOLS = MappingProxyType({
    ";": TokenType.SEMICOLON,
    "<": TokenType.LESSTHAN,
    "=": TokenType.EQUAL,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MULT,
    "/": TokenType.DIV,
    "(": TokenType.OPENBRACKET,
    ")": TokenType.CLOSEDBRACKET,
})