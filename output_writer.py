from tokens import Token

def write_tokens(tokens: list[Token],
                 filename: str = "tokens_output.txt") -> None:
    
    with open(filename, "w", encoding="utf-8") as file:
        for token in tokens:
            file.write(f"{token.value}, {token.type.name}\n")