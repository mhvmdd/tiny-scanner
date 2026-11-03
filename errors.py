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
            return f"ERROR at line {self.line}: {self.msg}"
        return f"ERROR at line {self.line}: {self.msg}"


class InvalidCharError(ScannerError):
    def __init__(self, ch, line=1, col=1, filename=None):
        super().__init__(f"Invalid character {ch!r}", line, col, filename)


class UnterminatedComment(ScannerError):
    def __init__(self, line=1, col=1, filename=None):
        super().__init__(f"Unterminated comment: missing {COMMENT_END!r}", line, col, filename)


class NestedComment(ScannerError):
    def __init__(self, line=1, col=1, filename=None):
        super().__init__("Nested comment: '{' inside a comment that is not closed yet", line, col, filename)


class InvalidIdentifierError(ScannerError):
    """A reserved word written in capitals, e.g. READ instead of read."""
    def __init__(self, word, line=1, col=1, filename=None):
        super().__init__(f"Invalid identifier {word!r}", line, col, filename)


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
            start_i = i
            i += 1
            col += 1
            while i < n and text[i] != COMMENT_END:
                # A '{' while a comment is still open is a nested comment.
                if text[i] == COMMENT_START:
                    err = NestedComment(line, col, filename)
                    err.pos = start_i
                    raise err
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
                err = UnterminatedComment(start_line, start_col, filename)
                err.pos = start_i
                raise err

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


# ---------------------------------------------------------------------------
# Shared source checking (used by both main.py and ui.py)
# ---------------------------------------------------------------------------

_VALID_SYMBOLS = set(":=+-*/<();")


def check_source(text, filename=None):
    """Scan the whole source once and return the FIRST error found.

    Returns None if the source is clean, otherwise (error, position) where
    `error` is a ScannerError subclass instance and `position` is the index in
    `text` where the problem starts (tokens before it are still valid).

    Comments are skipped with skip_whitespace_and_comments(), so an unclosed
    '{' is always reported as UnterminatedComment, wherever it is.
    """
    n = len(text)
    i, line, col = 0, 1, 1

    while True:
        try:
            i, line, col = skip_ignored(text, i, line, col, filename)
        except (UnterminatedCommentError, NestedComment) as e:
            # e.pos is the index of the '{' that starts the bad comment.
            return e, getattr(e, "pos", 0)

        if i >= n:
            return None

        ch = text[i]

        if ch.isalpha() or ch == '_':
            j = i
            while j < n and (text[j].isalnum() or text[j] == '_'):
                j += 1
            col += j - i
            i = j
            continue

        if ch.isdigit():
            j = i
            while j < n and text[j].isdigit():
                j += 1
            col += j - i
            i = j
            continue

        # ':' is only valid as part of ':='
        if ch == ':':
            if i + 1 < n and text[i + 1] == '=':
                i += 2
                col += 2
                continue
            return InvalidCharError(ch, line, col, filename), i

        if ch not in _VALID_SYMBOLS:
            return InvalidCharError(ch, line, col, filename), i

        i += 1
        col += 1


def scan_text(text):
    """Run the scanner over `text` and return the tokens it produces.

    Stops quietly at the first scanner exception. Used to collect the valid
    tokens that come before a reported error.
    """
    import os
    import tempfile
    from input_reader import InputReader
    from scanner import Scanner

    fd, path = tempfile.mkstemp(suffix=".tiny")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        scanner = Scanner(InputReader(path))
        tokens = []
        while True:
            try:
                token = scanner.get_token()
            except ScannerError:
                break
            except Exception:
                break
            if token is None:
                break
            tokens.append(token)
        return tokens
    finally:
        try:
            os.remove(path)
        except OSError:
            pass