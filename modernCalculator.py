import ast
import operator
import tkinter as tk
from tkinter import ttk


class CalculatorApp:
    """Modern calculator desktop application built with Tkinter."""

    WINDOW_WIDTH = 360
    WINDOW_HEIGHT = 520
    ERROR_MESSAGES = {"Invalid Expression", "Cannot divide by zero"}

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.expression = ""
        self.history_items: list[str] = []
        self.display_var = tk.StringVar(value="0")

        self.colors = {
            "window": "#14161a",
            "panel": "#1b1f26",
            "entry": "#0f1218",
            "digit": "#252b35",
            "digit_hover": "#303744",
            "operator": "#ff9f43",
            "operator_hover": "#ffb15e",
            "equals": "#00b894",
            "equals_hover": "#19d0a9",
            "clear": "#ff5c5c",
            "clear_hover": "#ff7676",
            "backspace": "#4d6480",
            "backspace_hover": "#5d7a9e",
            "text_primary": "#f5f7fa",
            "text_secondary": "#9ea7b3",
            "history_bg": "#171b22",
        }

        self.safe_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
        }

        self.configure_window()
        self.create_styles()
        self.create_layout()
        self.bind_keyboard()

    def configure_window(self) -> None:
        """Configure the main application window."""
        self.root.title("Modern Calculator")
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=self.colors["window"])

        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_pos = (screen_width - self.WINDOW_WIDTH) // 2
        y_pos = (screen_height - self.WINDOW_HEIGHT) // 2
        self.root.geometry(
            f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x_pos}+{y_pos}"
        )

    def create_styles(self) -> None:
        """Create ttk styles for the history panel."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "History.TLabel",
            background=self.colors["panel"],
            foreground=self.colors["text_secondary"],
            font=("Segoe UI", 10, "bold"),
        )

    def create_layout(self) -> None:
        """Build and place all calculator widgets."""
        container = tk.Frame(self.root, bg=self.colors["window"])
        container.pack(fill="both", expand=True, padx=16, pady=16)

        display_frame = tk.Frame(
            container,
            bg=self.colors["panel"],
            bd=0,
            highlightthickness=0,
            padx=14,
            pady=14,
        )
        display_frame.pack(fill="x", pady=(0, 12))

        display_entry = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            justify="right",
            font=("Segoe UI Semibold", 24),
            bd=0,
            relief="flat",
            bg=self.colors["entry"],
            fg=self.colors["text_primary"],
            insertbackground=self.colors["text_primary"],
            state="readonly",
            readonlybackground=self.colors["entry"],
        )
        display_entry.pack(fill="x", ipady=14)

        history_frame = tk.Frame(container, bg=self.colors["panel"], padx=12, pady=10)
        history_frame.pack(fill="x", pady=(0, 12))

        history_label = ttk.Label(history_frame, text="History", style="History.TLabel")
        history_label.pack(anchor="w", pady=(0, 8))

        self.history_listbox = tk.Listbox(
            history_frame,
            height=4,
            bg=self.colors["history_bg"],
            fg=self.colors["text_secondary"],
            bd=0,
            highlightthickness=0,
            selectbackground=self.colors["digit_hover"],
            activestyle="none",
            font=("Segoe UI", 10),
        )
        self.history_listbox.pack(fill="x")

        buttons_frame = tk.Frame(container, bg=self.colors["window"])
        buttons_frame.pack(fill="both", expand=True)

        for column in range(4):
            buttons_frame.grid_columnconfigure(column, weight=1, uniform="button")
        for row in range(5):
            buttons_frame.grid_rowconfigure(row, weight=1, uniform="button")

        buttons = [
            ("C", 0, 0, 1, 1, self.colors["clear"], self.colors["clear_hover"]),
            ("⌫", 0, 1, 1, 1, self.colors["backspace"], self.colors["backspace_hover"]),
            ("/", 0, 2, 1, 1, self.colors["operator"], self.colors["operator_hover"]),
            ("*", 0, 3, 1, 1, self.colors["operator"], self.colors["operator_hover"]),
            ("7", 1, 0, 1, 1, self.colors["digit"], self.colors["digit_hover"]),
            ("8", 1, 1, 1, 1, self.colors["digit"], self.colors["digit_hover"]),
            ("9", 1, 2, 1, 1, self.colors["digit"], self.colors["digit_hover"]),
            ("-", 1, 3, 1, 1, self.colors["operator"], self.colors["operator_hover"]),
            ("4", 2, 0, 1, 1, self.colors["digit"], self.colors["digit_hover"]),
            ("5", 2, 1, 1, 1, self.colors["digit"], self.colors["digit_hover"]),
            ("6", 2, 2, 1, 1, self.colors["digit"], self.colors["digit_hover"]),
            ("+", 2, 3, 1, 1, self.colors["operator"], self.colors["operator_hover"]),
            ("1", 3, 0, 1, 1, self.colors["digit"], self.colors["digit_hover"]),
            ("2", 3, 1, 1, 1, self.colors["digit"], self.colors["digit_hover"]),
            ("3", 3, 2, 1, 1, self.colors["digit"], self.colors["digit_hover"]),
            ("=", 3, 3, 2, 1, self.colors["equals"], self.colors["equals_hover"]),
            ("0", 4, 0, 1, 2, self.colors["digit"], self.colors["digit_hover"]),
            (".", 4, 2, 1, 1, self.colors["digit"], self.colors["digit_hover"]),
        ]

        for text, row, column, rowspan, colspan, color, hover in buttons:
            self.create_button(
                parent=buttons_frame,
                text=text,
                row=row,
                column=column,
                rowspan=rowspan,
                colspan=colspan,
                color=color,
                hover_color=hover,
            )

    def create_button(
        self,
        parent: tk.Frame,
        text: str,
        row: int,
        column: int,
        rowspan: int,
        colspan: int,
        color: str,
        hover_color: str,
    ) -> None:
        """Create a styled calculator button with hover feedback."""
        button = tk.Button(
            parent,
            text=text,
            font=("Segoe UI Semibold", 16),
            bg=color,
            fg=self.colors["text_primary"],
            activebackground=hover_color,
            activeforeground=self.colors["text_primary"],
            bd=0,
            relief="flat",
            cursor="hand2",
            command=lambda value=text: self.handle_button_click(value),
        )
        button.grid(
            row=row,
            column=column,
            rowspan=rowspan,
            columnspan=colspan,
            sticky="nsew",
            padx=6,
            pady=6,
            ipadx=4,
            ipady=10,
        )

        button.bind("<Enter>", lambda event, widget=button: widget.config(bg=hover_color))
        button.bind("<Leave>", lambda event, widget=button: widget.config(bg=color))

    def bind_keyboard(self) -> None:
        """Attach useful keyboard shortcuts."""
        self.root.bind("<Key>", self.handle_keypress)
        self.root.bind("<Return>", lambda event: self.calculate())
        self.root.bind("<KP_Enter>", lambda event: self.calculate())
        self.root.bind("<Escape>", lambda event: self.clear_display())
        self.root.bind("<BackSpace>", lambda event: self.backspace())

    def handle_keypress(self, event: tk.Event) -> None:
        """Process keyboard input for numbers, operators, and decimal points."""
        allowed_keys = "0123456789+-*/()."
        key = event.char

        if key in allowed_keys:
            self.click(key)

    def handle_button_click(self, value: str) -> None:
        """Route button actions to their matching handlers."""
        if value == "C":
            self.clear_display()
        elif value == "⌫":
            self.backspace()
        elif value == "=":
            self.calculate()
        else:
            self.click(value)

    def click(self, value: str) -> None:
        """Append a value to the current expression and refresh the display."""
        if self.display_var.get() in self.ERROR_MESSAGES:
            self.expression = ""

        if value in "+*/" and not self.expression:
            return

        if value == "-" and self.expression == "0":
            self.expression = "-"
            self.update_display(self.expression)
            return

        if value in "+-*/" and self.expression.endswith(("+", "-", "*", "/", ".")):
            self.expression = self.expression[:-1] + value
            self.update_display(self.expression or "0")
            return

        if value == "." and not self.can_add_decimal():
            return

        if value == "." and (not self.expression or self.expression.endswith(("+", "-", "*", "/"))):
            self.expression += "0."
        elif self.display_var.get() == "0" and value not in "+-*/.":
            self.expression = value
        else:
            self.expression += value

        self.update_display(self.expression or "0")

    def clear_display(self) -> None:
        """Reset the calculator display and current expression."""
        self.expression = ""
        self.update_display("0")

    def backspace(self) -> None:
        """Remove the last character from the expression."""
        if self.display_var.get() in self.ERROR_MESSAGES:
            self.clear_display()
            return

        self.expression = self.expression[:-1]
        self.update_display(self.expression or "0")

    def calculate(self) -> None:
        """Evaluate the current expression and show the result."""
        if not self.expression:
            return

        try:
            result = self.safe_evaluate(self.expression)
            formatted_result = self.format_result(result)
            self.add_to_history(self.expression, formatted_result)
            self.expression = formatted_result
            self.update_display(formatted_result)
        except ZeroDivisionError:
            self.expression = ""
            self.update_display("Cannot divide by zero")
        except (SyntaxError, TypeError, ValueError):
            self.expression = ""
            self.update_display("Invalid Expression")

    def safe_evaluate(self, expression: str) -> float:
        """Safely evaluate arithmetic expressions using an AST parser."""
        parsed = ast.parse(expression, mode="eval")
        return self.evaluate_node(parsed.body)

    def evaluate_node(self, node: ast.AST) -> float:
        """Recursively evaluate supported AST nodes."""
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.Num):
            return node.n

        if isinstance(node, ast.BinOp) and type(node.op) in self.safe_operators:
            left_value = self.evaluate_node(node.left)
            right_value = self.evaluate_node(node.right)
            return self.safe_operators[type(node.op)](left_value, right_value)

        if isinstance(node, ast.UnaryOp) and type(node.op) in self.safe_operators:
            operand_value = self.evaluate_node(node.operand)
            return self.safe_operators[type(node.op)](operand_value)

        raise ValueError("Unsupported expression")

    def can_add_decimal(self) -> bool:
        """Prevent multiple decimal points inside the same number segment."""
        number_segment = ""

        for character in reversed(self.expression):
            if character in "+-*/()":
                break
            number_segment = character + number_segment

        return "." not in number_segment

    def format_result(self, value: float) -> str:
        """Format results to avoid unnecessary trailing decimal places."""
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return f"{value:.10g}"

    def add_to_history(self, expression: str, result: str) -> None:
        """Store recent calculations in the history panel."""
        history_entry = f"{expression} = {result}"
        self.history_items.append(history_entry)
        self.history_items = self.history_items[-4:]

        self.history_listbox.delete(0, tk.END)
        for item in reversed(self.history_items):
            self.history_listbox.insert(tk.END, item)

    def update_display(self, value: str) -> None:
        """Refresh the display text."""
        self.display_var.set(value)


def main() -> None:
    """Start the calculator application."""
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
