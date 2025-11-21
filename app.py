import tkinter as tk
import random
import math
import re

# --- CONFIGURATION ---


class MiraConfig:
    """Centralized configuration for Theme and Settings."""
    TITLE = "MIRA // DEMON HUNTER [SCIENTIFIC MODE]"

    # Palette
    BG_COLOR = "#0b0213"       # Deep Void
    DISPLAY_BG = "#1a0824"     # Dark Stage
    TEXT_COLOR = "#fdf6ff"     # Starlight White
    NEON_PINK = "#ff2e9f"      # Mira Pink
    NEON_BLUE = "#5ef2ff"      # Cyber Blue
    BTN_COLOR = "#24102f"      # Key Dark
    OP_BG = "#3a1035"          # Operator Dark
    SCI_BG = "#1e2842"         # Scientific Dark (Blue-ish)
    OP_TEXT = "#ffb347"        # Warning Orange

    # Fonts
    FONT_DISPLAY = ("Consolas", 24, "bold")
    FONT_BTN = ("Segoe UI", 12, "bold")
    FONT_HEADER = ("Segoe UI", 10, "bold")

    QUOTES = [
        "CALCULATING TRAJECTORY...", "SYSTEM: SCIENTIFIC MODE",
        "QUANTUM SOLVER ONLINE", "MIRA SAYS: DO THE MATH!",
        "OPTIMIZING ALGORITHMS...", "TARGET: LOCKED"
    ]

# --- LOGIC ENGINE ---


class ScientificEngine:
    """
    Handles safe evaluation of scientific math.
    """

    SAFE_CONTEXT = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log10,
        "ln": math.log,
        "sqrt": math.sqrt,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
        "pow": math.pow,
        "radians": math.radians,
        "degrees": math.degrees,
        "fact": math.factorial
    }

    @staticmethod
    def prepare_expression(expression: str) -> str:
        """
        Translates visual symbols to Python syntax.
        Cybersecurity: This acts as a sanitation layer before eval.
        """
        if not expression:
            return ""

        # 1. Replace visual symbols with python operators
        expr = expression.replace("π", "pi")
        expr = expression.replace("^", "**")
        expr = expression.replace("√", "sqrt")

        # 2. Handle implicit multiplication
        # FIX: We must escape literal parenthesis with \

        # Case: "2sin" or "2(" -> "2*sin" or "2*("
        # Matches a digit followed immediately by a letter or open paren
        expr = re.sub(r'(\d)([a-z\(])', r'\1*\2', expr)

        # Case: ")3" or ")x" -> ")*3" or ")*x"
        # Matches a closing paren followed immediately by a letter or digit
        # FIXED: Added slash before ) -> r'\)'
        expr = re.sub(r'\)([a-z0-9])', r')*\1', expr)

        return expr

    @staticmethod
    def calculate(expression: str) -> str:
        try:
            if not expression:
                return ""

            # Translate to Python syntax
            py_expr = ScientificEngine.prepare_expression(expression)

            # Security: Use globals=None, locals=SAFE_CONTEXT
            result = eval(py_expr, {"__builtins__": None},
                          ScientificEngine.SAFE_CONTEXT)

            if isinstance(result, complex):
                return "Complex Error"

            if isinstance(result, float) and result.is_integer():
                return str(int(result))

            return str(round(result, 8))

        except ZeroDivisionError:
            return "DIV/0 ERROR"
        except ValueError:
            return "DOMAIN ERROR"
        except SyntaxError:
            return "SYNTAX ERROR"
        except Exception as e:
            print(f"Debug Error: {e}")  # Check console if it fails
            return "MISS!"

# --- MAIN APPLICATION ---


