"""The Fibonacci function used in the experiment."""


def fibonacci(n):
    """Return the nth Fibonacci number by plain recursion, where n is 0 or more. O(2^n).

    Fibonacci(0) = 0, Fibonacci(1) = 1, and every later number is the sum of the two before it.
    """
    if n <= 1:
        return n
    # Each call does a fixed amount of work, then makes two more calls,
    # so the number of calls roughly doubles every time n goes up by 1
    return fibonacci(n - 1) + fibonacci(n - 2)