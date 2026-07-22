# Python Basics

Python is a high-level, interpreted programming language known for its clean syntax and readability. Created by Guido van Rossum and first released in 1991, Python has become one of the most popular programming languages in the world.

## Data Types

Python has several built-in data types. The primary ones are:

- **Integers (int)**: Whole numbers like 1, 42, -7. Python supports arbitrarily large integers.
- **Floats (float)**: Decimal numbers like 3.14, -0.001, 2.0. These follow IEEE 754 double precision.
- **Strings (str)**: Text data enclosed in quotes. Strings are immutable in Python, meaning once created they cannot be modified in place.
- **Booleans (bool)**: True or False values, used for logical operations.
- **Lists (list)**: Ordered, mutable sequences. Lists can hold mixed types and are defined with square brackets like `[1, "hello", 3.14]`.
- **Tuples (tuple)**: Like lists but immutable. Defined with parentheses like `(1, 2, 3)`.
- **Dictionaries (dict)**: Key-value pairs for fast lookups. Keys must be hashable. Example: `{"name": "Alice", "age": 25}`.
- **Sets (set)**: Unordered collections of unique elements. Useful for membership testing and eliminating duplicates.

## List Comprehensions

List comprehensions provide a concise way to create lists based on existing iterables. The syntax is `[expression for item in iterable if condition]`. For example, `[x**2 for x in range(10) if x % 2 == 0]` produces `[0, 4, 16, 36, 64]`. They are generally faster than equivalent for-loops because the iteration is optimized internally.

## Functions and Scope

Functions in Python are defined using the `def` keyword. Python supports default arguments, keyword arguments, and variable-length argument lists using `*args` and `**kwargs`. Functions are first-class objects, meaning they can be passed as arguments, returned from other functions, and assigned to variables.

Python uses LEGB rule for variable scope resolution: Local, Enclosing, Global, Built-in. Variables defined inside a function are local by default. The `global` keyword allows modification of global variables from within a function.

## Error Handling

Python uses try-except blocks for exception handling. Common exceptions include TypeError, ValueError, KeyError, IndexError, and FileNotFoundError. You can define custom exceptions by subclassing the Exception class. The `finally` block executes regardless of whether an exception occurred, making it useful for cleanup operations like closing files.

## Decorators

Decorators are a way to modify the behavior of functions or classes. They use the `@decorator` syntax and are essentially higher-order functions that wrap another function. Common built-in decorators include `@staticmethod`, `@classmethod`, and `@property`. Decorators are widely used in web frameworks like Flask for defining routes.

## Generators

Generators are functions that use `yield` instead of `return` to produce a sequence of values lazily. They are memory-efficient because they generate values on-the-fly rather than storing them all in memory. Generator expressions use parentheses instead of square brackets: `(x**2 for x in range(1000000))`.
