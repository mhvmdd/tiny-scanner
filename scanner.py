from char_classes import CharClass, State, DFA_TRANSITIONS, get_char_class
from tokens import Token, TokenType, RESERVED_WORDS, SPECIAL_SYMBOLS


class Scanner:
    def __init__(self, reader):
        self.reader = reader  # an InputReader
        
    @staticmethod
    def _make_word(lexeme):
        """Keyword (if, then, ...) or plain identifier."""
        return Token(RESERVED_WORDS.get(lexeme, TokenType.IDENTIFIER), lexeme)

    def get_token(self):
        """Return the next Token, or None at the end of the input."""
        state = State.START
        lexeme = ""
        token_line = self.reader.get_line_number()

        while True:
            char = self.reader.next_char()

            # end of file 
            if char is None:
                if state == State.INID:
                    return self._make_word(lexeme)

                if state == State.INNUM:
                    return Token(TokenType.NUMBER, lexeme)

                if state == State.INASSIGN:
                    return None

                return None

            char_class = get_char_class(char)
            next_state = DFA_TRANSITIONS[state][char_class]

            #START 
            if state == State.START:
                if char_class == CharClass.WHITESPACE:
                    continue

                token_line = self.reader.get_line_number()

                if next_state == State.INCOMMENT:
                    state = State.INCOMMENT

                elif next_state in (State.INID, State.INNUM, State.INASSIGN):
                    lexeme = char
                    state = next_state

                elif char_class in (CharClass.SYMBOL, CharClass.EQUAL):
                    return Token(SPECIAL_SYMBOLS[char], char)

            #identifier 
            elif state == State.INID:
                if next_state == State.INID:
                    lexeme += char
                else:
                    self.reader.unget_char()
                    return self._make_word(lexeme)

            #number 
            elif state == State.INNUM:
                if next_state == State.INNUM:
                    lexeme += char
                else:
                    self.reader.unget_char()
                    return Token(TokenType.NUMBER, lexeme)

            # ':' waiting for '=' 
            elif state == State.INASSIGN:
                if char_class == CharClass.EQUAL:
                    return Token(TokenType.ASSIGN, ":=")

                self.reader.unget_char()
                state, lexeme = State.START, ""

            # inside { ... } 
            elif state == State.INCOMMENT:
                if next_state == State.START:
                    state = State.START
