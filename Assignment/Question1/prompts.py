"""Asks the user for input and keeps asking until the answer is valid."""
import display
import validation
import constants


def prompt_id():
    """Show the category codes, then ask for a medicine ID. """
    display.print_category_table()
    return _prompt_until_valid("Enter Medicine ID", validation.validate_id,
                               "Invalid ID. Use a category code + a number from 1 to 9999 "
                               "(e.g. PR1 or PR0001).",
                               convert=validation.normalize_id)


def prompt_medicine():
    """Ask for every detail of a new medicine, in the order the OTCMedicine class expects"""
    return prompt_name(), prompt_size(), prompt_price(), prompt_quantity()


def prompt_name():
    """Ask for a medicine name that is not blank."""
    return _prompt_until_valid("Enter Medicine Name", validation.validate_string,
                               "Medicine name cannot be empty.")


def prompt_size():
    """Ask for a medicine size that is not blank (500mg, 12 pcs)."""
    return _prompt_until_valid("Enter Medicine Size", validation.validate_string,
                               "Medicine size cannot be empty.")


def prompt_price():
    """Ask for a price greater than 0."""
    return _prompt_until_valid("Enter Medicine Price", validation.validate_price,
                               "Invalid price. Enter a number greater than 0 (e.g. 5.90).",
                               convert=_to_float)


def prompt_quantity():
    """Ask for a stock quantity that is a whole number, 0 or more."""
    return _prompt_until_valid("Enter Medicine Quantity", validation.validate_quantity,
                               "Invalid quantity. Enter a whole number, 0 or more (e.g. 120).",
                               convert=_to_int)


def confirm_action(action):
    """Ask the user to confirm an action.
    Show a cancel message and return False if they say no."""
    if prompt_yes_no(f"Confirm {action}? (Y/N)"):
        return True
    print(f"{action} cancelled.")
    return False


def prompt_yes_no(text):
    """Ask a yes/no question. Return True for Y, False for N."""
    answer = _prompt_until_valid(text, _is_yes_or_no, "Please enter Y or N.", convert=str.upper)
    return answer == "Y"


def prompt_input(text):
    """Show an aligned prompt and return what the user typed, without extra spaces."""
    return input(f"{text:{constants.PROMPT_WIDTH}}: ").strip()


def _prompt_until_valid(label, is_valid, error, convert=None):
    """Keep asking until the answer passes is_valid function, then return it.

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


def _to_float(text):
    """Turn text into a decimal number, or None if it isn't one (e.g. 'abc')."""
    try:
        return float(text)
    except ValueError:
        return None


def _to_int(text):
    """Turn text into a whole number, or None if it isn't one (e.g. '2.5')."""
    try:
        return int(text)
    except ValueError:
        return None


def _is_yes_or_no(answer):
    """Return True if the answer is Y or N."""
    return answer in ("Y", "N")
