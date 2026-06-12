"""Core calculator logic.

Kept separate from the web layer so it is easy to unit-test.
These pure functions are what our GitHub Actions test job exercises.
"""


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(a: float, b: float) -> float:
    return a ** b


OPERATIONS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
    "power": power,
}


def calculate(operation: str, a: float, b: float) -> float:
    """Look up and run an operation by name."""
    if operation not in OPERATIONS:
        raise ValueError(f"Unknown operation: {operation}")
    return OPERATIONS[operation](a, b)
