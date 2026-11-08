"""Asks the user for input and keeps asking until the answer is valid."""
import constants
import display
import validation


def prompt_course_details():
    """Ask for every detail of a new course except the code, in the order Course expects."""
    return prompt_name(), prompt_credit_hours(), prompt_level(), prompt_description()


def prompt_input(text):
    """Show an aligned prompt and return what the user typed, without extra spaces."""
    return input(f"{text:{constants.PROMPT_WIDTH}}: ").strip()


def prompt_code(text="Enter Course Code"):
    """Ask for a course code in the form 3 letters + 4 digits."""
    return _prompt_until_valid(text, validation.validate_code,
                               "Invalid code. Use 3 letters + 4 digits (e.g. DCS1101).",
                               convert=validation.normalize_code)


def prompt_name():
    """Ask for a course name that is not blank."""
    return _prompt_until_valid("Enter Course Name", validation.validate_string,
                               "Course Name cannot be empty. Please try again.")


def prompt_credit_hours():
    """Ask for credit hours as a whole number from 1 to MAX_CREDIT_HOURS."""
    return _prompt_until_valid(
        "Enter Credit Hours", validation.validate_credit_hours,
        f"Invalid credit hours. Enter a whole number from 1 to {constants.MAX_CREDIT_HOURS}.",
        convert=_to_int)


def prompt_level():
    """Ask for the course level (Core or Elective), in any letter case."""
    return _prompt_until_valid(f"Enter Level ({'/'.join(constants.LEVELS)})",
                               validation.validate_level,
                               f"Invalid level. Please enter {' or '.join(constants.LEVELS)}.",
                               convert=validation.normalize_level)


def prompt_description():
    """Ask for a description. Blank is allowed because it is optional."""
    return prompt_input("Enter Description")


def prompt_yes_no(text):
    """Ask a yes/no question. Return True for Y, False for N."""
    answer = _prompt_until_valid(text, _is_yes_or_no, "Please enter Y or N.", convert=str.upper)
    return answer == "Y"


def confirm_action(action):
    """Ask the user to confirm action. Print a cancel message and return False if they say no."""
    if prompt_yes_no(f"Confirm {action}? (Y/N)"):
        return True
    print(f"{action} cancelled.")
    return False

def _prompt_until_valid(label, is_valid, error, convert=None):
    """Keep asking until the answer passes is_valid, then return it.

    If convert is given, the typed text is converted first (e.g. into a number).
    A conversion that fails gives None, which counts as invalid.
    """
    value = _read(label, convert)
    while value is None or not is_valid(value):
        display.print_error(error)
        value = _read(label, convert)
    return value


def _read(label, convert):
    """Read one answer, converted if a convert function is given."""
    text = prompt_input(label)
    return convert(text) if convert else text


def _to_int(text):
    """Turn text into a whole number, or None if it isn't one (e.g. '2.5')."""
    try:
        return int(text)
    except ValueError:
        return None


def _is_yes_or_no(answer):
    """Return True if the answer is Y or N."""
    return answer in ("Y", "N")


def pause():
    """Wait for Enter, so the user can read the result before the menu returns."""
    input("\nPress Enter to continue...")