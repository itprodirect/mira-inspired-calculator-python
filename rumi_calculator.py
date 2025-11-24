import tkinter as tk


class RumiCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Rumi // Demon Hunter Calc")
        self.configure(bg="#050814")  # dark concert stage
        self.resizable(False, False)

        # Rumi-inspired palette (pink + aqua neon)
        self.bg = "#050814"
        self.display_bg = "#150d29"
        self.display_fg = "#fef7ff"
        self.accent = "#ff6ad5"           # Rumi pink
        self.accent_secondary = "#6af2ff"  # aqua highlight
        self.button_bg = "#241236"
        self.button_hover = "#341b4a"
        self.op_bg = "#3a163b"
        self.op_fg = "#ffd37a"
        self.equal_bg = "#ff6ad5"
        self.equal_fg = "#050814"

        self.expression = ""

        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        # Header – this MUST say RUMI now
        header = tk.Label(
            self,
            text="RUMI // DEMON HUNTER CALC",
            bg=self.bg,
            fg=self.accent_secondary,
            font=("Segoe UI", 11, "bold"),
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
            insertbackground=self.display_fg,
        )
        display.pack(fill="x", padx=16, pady=(0, 16), ipady=10)

        # Buttons frame
        btn_frame = tk.Frame(self, bg=self.bg)
        btn_frame.pack(padx=16, pady=(0, 16))

        buttons = [
            ["C", "", "", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", "0", ".", "="],  # first 0 is wide
        ]

        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                if char == "":
                    spacer = tk.Label(btn_frame, text="", bg=self.bg)
                    spacer.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
                    continue

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
                    font=("Segoe UI", 14, "bold"),
                )

                if r == 4 and c == 0:
                    btn.grid(
                        row=r,
                        column=c,
                        columnspan=2,
                        padx=4,
                        pady=4,
                        sticky="nsew",
                    )
                elif r == 4 and c == 1:
                    continue
                else:
                    btn.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

        cols, rows = 4, 5
        for i in range(cols):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(rows):
            btn_frame.rowconfigure(i, weight=1)

    def _bind_keys(self):
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
            result = eval(self.expression or "0")
            self.display_var.set(str(result))
            self.expression = str(result)
        except Exception:
            self.display_var.set("Error")
            self.expression = ""


if __name__ == "__main__":
    app = RumiCalculator()
    app.mainloop()
