"""Rules for valid course data. These only check values; they never ask or print."""
import constants


def validate_code(course_code):
    """Return True if the code is 3 letters followed by 4 digits (e.g. DCS1101)."""
    if len(course_code) != constants.CODE_LENGTH:
        return False

    prefix = course_code[:constants.CODE_PREFIX_LENGTH]
    number = course_code[constants.CODE_PREFIX_LENGTH:]
    return prefix.isascii() and prefix.isalpha() and number.isdecimal()


def normalize_code(course_code):
    """Put a code into its standard form, e.g. ' dcs1101 ' becomes 'DCS1101'."""
    return course_code.strip().upper()


def normalize_level(level):
    """Put a level into its standard form, e.g. 'core' becomes 'Core'."""
    return level.strip().capitalize()


def validate_string(text):
    """Return True if text is not blank (used for the course name)."""
    return isinstance(text, str) and text.strip() != ""


def validate_optional_string(text):
    """Return True for any text, including blank (used for the description)."""
    return isinstance(text, str)


def validate_credit_hours(credit_hours):
    """Return True if credit hours is a whole number from 1 to MAX_CREDIT_HOURS."""
    return (isinstance(credit_hours, int) and not isinstance(credit_hours, bool)
            and 0 < credit_hours <= constants.MAX_CREDIT_HOURS)


def validate_level(level):
    """Return True if level is one of the allowed levels (Core or Elective)."""
    return level in constants.LEVELS


def validate_course(course):
    """Return True if a (code, name, credit hours, level, description) record passes all checks."""
    validators = (validate_code, validate_string, validate_credit_hours,
                  validate_level, validate_optional_string)
    if len(course) != len(validators):  # Missing or extra fields
        return False
    return all(check(value) for check, value in zip(validators, course))