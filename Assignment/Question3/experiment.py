"""Times Fibonacci run on several values, with and without multithreading.

Both kinds of round are measured the same way, so their times can be compared fairly:
time taken = end of the calculation that finished last - start of the one that started first.
"""
import threading
import time

from fibonacci import fibonacci


class TaskRecord:
    """The result of one Fibonacci calculation and the times (in ns) when it started and ended."""

    def __init__(self, value):
        self.value = value  # The number to calculate Fibonacci of
        self.start = None  # Set just before the calculation runs
        self.result = None  # The Fibonacci number calculated
        self.end = None  # Set just after the calculation finishes

    def run(self):
        """Calculate Fibonacci of the value, storing its result and its start and end times."""
        self.start = time.perf_counter_ns()
        self.result = fibonacci(self.value)
        self.end = time.perf_counter_ns()


def run_sequential_round(values):
    """Calculate Fibonacci of each value one after another. Return (time taken in ns, results, spans)."""
    records = [TaskRecord(value) for value in values]
    for record in records:
        record.run()
    return _summarise(records)


def run_threaded_round(values):
    """Calculate Fibonacci of each value in its own thread. Return (time taken in ns, results, spans)."""
    # Each thread writes only to its own record, so threads never change the same data
    records = [TaskRecord(value) for value in values]
    threads = [threading.Thread(target=record.run) for record in records]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()  # Wait until every thread has finished
    return _summarise(records)


def average(times):
    """Return the average of a list of times."""
    if not times:
        raise ValueError("Cannot average an empty list of times.")
    return sum(times) / len(times)


def _summarise(records):
    """Return (time taken in ns, results, spans) for one round.

    Each span is (start, end) in ns, measured from the start of the calculation that began first.
    """
    first_start = min(record.start for record in records)
    last_end = max(record.end for record in records)
    results = [record.result for record in records]
    spans = [(record.start - first_start, record.end - first_start) for record in records]
    return last_end - first_start, results, spans