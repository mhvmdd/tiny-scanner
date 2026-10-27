
class InputReader:
    def __init__(self, filename):
        # Read the source file
        with open(filename, "r", encoding="utf-8") as file:
            self.source = file.read()

        self.position = 0
        self.line_number = 1
        self.last_char = None
        self.previous_line = 1
        self.can_unget = False

    def next_char(self):
    
        if self.position >= len(self.source):# Check for end of file
            self.can_unget = False
            return None

        self.previous_line = self.line_number# Save the current 
        char = self.source[self.position]
        self.position += 1

        # Update line number
        if char == "\n":
            self.line_number += 1

        self.last_char = char
        self.can_unget = True

        return char

    def unget_char(self):
        if not self.can_unget:
            return False

        self.position -= 1
        self.line_number = self.previous_line
        self.can_unget = False

        return True

    def get_line_number(self):
        return self.line_number
