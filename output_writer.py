from tokens import Token

def write_tokens(tokens: list[Token],
                 filename: str = "tokens_output.txt",error: str | None = None) -> None:
    
    with open(filename, "w", encoding="utf-8") as file:
        # Write all successfully recognized tokens
        for token in tokens:
            file.write(f"{token.value}, {token.type.name}\n")

        # Write the error if one occurred
        if error is not None:
            file.write(f"{error}\n")