"""Rules for valid medicine data. These only check values; they never ask or print."""
import math

import constants


def validate_id(medicine_id):
    """Return True if the ID is a known category code plus a number from 0001 to 9999."""
    if len(medicine_id) != constants.ID_LENGTH:
        return False

    code = medicine_id[:constants.CODE_LENGTH]
    number = medicine_id[constants.CODE_LENGTH:]

    if code not in constants.CATEGORY_CODES or not number.isdecimal():
        return False

    return int(number) != 0  # Item numbers start from 1


def normalize_id(medicine_id):
    """Put an ID into its standard form, e.g. ' pr1 ' becomes 'PR0001'.

    Every ID must have one exact form, because the hash table treats 'pr1' and 'PR0001' as
    different keys.
    """
    medicine_id = medicine_id.strip().upper()
    code = medicine_id[:constants.CODE_LENGTH]
    number = medicine_id[constants.CODE_LENGTH:]
    return code + number.zfill(constants.NUMBER_LENGTH)


def validate_string(text):
    """Return True if text is not blank (used for name and size)."""
    return isinstance(text, str) and text.strip() != ""


def validate_price(price):
    """Return True if price is a real number greater than 0 (rejects 'inf')."""
    return isinstance(price, (int, float)) and math.isfinite(price) and price > 0


def validate_quantity(quantity):
    """Return True if quantity is a whole number, 0 or more."""
    return _is_number(quantity) and isinstance(quantity, int) and quantity >= 0


def validate_medicine(medicine):
    """Return True if a record (id, name, size, price, quantity) passes every check above."""
    validators = (validate_id, validate_string, validate_string,
                  validate_price, validate_quantity)
    if len(medicine) != len(validators):  # Missing or extra fields
        return False
    return all(check(value) for check, value in zip(validators, medicine))


def _is_number(value):
    """Return True for int or float, but not True/False (Python treats those as 1 and 0)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)
