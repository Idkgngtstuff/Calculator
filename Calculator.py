import tkinter as tk
import math
import ast
import operator

class functions:
    def sqrt(self, n):
        if n == 0:
            return 0
        return math.sqrt(n)
    
    def square(self, n):
        return n ** 2

    def reciprocal(self, n):
        if n == 0:
            return "Error"
        return 1 / n
    
    def factorial(self, n):
        if n < 0:
            return "Error"
        elif n == 0:
            return 1
        else:
            result = 1
            for i in range(1, n + 1):
                result *= i
            return result
        
    def sin(self, n):
        return math.sin(math.radians(n))
    
    def cos(self, n):
        return math.cos(math.radians(n))
    
    def tan(self, n):
        return math.tan(math.radians(n))
    
    def log(self, n):
        if n <= 0:
            return "Error"
        return math.log10(n)
    
    def ln(self, n):
        if n <= 0:
            return "Error"
        return math.log(n)

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.master.geometry("400x600")
        self.master.resizable(False, False)
        self.master.configure(bg="gray20")

        self.functions = functions()

        self.entry = tk.Entry(self.master, width=30, font=("Arial", 24), bg="black", fg="white", insertbackground="white")
        self.entry.pack(pady=10)
        self.master.bind("<Return>", self.calculate)

        self.create_buttons()

        
    def create_buttons(self):
        frame = tk.Frame(self.master, bg="gray20")
        frame.pack(pady=10)
        keys = [
            ("7", "8", "9", "/"),
            ("4", "5", "6", "*"),
            ("1", "2", "3", "-"),
            ("0", ".", "=", "+"),
            ("sqrt", "x²", "1/x", "C"),
            ("sin", "cos", "tan", "!"),
            ("log", "ln", "(", ")"),
        ]
        for row, values in enumerate(keys):
            for column, label in enumerate(values):
                command = self.calculate if label == "=" else (
                    self.clear if label == "C" else
                    lambda value=label: self.press(value)
                )
                tk.Button(
                    frame, text=label, width=7, height=2, command=command,
                    bg="black", fg="white", activebackground="gray35",
                ).grid(row=row, column=column, padx=3, pady=3)

    def press(self, value):
        operations = {
            "sqrt": "sqrt(", "x²": "**2", "1/x": "reciprocal(",
            "sin": "sin(", "cos": "cos(", "tan": "tan(",
            "!": "factorial(", "log": "log(", "ln": "ln(",
        }
        self.entry.insert(tk.END, operations.get(value, value))
        self.entry.focus_set()

    def add(self):
        self.press("+")

    def clear(self, event=None):
        self.entry.delete(0, tk.END)

    def backspace(self, event=None):
        text = self.entry.get()
        if text:
            self.entry.delete(len(text) - 1, tk.END)

    def key_press(self, event):
        if event.keysym == "Return":
            self.calculate()
            return "break"
        if event.keysym == "Escape":
            self.clear()
            return "break"
        if event.keysym == "BackSpace":
            self.backspace()
            return "break"

    def calculate(self, event=None):
        binary_ops = {
            ast.Add: operator.add, ast.Sub: operator.sub,
            ast.Mult: operator.mul, ast.Div: operator.truediv,
            ast.Pow: operator.pow, ast.Mod: operator.mod,
        }
        unary_ops = {ast.UAdd: operator.pos, ast.USub: operator.neg}
        allowed_functions = {
            name: getattr(self.functions, name)
            for name in ("sqrt", "square", "reciprocal", "factorial", "sin", "cos", "tan", "log", "ln")
        }

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            if isinstance(node, ast.BinOp) and type(node.op) in binary_ops:
                return binary_ops[type(node.op)](evaluate(node.left), evaluate(node.right))
            if isinstance(node, ast.UnaryOp) and type(node.op) in unary_ops:
                return unary_ops[type(node.op)](evaluate(node.operand))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in allowed_functions and len(node.args) == 1:
                return allowed_functions[node.func.id](evaluate(node.args[0]))
            raise ValueError("Invalid expression")

        try:
            result = evaluate(ast.parse(self.entry.get(), mode="eval"))
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(result))
        except (ValueError, TypeError, SyntaxError, ZeroDivisionError, OverflowError):
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")


if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()

    