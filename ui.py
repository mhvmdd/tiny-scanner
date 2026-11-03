import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from scanner import Scanner
from input_reader import InputReader
from output_writer import write_tokens
from errors import (
    ScannerError,
    check_source,
    scan_text,
    fix_case,
)


class TinyScannerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tiny Scanner")
        self.root.geometry("700x550")

        top = tk.Frame(root)
        top.pack(fill=tk.X)

        tk.Button(top, text="Open", command=self.open_file).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(top, text="Scan", command=self.scan_code).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(top, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(top, text="Save Tokens", command=self.save_tokens).pack(side=tk.LEFT, padx=2, pady=2)

        tk.Label(root, text="Source Code:").pack(anchor=tk.W, padx=5)
        self.code = tk.Text(root, height=18)
        self.code.pack(fill=tk.BOTH, expand=True, padx=5)

        tk.Label(root, text="Tokens:").pack(anchor=tk.W, padx=5)
        self.tokens = tk.Text(root, height=12)
        self.tokens.pack(fill=tk.BOTH, expand=True, padx=5)

        self.tokens_list = []

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Tiny files", "*.tiny"), ("All files", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.code.delete("1.0", tk.END)
                self.code.insert("1.0", f.read())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_error(self, err, tokens):
        """Show valid tokens, then the error, and save everything to the output file."""
        msg = str(err)
        self.tokens_list = tokens
        for t in tokens:
            self.tokens.insert(tk.END, f"{t.value}, {t.type.name}\n")
        self.tokens.insert(tk.END, msg + "\n")
        write_tokens(tokens, "tokens_output.txt", error=msg)
        messagebox.showerror("Error", msg)

    def scan_code(self):
        self.tokens.delete("1.0", tk.END)
        self.tokens_list = []
        # Always read the CURRENT contents of the editor.
        text = self.code.get("1.0", "end-1c")

        try:
            with open("temp_input.tiny", "w", encoding="utf-8", newline="") as f:
                f.write(text)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        # One pass over the whole source: invalid characters, capitalised
        # reserved words and unterminated comments are all detected here.
        found = check_source(text, "temp_input.tiny")
        if found is not None:
            err, pos = found
            self.show_error(err, scan_text(text[:pos]))
            return

        try:
            reader = InputReader("temp_input.tiny")
            scanner = Scanner(reader)
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
                fix_case([token])
                self.tokens_list.append(token)
                self.tokens.insert(tk.END, f"{token.value}, {token.type.name}\n")
            if err is None:
                write_tokens(self.tokens_list, "tokens_output.txt")
            else:
                self.show_error(err, self.tokens_list)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_tokens(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not path:
            return
        try:
            write_tokens(self.tokens_list, path)
            messagebox.showinfo("Saved", "Tokens saved")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear(self):
        self.code.delete("1.0", tk.END)
        self.tokens.delete("1.0", tk.END)
        self.tokens_list = []


if __name__ == "__main__":
    root = tk.Tk()
    app = TinyScannerUI(root)
    root.mainloop()