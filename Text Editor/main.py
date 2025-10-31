import tkinter as tk
from tkinter import filedialog, messagebox

PYTHON_KEYWORDS = [
    "def",
    "class",
    "if",
    "elif",
    "else",
    "try",
    "except",
    "for",
    "while",
    "import",
    "from",
    "as",
    "return",
    "with",
    "lambda",
    "True",
    "False",
    "None",
    "in",
    "not",
    "and",
    "or",
    "break",
    "continue",
    "pass",
    "global",
    "nonlocal",
    "raise",
    "yield",
    "assert",
    "print",
    "input",
]


class TextEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Text Editor")
        self.root.geometry("800x600")

        self.file_path = None

        self._create_widgets()
        self._create_menu()
        self._bind_shortcuts()

        self.root.mainloop()

    def _create_widgets(self):
        self.line_numbers = tk.Text(
            self.root,
            width=4,
            padx=5,
            takefocus=0,
            border=0,
            background="#f0f0f0",
            state="disabled",
        )
        self.line_numbers.pack(side="left", fill="y")

        self.text = tk.Text(self.root, wrap="none", undo=True, font=("Consolas", 12))
        self.text.pack(fill="both", expand=True)

        self.text.bind("<KeyRelease>", self._on_key_release)
        self.text.bind("<Button-1>", lambda e: self._update_line_numbers())
        self.text.bind("<MouseWheel>", lambda e: self._update_line_numbers())

        self._configure_tags()

    def _configure_tags(self):
        self.text.tag_config("keyword", foreground="magenta")
        self.text.tag_config("string", foreground="green")
        self.text.tag_config("comment", foreground="gray")

    def _on_key_release(self, event=None):
        self._highlight_syntax()
        self._update_line_numbers()

    def _highlight_syntax(self):
        content = self.text.get("1.0", "end-1c")
        self.text.tag_remove("keyword", "1.0", "end")
        self.text.tag_remove("string", "1.0", "end")
        self.text.tag_remove("comment", "1.0", "end")

        lines = content.split("\n")
        for i, line in enumerate(lines):
            index = f"{i+1}.0"
            words = line.split(" ")
            pos = 0
            while pos < len(line):
                for word in PYTHON_KEYWORDS:
                    if line[pos:].startswith(word) and (
                        pos + len(word) == len(line)
                        or not line[pos + len(word)].isalnum()
                    ):
                        self.text.tag_add(
                            "keyword", f"{i+1}.{pos}", f"{i+1}.{pos+len(word)}"
                        )
                if line[pos] == "#":
                    self.text.tag_add("comment", f"{i+1}.{pos}", f"{i+1}.end")
                    break
                elif line[pos] in ("'", '"'):
                    quote = line[pos]
                    end = pos + 1
                    while end < len(line) and line[end] != quote:
                        end += 1
                    end = min(end + 1, len(line))
                    self.text.tag_add("string", f"{i+1}.{pos}", f"{i+1}.{end}")
                    pos = end - 1
                pos += 1

    def _update_line_numbers(self):
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")

        line_count = int(self.text.index("end-1c").split(".")[0])
        line_text = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.insert("1.0", line_text)
        self.line_numbers.config(state="disabled")

    def _create_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(
            label="Open", command=self.open_file, accelerator="Ctrl+O"
        )
        file_menu.add_command(
            label="Save", command=self.save_file, accelerator="Ctrl+S"
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(
            label="Undo", command=lambda: self.text.edit_undo(), accelerator="Ctrl+Z"
        )
        edit_menu.add_command(
            label="Redo", command=lambda: self.text.edit_redo(), accelerator="Ctrl+Y"
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Cut",
            command=lambda: self.text.event_generate("<<Cut>>"),
            accelerator="Ctrl+X",
        )
        edit_menu.add_command(
            label="Copy",
            command=lambda: self.text.event_generate("<<Copy>>"),
            accelerator="Ctrl+C",
        )
        edit_menu.add_command(
            label="Paste",
            command=lambda: self.text.event_generate("<<Paste>>"),
            accelerator="Ctrl+V",
        )
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.root.config(menu=menu_bar)

    def _bind_shortcuts(self):
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-z>", lambda e: self.text.edit_undo())
        self.root.bind("<Control-y>", lambda e: self.text.edit_redo())

    def new_file(self):
        self.text.delete("1.0", tk.END)
        self.file_path = None
        self.root.title("Untitled - Pure Text Editor")
        self._update_line_numbers()

    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Python Files", "*.py"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*"),
            ]
        )
        if path:
            with open(path, "r") as file:
                content = file.read()
            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", content)
            self.file_path = path
            self.root.title(f"{path} - Pure Text Editor")
            self._highlight_syntax()
            self._update_line_numbers()

    def save_file(self):
        if not self.file_path:
            path = filedialog.asksaveasfilename(
                filetypes=[
                    ("Python Files", "*.py"),
                    ("Text Files", "*.txt"),
                    ("All Files", "*.*"),
                ],
            )
            if not path:
                return
            self.file_path = path

        with open(self.file_path, "w") as file:
            content = self.text.get("1.0", tk.END)
            file.write(content)
        self.root.title(f"{self.file_path} - Text Editor")


def main():
    TextEditor()


if __name__ == "__main__":
    main()
