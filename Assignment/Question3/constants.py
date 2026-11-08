"""Fixed settings for the multithreading experiment."""

# Experiment
FIB_VALUES = (35, 38, 40)  # One thread is created for each value
ROUNDS = 10

# Display
DISPLAY_WIDTH = 64
LABEL_WIDTH = 12
ROUND_LABEL_WIDTH = 15
COMPARE_LABEL_WIDTH = 23
TIME_WIDTH = 18  # Room for nanosecond values with commas, e.g. 16,222,046,166
NS_PER_SECOND = 1_000_000_000