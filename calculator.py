# Provide dependency-free arithmetic for the demonstration baseline.
"""Small calculator fixture for the software factory PoC."""


# Return the sum of two operands without external effects.
def add(a, b):
    return a + b


# Return the difference of two operands without external effects.
def subtract(a, b):
    return a - b
