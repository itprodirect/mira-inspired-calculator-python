import tkinter as tk

class MiraCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mira // Demon Hunter Calc")
        self.configure(bg="#0b0213")
        self.resizable(False, False)

        # Color palette (Mira-inspired: neon magenta + dark stage)
        self.bg = "#0b0213"
        self.display_bg = "#1a0824"
        self.display_fg = "#fdf6ff"
        self.accent = "#ff2e9f"
        self.accent_secondary = "#5ef2ff"
        self.button_bg = "#24102f"
        self.button_hover = "#31183f"
        self.op_bg = "#3a1035"
        self.op_fg = "#ffb347"
        self.equal_bg = "#ff2e9f"
        self.equal_fg = "#0b0213"

        self.expression = ""

        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        # Header – gives it that “idol tech” vibe
        header = tk.Label(
            self,
            text="MIRA // DEMON HUNTER CALC",
            bg=self.bg,
            fg=self.accent_secondary,
            font=("Segoe UI", 11, "bold")
        )
        header.pack(padx=16, pady=(12, 4), anchor="w")

        # Display
        self.display_var = tk.StringVar(value="0")
        display = tk.Entry(
            self,
            textvariable=self.display_var,
            font=("Consolas", 24, "bold"),
            bg=self.display_bg,
            fg=self.display_fg,
            bd=0,
            relief="flat",
            justify="right",
            insertbackground=self.display_fg
        )
        display.pack(fill="x", padx=16, pady=(0, 16), ipady=10)

        # Buttons frame
        btn_frame = tk.Frame(self, bg=self.bg)
        btn_frame.pack(padx=16, pady=(0, 16))

        # Layout: C in top-left, ops on the right, wide 0 on bottom
        buttons = [
            ["C", "",  "",  "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", "0", ".", "="],  # first "0" is styled as wide
        ]

        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                if char == "":
                    # spacer cell
                    spacer = tk.Label(btn_frame, text="", bg=self.bg)
                    spacer.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
                    continue

                # Decide button style
                if char == "C":
                    bg = self.op_bg
                    fg = self.accent_secondary
                elif char in {"/", "*", "-", "+"}:
                    bg = self.op_bg
                    fg = self.op_fg
                elif char == "=":
                    bg = self.equal_bg
                    fg = self.equal_fg
                else:
                    bg = self.button_bg
                    fg = self.display_fg

                btn = tk.Button(
                    btn_frame,
                    text=char,
                    command=lambda ch=char: self.on_button_click(ch),
                    bg=bg,
                    fg=fg,
                    activebackground=self.button_hover,
                    activeforeground=fg,
                    bd=0,
                    relief="flat",
                    font=("Segoe UI", 14, "bold")
                )

                # Make the first 0 double width
                if r == 4 and c == 0:
                    btn.grid(row=r, column=c, columnspan=2, padx=4, pady=4, sticky="nsew")
                elif r == 4 and c == 1:
                    # skip, handled by col span
                    continue
                else:
                    btn.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

        # Make grid responsive
        cols = 4
        rows = 5
        for i in range(cols):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(rows):
            btn_frame.rowconfigure(i, weight=1)

    def _bind_keys(self):
        # Basic keyboard support
        for char in "0123456789+-*/.":
            self.bind(char, self.on_key)
        self.bind("<Return>", self.on_key)
        self.bind("<KP_Enter>", self.on_key)
        self.bind("<BackSpace>", self.on_key)
        self.bind("<Escape>", self.on_key)

    def on_button_click(self, char: str):
        if char == "C":
            self.expression = ""
            self.display_var.set("0")
            return
        if char == "=":
            self._evaluate()
            return

        # Build the expression string
        if self.display_var.get() == "0" and char not in {".", "+", "-", "*", "/"}:
            self.expression = char
        else:
            self.expression += char
        self.display_var.set(self.expression)

    def on_key(self, event):
        key = event.keysym

        if key in [str(i) for i in range(10)]:
            self.on_button_click(event.char)
        elif key in {"plus", "minus", "slash", "asterisk"}:
            mapping = {
                "plus": "+",
                "minus": "-",
                "slash": "/",
                "asterisk": "*",
            }
            self.on_button_click(mapping[key])
        elif key in {"period", "comma"}:
            self.on_button_click(".")
        elif key in {"Return", "KP_Enter"}:
            self._evaluate()
        elif key == "BackSpace":
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression if self.expression else "0")
        elif key == "Escape":
            self.expression = ""
            self.display_var.set("0")

    def _evaluate(self):
        try:
            # Using eval for a quick local calculator; for untrusted input, replace with a real parser
            result = eval(self.expression or "0")
            self.display_var.set(str(result))
            self.expression = str(result)
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

if __name__ == "__main__":
    app = MiraCalculator()
    app.mainloop()