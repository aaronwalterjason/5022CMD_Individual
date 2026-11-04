import time


def average_search_time(search_function, key, repeats):
    """Return the average time (ns) of one search, measured over repeats runs.

    Timing many runs together and dividing gives a steadier result than timing
    a single search, which is too quick to measure reliably.
    """
    start = time.perf_counter_ns()
    for _ in range(repeats):
        search_function(key)
    return (time.perf_counter_ns() - start) / repeats
