from enum import Enum, auto
from types import MappingProxyType

class CharClass(Enum):
    LETTER = auto()
    DIGIT = auto()
    WHITESPACE = auto()
    COLON = auto()       
    EQUAL = auto()       
    LBRACE = auto()      
    RBRACE = auto()      
    SYMBOL = auto()
    OTHER = auto()

def get_char_class(char: str) -> CharClass:
    if not char:
        return CharClass.OTHER
        
    if char.isalpha():
        return CharClass.LETTER
    if char.isdigit():
        return CharClass.DIGIT
    if char.isspace():
        return CharClass.WHITESPACE
        
    # Structural symbols that have distinct paths in the DFA
    if char == ':': return CharClass.COLON
    if char == '=': return CharClass.EQUAL
    if char == '{': return CharClass.LBRACE
    if char == '}': return CharClass.RBRACE
    
    if char in "+-*/<();":
        return CharClass.SYMBOL
        
    return CharClass.OTHER


class State(Enum):
    START = auto()
    INASSIGN = auto()
    INCOMMENT = auto()
    INNUM = auto()
    INID = auto()
    DONE = auto()

# next_state = DFA_TRANSITIONS[current_state][char_class]
DFA_TRANSITIONS = MappingProxyType({
    State.START: MappingProxyType({
        CharClass.LETTER: State.INID,
        CharClass.DIGIT: State.INNUM,
        CharClass.WHITESPACE: State.START,
        CharClass.COLON: State.INASSIGN,
        CharClass.LBRACE: State.INCOMMENT,
        CharClass.RBRACE: State.DONE,
        CharClass.SYMBOL: State.DONE,
        CharClass.EQUAL: State.DONE,
        CharClass.OTHER: State.DONE
    }),
    
    State.INID: MappingProxyType({
        CharClass.LETTER: State.INID,
        CharClass.DIGIT: State.DONE,
        CharClass.WHITESPACE: State.DONE,
        CharClass.COLON: State.DONE,
        CharClass.LBRACE: State.DONE,
        CharClass.RBRACE: State.DONE,
        CharClass.SYMBOL: State.DONE,
        CharClass.EQUAL: State.DONE,
        CharClass.OTHER: State.DONE
    }),
    
    State.INNUM: MappingProxyType({
        CharClass.LETTER: State.DONE,
        CharClass.DIGIT: State.INNUM,
        CharClass.WHITESPACE: State.DONE,
        CharClass.COLON: State.DONE,
        CharClass.LBRACE: State.DONE,
        CharClass.RBRACE: State.DONE,
        CharClass.SYMBOL: State.DONE,
        CharClass.EQUAL: State.DONE,
        CharClass.OTHER: State.DONE
    }),
    
    State.INASSIGN: MappingProxyType({
        CharClass.LETTER: State.DONE,
        CharClass.DIGIT: State.DONE,
        CharClass.WHITESPACE: State.DONE,
        CharClass.COLON: State.DONE,
        CharClass.LBRACE: State.DONE,
        CharClass.RBRACE: State.DONE,
        CharClass.SYMBOL: State.DONE,
        CharClass.EQUAL: State.DONE,
        CharClass.OTHER: State.DONE
    }),
    
    State.INCOMMENT: MappingProxyType({
        CharClass.LETTER: State.INCOMMENT,
        CharClass.DIGIT: State.INCOMMENT,
        CharClass.WHITESPACE: State.INCOMMENT,
        CharClass.COLON: State.INCOMMENT,
        CharClass.LBRACE: State.INCOMMENT,
        CharClass.RBRACE: State.START, # Closes the comment and restarts token gathering
        CharClass.SYMBOL: State.INCOMMENT,
        CharClass.EQUAL: State.INCOMMENT,
        CharClass.OTHER: State.INCOMMENT
    })
})