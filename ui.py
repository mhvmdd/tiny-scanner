import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from scanner import Scanner
from input_reader import InputReader
from output_writer import write_tokens


class TinyScannerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tiny Scanner")
        self.root.geometry("700x550")

        # toolbar
        top = tk.Frame(root)
        top.pack(fill=tk.X)

        tk.Button(top, text="Open", command=self.open_file).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(top, text="Scan", command=self.scan_code).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(top, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(top, text="Save Tokens", command=self.save_tokens).pack(side=tk.LEFT, padx=2, pady=2)

        # input
        tk.Label(root, text="Source Code:").pack(anchor=tk.W, padx=5)
        self.code = tk.Text(root, height=18)
        self.code.pack(fill=tk.BOTH, expand=True, padx=5)

        # output
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

    def scan_code(self):
        self.tokens.delete("1.0", tk.END)
        self.tokens_list = []
        text = self.code.get("1.0", tk.END)

        # save temp file
        try:
            with open("temp_input.tiny", "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        # check for errors first
        i = 0
        line = 1
        col = 1
        n = len(text)
        while i < n:
            ch = text[i]
            if ch == '\n':
                line += 1
                col = 1
                i += 1
                continue
            if ch == '\r':
                if i + 1 < n and text[i + 1] == '\n':
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
                i += 1
                col += 1
                while i < n and text[i] != '}':
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
                if i < n and text[i] == '}':
                    i += 1
                    col += 1
                continue
            if ch.isalpha():
                while i < n and text[i].isalpha():
                    i += 1
                    col += 1
                continue
            if ch.isdigit():
                while i < n and text[i].isdigit():
                    i += 1
                    col += 1
                continue
            if ch == ':' and i + 1 < n and text[i + 1] == '=':
                i += 2
                col += 2
                continue
            if ch in ';<>=+-*/()':
                i += 1
                col += 1
                continue
            msg = f"Lexical error at line {line}, column {col}: invalid character {ch!r}"
            self.tokens.insert(tk.END, msg + "\n")
            messagebox.showerror("Error", msg)
            try:
                write_tokens([], "tokens_output.txt", error=msg)
            except:
                pass
            return

        try:
            reader = InputReader("temp_input.tiny")
            scanner = Scanner(reader)
            while True:
                token = scanner.get_token()
                if token is None:
                    break
                self.tokens_list.append(token)
                self.tokens.insert(tk.END, f"{token.value}, {token.type.name}\n")
            write_tokens(self.tokens_list, "tokens_output.txt")
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