class MiraScientific(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(MiraConfig.TITLE)
        self.configure(bg=MiraConfig.BG_COLOR)
        self.resizable(False, False)

        self.expression = ""
        self.should_reset = False

        self._build_ui()
        self._bind_keys()
        self._update_status_loop()

    def _build_ui(self):
        self.header_var = tk.StringVar(value="SYSTEM ONLINE // SCI-MODE")
        tk.Label(
            self, textvariable=self.header_var, bg=MiraConfig.BG_COLOR,
            fg=MiraConfig.NEON_BLUE, font=MiraConfig.FONT_HEADER, anchor="w"
        ).pack(padx=20, pady=(15, 5), fill="x")

        self.display_var = tk.StringVar(value="0")
        display = tk.Entry(
            self, textvariable=self.display_var, font=MiraConfig.FONT_DISPLAY,
            bg=MiraConfig.DISPLAY_BG, fg=MiraConfig.TEXT_COLOR, bd=0,
            relief="flat", justify="right", insertbackground=MiraConfig.NEON_PINK
        )
        display.pack(fill="x", padx=20, pady=(0, 20), ipady=15)

        btn_frame = tk.Frame(self, bg=MiraConfig.BG_COLOR)
        btn_frame.pack(padx=15, pady=(0, 20))

        # Layout: 5 Columns
        # Note: I fixed the bottom row. We use "SKIP" to tell the loop
        # to ignore that spot because the previous button ("0") is wide.
        layout = [
            ["(",   ")",   "C",   "DEL",  "AC"],
            ["sin", "cos", "tan", "sqrt", "^"],
            ["ln",  "log", "pi",  "e",    "%"],
            ["7",   "8",   "9",   "/",    "*"],
            ["4",   "5",   "6",   "-",    "+"],
            ["1",   "2",   "3",   ".",    "="],
            ["0",   "SKIP", "00",  "",     ""]
        ]

        for r, row in enumerate(layout):
            for c, char in enumerate(row):
                if char == "" or char == "SKIP":
                    continue

                # Color & Logic
                def cmd(ch=char): return self.on_button_click(ch)

                if char in {"C", "AC", "DEL"}:
                    bg, fg = MiraConfig.OP_BG, MiraConfig.NEON_PINK
                elif char == "=":
                    bg, fg = MiraConfig.NEON_PINK, MiraConfig.BG_COLOR
                elif char in {"sin", "cos", "tan", "log", "ln", "sqrt", "^", "(", ")", "pi", "e"}:
                    bg, fg = MiraConfig.SCI_BG, MiraConfig.NEON_BLUE
                elif char in {"/", "*", "-", "+", "%"}:
                    bg, fg = MiraConfig.OP_BG, MiraConfig.OP_TEXT
                else:
                    bg, fg = MiraConfig.BTN_COLOR, MiraConfig.TEXT_COLOR

                btn = tk.Button(
                    btn_frame, text=char, bg=bg, fg=fg,
                    activebackground=MiraConfig.NEON_BLUE, activeforeground=MiraConfig.BG_COLOR,
                    bd=0, relief="flat", font=MiraConfig.FONT_BTN, cursor="hand2",
                    command=cmd
                )

                # Grid Placement
                if char == "0":
                    # Span 2 columns
                    btn.grid(row=r, column=c, columnspan=2,
                             padx=3, pady=3, sticky="nsew")
                else:
                    btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")

        # Grid Weights
        for i in range(5):
            btn_frame.columnconfigure(i, weight=1, minsize=60)
        for i in range(len(layout)):
            btn_frame.rowconfigure(i, weight=1, minsize=50)

    def _bind_keys(self):
        self.bind("<Return>", lambda e: self.on_button_click("="))
        self.bind("<KP_Enter>", lambda e: self.on_button_click("="))
        self.bind("<Escape>", lambda e: self.on_button_click("AC"))
        self.bind("<BackSpace>", lambda e: self.on_button_click("DEL"))
        for char in "0123456789+-*/.()^%":
            self.bind(char, lambda e, c=char: self.on_button_click(c))

    def _update_status_loop(self):
        if random.random() > 0.8:
            self.header_var.set(random.choice(MiraConfig.QUOTES))
        self.after(3000, self._update_status_loop)

    def on_button_click(self, char):
        if char == "AC":
            self.expression = ""
            self.display_var.set("0")
            self.should_reset = False
            return

        if char == "C" or char == "DEL":
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression if self.expression else "0")
            return

        if char == "=":
            result = ScientificEngine.calculate(self.expression)
            self.display_var.set(result)
            if "ERROR" in result or "MISS" in result:
                self.expression = ""
            else:
                self.expression = result
                self.should_reset = True
            return

        if self.should_reset:
            if char in "0123456789sin(logpi":
                self.expression = ""
            self.should_reset = False

        # Auto-add parenthesis for functions
        if char in ["sin", "cos", "tan", "log", "ln", "sqrt"]:
            self.expression += char + "("
        else:
            self.expression += char

        self.display_var.set(self.expression)


if __name__ == "__main__":
    app = MiraScientific()
    app.mainloop()
