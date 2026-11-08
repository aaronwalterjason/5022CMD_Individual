"""Runs the Fibonacci experiment with and without multithreading, then compares them."""
import os
import platform
import sys

import constants
import display
import experiment


def gil_is_enabled():
    """Return True if Python's Global Interpreter Lock (GIL) is switched on."""
    # Python 3.13 added a way to check; older versions always have the GIL
    check = getattr(sys, "_is_gil_enabled", None)
    return True if check is None else check()


def run_rounds(title, round_function, values, rounds):
    """Run round_function on values for every round, showing each time. Return the average."""
    display.print_title(title)
    times = []
    for number in range(1, rounds + 1):
        elapsed_ns, results, spans = round_function(values)
        if number == 1:  # Show the answers and timeline once, as evidence for the report
            display.print_results(values, results)
            display.print_timeline(values, spans, number)
        display.print_round(number, rounds, elapsed_ns)
        times.append(elapsed_ns)
    average_ns = experiment.average(times)
    display.print_average(average_ns)
    return average_ns


def main():
    """Show the test conditions, run both experiments, then compare their averages."""
    display.print_title("Fibonacci Multithreading Experiment")
    display.print_environment(platform.python_version(), gil_is_enabled(), os.cpu_count())

    values, rounds = constants.FIB_VALUES, constants.ROUNDS
    threaded_average = run_rounds("With Multithreading (1 thread per value)",
                                  experiment.run_threaded_round, values, rounds)
    sequential_average = run_rounds("Without Multithreading (one after another)",
                                    experiment.run_sequential_round, values, rounds)

    display.print_title("Comparison of Average Times")
    display.print_comparison(threaded_average, sequential_average)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Closes cleanly if the user presses Ctrl+C during the long calculation
        print("\n\nExperiment stopped. Goodbye!")