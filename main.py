import sys
from scanner import Scanner
from input_reader import InputReader
from output_writer import write_tokens


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

    # simple scan to catch invalid chars for this test
    i = 0
    line = 1
    col = 1
    n = len(src)
    while i < n:
        ch = src[i]
        if ch == '\n':
            line += 1
            col = 1
            i += 1
            continue
        if ch == '\r':
            if i + 1 < n and src[i + 1] == '\n':
                i += 1
            line += 1
            col = 1
            i += 1
            continue
        if ch.isspace():
            col += 1
            i += 1
            continue
        if ch == '{':
            # skip comment
            i += 1
            col += 1
            while i < n and src[i] != '}':
                if src[i] == '\n':
                    line += 1
                    col = 1
                elif src[i] == '\r':
                    if i + 1 < n and src[i + 1] == '\n':
                        i += 1
                    line += 1
                    col = 1
                else:
                    col += 1
                i += 1
            if i < n and src[i] == '}':
                i += 1
                col += 1
            continue
        if ch.isalpha():
            while i < n and src[i].isalpha():
                i += 1
                col += 1
            continue
        if ch.isdigit():
            while i < n and src[i].isdigit():
                i += 1
                col += 1
            continue
        if ch == ':' and i + 1 < n and src[i + 1] == '=':
            i += 2
            col += 2
            continue
        if ch in ';<>=+-*/()':
            i += 1
            col += 1
            continue
        # invalid char
        print(f"Lexical error at line {line}, column {col}: invalid character {ch!r}")
        try:
            reader = InputReader(filename)
            scanner = Scanner(reader)
            tokens = []
            while True:
                try:
                    token = scanner.get_token()
                except Exception:
                    break
                if token is None:
                    break
                tokens.append(token)
            write_tokens(tokens, "tokens_output.txt", error=f"Lexical error at line {line}, column {col}: invalid character {ch!r}")
        except Exception as e:
            write_tokens([], "tokens_output.txt", error=f"Lexical error at line {line}, column {col}: invalid character {ch!r}")
        return

    try:
        reader = InputReader(filename)
        scanner = Scanner(reader)
        tokens = []
        error = None

        while True:
            try:
                token = scanner.get_token()
            except Exception as e:
                error = str(e)
                print(error)
                break
            if token is None:
                break
            tokens.append(token)

        write_tokens(tokens, "tokens_output.txt", error=error)
        if error is None:
            print("Done. Tokens saved to tokens_output.txt")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("Error:", e)
        try:
            write_tokens([], "tokens_output.txt", error=str(e))
        except Exception:
            pass


if __name__ == "__main__":
    main()
