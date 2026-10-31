# tiny-scanner

A scanner (lexical analyzer) for the TINY language, written in Python. It reads TINY source code and produces a list of tokens as `(tokenvalue, tokentype)` pairs.

## Features

- Scans TINY code using a DFA
- Skips whitespace and `{ ... }` comments
- Reports invalid characters with line and column numbers using `errors.py`
- Simple GUI (`ui.py`) to write and scan code
- CLI (`main.py`) to scan from a `.tiny` file
- Can be built as a standalone Windows `.exe`

## Example

Input:

```
read x;
if x < 10 then
  x := x + 4
end
```

Output (`tokens_output.txt`):

```
read, READ
x, IDENTIFIER
;, SEMICOLON
if, IF
x, IDENTIFIER
<, LESSTHAN
10, NUMBER
then, THEN
x, IDENTIFIER
:=, ASSIGN
x, IDENTIFIER
+, PLUS
4, NUMBER
end, END
```

## Supported Tokens

| Token | Example |
|---|---|
| SEMICOLON | `;` |
| IF | `if` |
| THEN | `then` |
| END | `end` |
| REPEAT | `repeat` |
| UNTIL | `until` |
| READ | `read` |
| WRITE | `write` |
| ASSIGN | `:=` |
| LESSTHAN | `<` |
| EQUAL | `=` |
| PLUS | `+` |
| MINUS | `-` |
| MULT | `*` |
| DIV | `/` |
| OPENBRACKET | `(` |
| CLOSEDBRACKET | `)` |
| IDENTIFIER | `x`, `abc` |
| NUMBER | `0`, `123` |

## How to Run

### GUI
```bash
python ui.py
```

### CLI
```bash
python main.py sample.tiny
```

Tokens are saved to `tokens_output.txt`.

## Testing

```bash
python run_tests.py
```

## Build EXE
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name TinyScanner ui.py
```

The exe will be in `dist/TinyScanner.exe`

## Project Files

```text
tiny-scanner/
├── main.py         # CLI
├── ui.py           # GUI
├── scanner.py      # Scanner
├── input_reader.py # Input
├── output_writer.py# Output
├── tokens.py       # Token types
├── char_classes.py # DFA
├── errors.py       # Error handling
├── run_tests.py    # Tests
└── test_samples/   # Test cases
```

## Team

| Member | Task |
|---|---|
| Member 1 | Scanner core (`scanner.py`) |
| Member 2 | Tokens & DFA (`tokens.py`, `char_classes.py`) |
| Member 3 | UI & EXE (`ui.py`, `main.py`) |
| Member 4 | Error handling (`errors.py`) |
| Member 5 | Input & Output (`input_reader.py`, `output_writer.py`) |
| Member 6 | Testing (`run_tests.py`, `test_samples/`) |
