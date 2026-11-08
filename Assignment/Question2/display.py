"""Everything the user sees on screen: menus, tables and messages."""
import constants


def print_menu(labels, course_count):
    """Show the main menu. Options are numbered in order, with Exit as the last number."""
    print("\n" + "=" * constants.DISPLAY_WIDTH)
    print("=== Course Prerequisite System ===".center(constants.DISPLAY_WIDTH))
    print("=" * constants.DISPLAY_WIDTH)
    for number, label in enumerate(labels, start=1):
        print(f"{number}. {label}")
    print(f"{len(labels) + 1}. Exit")
    print("-" * constants.DISPLAY_WIDTH)
    print(f"Courses stored: {course_count}/{constants.MAX_COURSES}")


def print_header(title):
    """Show a screen title centred between two lines."""
    print("\n" + "=" * constants.DISPLAY_WIDTH)
    print(title.center(constants.DISPLAY_WIDTH))
    print("=" * constants.DISPLAY_WIDTH)


def print_message(text):
    """Show a line of information, with a blank line above it."""
    print(f"\n{text}")


def print_course(course):
    """Show every detail of a course."""
    print(course)


def print_error(text):
    """Show an error with blank lines around it, so it stands out."""
    print(f"\n{text}")


def _print_table(headers, widths, rows):
    """Print rows as a table. Columns start at the given widths and grow to fit longer text."""
    widths = _column_widths(headers, widths, rows)
    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"
    print(border)
    print("| " + " | ".join(f"{h:<{w}}" for h, w in zip(headers, widths)) + " |")
    print(border)
    for row in rows:
        print("| " + " | ".join(f"{str(v):<{w}}" for v, w in zip(row, widths)) + " |")
    print(border)


def _column_widths(headers, widths, rows):
    """Return each column's width: the largest of its starting width, header and values."""
    new_widths = []
    for i, width in enumerate(widths):  # Go through each column
        candidates = [width, len(headers[i])]  # The starting width and the header's length
        for row in rows:
            candidates.append(len(str(row[i])))  # The length of every value in this column
        new_widths.append(max(candidates))  # Keep the biggest
    return new_widths


def print_course_names(courses):
    """Show a numbered list of every course name."""
    rows = [(number, c.course_name) for number, c in enumerate(courses, start=1)]
    _print_table(["No.", "Course Name"],
                 [constants.NO_COLUMN_WIDTH, constants.NAME_COLUMN_WIDTH], rows)
    print(f"Total: {len(courses)} course(s)")


def print_course_table(courses, empty_message="No courses."):
    """Show courses as a table of code, name and level, or empty_message if there are none."""
    if not courses:
        print(empty_message)
        return
    rows = [(number, c.course_code, c.course_name, c.level)
            for number, c in enumerate(courses, start=1)]
    _print_table(["No.", "Code", "Course Name", "Level"],
                 [constants.NO_COLUMN_WIDTH, constants.CODE_COLUMN_WIDTH,
                  constants.NAME_COLUMN_WIDTH, constants.LEVEL_COLUMN_WIDTH], rows)


def print_links(prerequisite_codes, unlocked_codes):
    """Show the prerequisites and unlocked courses of a course as code lists."""
    width = constants.LABEL_WIDTH
    print(f"{'Prerequisites':<{width}}: {', '.join(prerequisite_codes) or 'None'}")
    print(f"{'Unlocks':<{width}}: {', '.join(unlocked_codes) or 'None'}")


def print_course_profile(course):
    """Core courses show every detail; elective courses show only the name."""
    if course.is_core():
        print_course(course)
    else:
        print(f"\n{'Course Name':<{constants.LABEL_WIDTH}}: {course.course_name}")
        print("(Other details are hidden because this is an elective course.)")


def print_study_stages(stages):
    """Each stage is a list of (course, prerequisite codes). Stage 1 has no prerequisites."""
    rows = []
    for number, stage in enumerate(stages, start=1):
        for course, codes in stage:
            rows.append((number, course.course_code, course.course_name,
                         ", ".join(codes) or "None"))
    _print_table(["Stage", "Code", "Course Name", "Needs"],
                 [constants.NO_COLUMN_WIDTH, constants.CODE_COLUMN_WIDTH,
                  constants.NAME_COLUMN_WIDTH, constants.CODE_COLUMN_WIDTH], rows)
    print("Courses in the same stage can be taken together once earlier stages are done.")
