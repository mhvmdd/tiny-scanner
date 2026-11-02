# Test samples

Each source file is named `NAME.tiny` and has one of two companion files.

## Expected tokens: `NAME_expected.txt`

The scanner is run on a copy of `NAME.tiny` and must produce
`tokens_output.txt` containing the same tokens:

```
value, tokentype
```

Blank lines and lines beginning with `#` are ignored. Whitespace around the
comma does not matter. Token types are compared case-insensitively, so
`Identifier` and `identifier` are equivalent; token values are compared
exactly.

## Expected error: `NAME_error.txt`

For invalid input, the file lists fragments (one per non-blank line, `#` for
comments). Every fragment must appear in the scanner's stdout, stderr, or
output file, and the scanner must not print a Python traceback. The scanner
may continue after the error or stop; only the presence and line number of
the message are checked.

## Adding a sample

1. Add `NAME.tiny`.
2. Add either `NAME_expected.txt` or `NAME_error.txt` (exactly one).
3. Run `python run_tests.py --sample NAME`.
