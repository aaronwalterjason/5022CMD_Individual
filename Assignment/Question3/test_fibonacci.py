"""Quick checks with small values, so they finish in under a second."""
import experiment
from fibonacci import fibonacci


def square(number):
    """A simple task, to show the experiment works with any function, not just Fibonacci."""
    return number * number


print("=== Fibonacci values ===")
print("Got      :", [fibonacci(n) for n in range(11)])
print("Expected : [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]")

print("\n=== Both rounds give the same answers ===")
values = (20, 22, 25)
_, sequential_results, sequential_spans = experiment.run_sequential_round(values)
_, threaded_results, threaded_spans = experiment.run_threaded_round(values)
print("Sequential :", sequential_results)
print("Threaded   :", threaded_results)
print("Same answers:", sequential_results == threaded_results, "(expected True)")

print("\n=== Sequential tasks never overlap ===")
no_overlap = all(earlier[1] <= later[0]
                 for earlier, later in zip(sequential_spans, sequential_spans[1:]))
print("Each task starts after the previous one ends:", no_overlap, "(expected True)")

print("\n=== Works with any task ===")
_, squares, _ = experiment.run_threaded_round((2, 3, 4), task=square)
print("Squares of 2, 3, 4 :", squares, "(expected [4, 9, 16])")

print("\n=== Average ===")
print("Average of [10, 20, 30] :", experiment.average([10, 20, 30]), "(expected 20.0)")
try:
    experiment.average([])
except ValueError as error:
    print("Average of [] :", error, "(expected this message)")