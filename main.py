import sys
from scanner import Scanner
from input_reader import InputReader
from output_writer import write_tokens
from errors import (
    ScannerError,
    InvalidCharError,
    InvalidIdentifierError,
    UnterminatedComment,
    InvalidCharacterError,
    UnterminatedCommentError,
    skip_whitespace_and_comments,
    skip_ignored,
    skipWhitespaceAndComments,
    skip_whitespace_and_comment,
    check_source,
    scan_text,
    fix_case,
)


def report_error(err, tokens):
    print(str(err))
    print(str(err), file=sys.stderr)
    write_tokens(tokens, "tokens_output.txt", error=str(err))


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input.tiny>")
        return

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as f:
            src = f.read()
    except FileNotFoundError:
        print("File not found.")
        return
    except Exception as e:
        print("Error:", e)
        return

    # One pass over the whole source: invalid characters, capitalised
    # reserved words and unterminated comments are all detected here.
    found = check_source(src, filename)
    if found is not None:
        err, pos = found
        # Only the tokens before the error are valid output.
        report_error(err, scan_text(src[:pos]))
        return

    reader = InputReader(filename)
    scanner = Scanner(reader)
    tokens = []
    err = None
    while True:
        try:
            token = scanner.get_token()
        except ScannerError as e:
            err = e
            break
        except Exception as e:
            err = e
            break
        if token is None:
            break
        tokens.append(token)
    fix_case(tokens)

    if err is None:
        write_tokens(tokens, "tokens_output.txt")
        print("Done. Tokens saved to tokens_output.txt")
    else:
        report_error(err, tokens)


if __name__ == "__main__":
    main()