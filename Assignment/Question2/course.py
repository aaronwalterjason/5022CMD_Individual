"""The course record stored as a vertex in the prerequisite graph."""
import constants


class Course:
    """One course offered by the university."""

    def __init__(self, course_code, course_name, credit_hours, level, description):
        self._course_code = course_code  # str, e.g. "DCS1101" (read-only, see below)
        self.course_name = course_name  # str, e.g. "Programming Fundamentals"
        self.credit_hours = credit_hours  # int, from 1 to MAX_CREDIT_HOURS
        self.level = level  # str, "Core" or "Elective"
        self.description = description  # str, may be blank

    def __str__(self):
        """Show every detail of the course."""
        width = constants.LABEL_WIDTH
        return (f"\n{'Course Code':<{width}}: {self.course_code}\n"
                f"{'Course Name':<{width}}: {self.course_name}\n"
                f"{'Credit Hours':<{width}}: {self.credit_hours}\n"
                f"{'Level':<{width}}: {self.level}\n"
                f"{'Description':<{width}}: {self.description or '-'}")

    @property
    def course_code(self):
        """Read-only, because the graph and the lookup dictionary both rely on the code."""
        return self._course_code

    def is_core(self):
        """Return True if this is a core course, False if it is an elective."""
        return self.level == constants.CORE_LEVEL

    # Two Course objects with the same code are the same course,
    # so a Course can be used safely as a vertex (dictionary key) in the graph
    def __eq__(self, other):
        return isinstance(other, Course) and self.course_code == other.course_code

    def __hash__(self):
        return hash(self.course_code)