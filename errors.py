# Error handling for the TINY scanner

WHITESPACE = " \t\n\r\f\v"
COMMENT_START = '{'
COMMENT_END = '}'


class ScannerError(Exception):
    def __init__(self, msg, line=1, col=1, filename=None):
        self.msg = msg
        self.line = line
        self.col = col
        self.filename = filename
        super().__init__(self.__str__())

    def __str__(self):
        if self.filename:
            return f"Lexical error at {self.filename}:{self.line}:{self.col}: {self.msg}"
        return f"Lexical error at line {self.line}, column {self.col}: {self.msg}"


class InvalidCharError(ScannerError):
    def __init__(self, ch, line=1, col=1, filename=None):
        super().__init__(f"invalid character {ch!r}", line, col, filename)


class UnterminatedComment(ScannerError):
    def __init__(self, line=1, col=1, filename=None):
        super().__init__(f"unterminated comment: missing {COMMENT_END!r}", line, col, filename)


# keep old names too
InvalidCharacterError = InvalidCharError
UnterminatedCommentError = UnterminatedComment


def skip_whitespace_and_comments(text, i=0, line=1, col=1, filename=None):
    """Skip spaces, tabs, newlines and { ... } comments.
    Returns (new_index, new_line, new_column) or can report error.
    """
    n = len(text)
    while i < n:
        ch = text[i]

        # whitespace
        if ch in WHITESPACE:
            if ch == '\n':
                line += 1
                col = 1
            elif ch == '\r':
                # handle CRLF
                if i + 1 < n and text[i + 1] == '\n':
                    i += 1
                line += 1
                col = 1
            else:
                col += 1
            i += 1
            continue

        # comment
        if ch == COMMENT_START:
            start_line = line
            start_col = col
            i += 1
            col += 1
            while i < n and text[i] != COMMENT_END:
                if text[i] == '\n':
                    line += 1
                    col = 1
                elif text[i] == '\r':
                    if i + 1 < n and text[i + 1] == '\n':
                        i += 1
                    line += 1
                    col = 1
                else:
                    col += 1
                i += 1

            if i >= n:
                raise UnterminatedComment(start_line, start_col, filename)

            # skip }
            i += 1
            col += 1
            continue

        break

    return i, line, col


# aliases for compatibility
skip_ignored = skip_whitespace_and_comments
skipWhitespaceAndComments = skip_whitespace_and_comments
skip_whitespace_and_comment = skip_whitespace_and_comments
