# tiny-scanner

A scanner (lexical analyzer) for the TINY language, written in Python. It reads TINY source code and produces the list of tokens as `(tokenvalue, tokentype)` pairs. Built as the Scanner Project for our Compilers course.

## Features

- `getToken()` returns the next token from the input, with its string value and type
- Writes the full token list to an output file
- Recognizes all TINY tokens (see the table below)
- Reports invalid input with the line number instead of crashing
- Skips whitespace and `{ ... }` comments
- Packaged as a standalone Windows `.exe` (no Python or third-party tools needed)

## Example

Input (`sample.tiny`):

```
read x;
if x < 10 then
  x := x + 4
end
```

Output (`tokens_output.txt`):

```
read, read
x, Identifier
;, semicolon
if, if
x, Identifier
<, lessthan
10, number
then, then
x, Identifier
:=, assign
x, Identifier
+, plus
4, number
end, end
```

## Supported tokens

| Token type | Example |
|---|---|
| SEMICOLON | `;` |
| IF | `if` |
| THEN | `then` |
| END | `end` |
| REPEAT | `repeat` |
| UNTIL | `until` |
| IDENTIFIER | `x`, `abc`, `xyz` |
| ASSIGN | `:=` |
| READ | `read` |
| WRITE | `write` |
| LESSTHAN | `<` |
| EQUAL | `=` |
| PLUS | `+` |
| MINUS | `-` |
| MULT | `*` |
| DIV | `/` |
| OPENBRACKET | `(` |
| CLOSEDBRACKET | `)` |
| NUMBER | `12`, `289` |

## Getting started

Requirements: Python 3.10 or newer (only needed to run from source).

```bash
git clone https://github.com/<your-username>/tiny-scanner.git
cd tiny-scanner
python main.py path/to/sample.tiny
```

The token list is written to `tokens_output.txt`.

### Run the tests

```bash
python run_tests.py
```

### Build the Windows executable

```bash
pip install pyinstaller
pyinstaller --onefile main.py --name TinyScanner
```

The executable is created in `dist/TinyScanner.exe`.

## Project structure

```
tiny-scanner/
├── main.py             # entry point (UI/CLI)
├── scanner.py          # Scanner class and getToken()
├── tokens.py           # token types, Token class, reserved words
├── char_classes.py     # character classes and DFA transition table
├── input_reader.py     # reads the source file, lookahead, line tracking
├── output_writer.py    # writes the (tokenvalue, tokentype) file
├── errors.py           # error types and reporting
├── run_tests.py        # runs every sample and compares with expected output
├── test_samples/       # .tiny samples with matching _expected.txt files
└── docs/               # report and screenshots
```

## How it works

The scanner is a deterministic finite automaton (DFA) with these states: `START`, `INID`, `INNUM`, `INASSIGN`, `INCOMMENT` and `DONE`. `getToken()` reads characters one at a time, follows the transition table, and steps back one character (`unget_char`) when a token ends on a lookahead character. Identifiers are checked against the reserved-words table to separate keywords such as `if` and `repeat` from plain identifiers.

## Team

| Member | Responsibility |
|---|---|
| Member 1 | Scanner core (`scanner.py`) |
| Member 2 | DFA table and token definitions (`char_classes.py`, `tokens.py`) |
| Member 3 | UI/CLI and executable (`main.py`, `TinyScanner.exe`) |
| Member 4 | Error handling, comments and whitespace (`errors.py`) |
| Member 5 | Input/output and screenshots (`input_reader.py`, `output_writer.py`) |
| Member 6 | Testing, documentation and review (`run_tests.py`, `test_samples/`, `docs/`) |

Replace "Member N" with your names and GitHub usernames.

## Deliverables

1. Executable (`TinyScanner.exe`)
2. Screenshots of the program (`docs/screenshots/`)
3. Source code files

## License

For coursework use. Add a license here if you plan to make the repo public.
