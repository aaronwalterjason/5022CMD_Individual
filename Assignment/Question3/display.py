"""Everything the user sees on screen: titles, round times, timelines and the comparison."""
import constants


def print_title(title):
    """Show a title centred between two lines."""
    print("\n" + "=" * constants.DISPLAY_WIDTH)
    print(title.center(constants.DISPLAY_WIDTH))
    print("=" * constants.DISPLAY_WIDTH)


def print_environment(python_version, gil_enabled, cpu_count):
    """Show the conditions the experiment ran under, since they affect the results."""
    width = constants.LABEL_WIDTH
    print(f"{'Python':<{width}}: {python_version}")
    print(f"{'GIL enabled':<{width}}: {'Yes' if gil_enabled else 'No'}")
    print(f"{'CPU cores':<{width}}: {cpu_count}")


def print_results(values, results):
    """Show each Fibonacci number that was calculated."""
    for value, result in zip(values, results):
        print(f"  Fibonacci({value}) = {result:,}")


def print_timeline(values, spans, number):
    """Show when each calculation started and ended, in seconds from the first start."""
    print(f"Timeline of Round {number} (seconds from the 1st start):")
    for value, (start_ns, end_ns) in zip(values, spans):
        start, end = start_ns / constants.NS_PER_SECOND, end_ns / constants.NS_PER_SECOND
        print(f"  Fibonacci({value}) : {start:6.2f} -> {end:6.2f}  (ran for {end - start:.2f} s)")


def print_round(number, total, elapsed_ns):
    """Show the time taken by one round, in nanoseconds and seconds."""
    _print_time(f"Round {number:>2} of {total}", elapsed_ns)


def print_average(average_ns):
    """Show the average time of all rounds, in nanoseconds and seconds."""
    print("-" * constants.DISPLAY_WIDTH)
    _print_time("Average", average_ns)


def print_comparison(threaded_average, sequential_average):
    """Show both averages side by side and whether multithreading was faster or slower."""
    difference = threaded_average - sequential_average
    percent = abs(difference) / sequential_average * 100
    verdict = "slower" if difference > 0 else "faster"
    width, time_width = constants.COMPARE_LABEL_WIDTH, constants.TIME_WIDTH

    print(f"{'With multithreading':<{width}}: {threaded_average:>{time_width},.0f} ns")
    print(f"{'Without multithreading':<{width}}: {sequential_average:>{time_width},.0f} ns")
    print("-" * constants.DISPLAY_WIDTH)
    print(f"Multithreading was {percent:.2f}% {verdict} "
          f"({abs(difference):,.0f} ns per round).")


def _print_time(label, time_ns):
    """Show a labelled time in nanoseconds, with seconds in brackets for easier reading."""
    seconds = time_ns / constants.NS_PER_SECOND
    width, time_width = constants.ROUND_LABEL_WIDTH, constants.TIME_WIDTH
    print(f"{label:<{width}}: {time_ns:>{time_width},.0f} ns  ({seconds:.2f} s)")