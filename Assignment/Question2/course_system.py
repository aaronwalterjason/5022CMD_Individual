"""The course prerequisite system: the menu and every action the user can take."""
import constants
import display
import prompts
import validation
from course import Course
from graph import DirectedGraph


class CourseSystem:
    """Course prerequisite system. An edge A -> B means A is a prerequisite of B."""

    # ==================================================================
    # Setup
    # ==================================================================
    def __init__(self, max_courses=constants.MAX_COURSES):
        self.graph = DirectedGraph()
        self.courses = {}  # Course code -> Course, for quick lookup
        self.max_courses = max_courses
        # The only place menu options are defined: number = position, Exit comes after them
        self.menu_options = [
            ("List All Course Names", self.list_course_names),
            ("View Course Details", self.view_course_details),
            ("View Prerequisites", self.view_prerequisites),
            ("View Unlocked Courses", self.view_unlocked_courses),
            ("Add Course", self.add_course),
            ("Add Prerequisite", self.add_prerequisite),
            ("Remove Prerequisite", self.remove_prerequisite),
            ("Suggested Study Order", self.view_study_order),
        ]

    def load_preloaded_courses(self):
        """Add the sample courses and prerequisite links from constants, skipping invalid ones."""
        for record in constants.PRELOADED_COURSES:
            if validation.validate_course(record):
                self._store(Course(*record))
            else:
                display.print_error(f"Skipped invalid pre-loaded course: {record}")

        for prerequisite_code, course_code in constants.PRELOADED_PREREQUISITES:
            error = self._link(prerequisite_code, course_code)
            if error:
                display.print_error(
                    f"Skipped pre-loaded link {prerequisite_code} -> {course_code}: {error}")

    # ==================================================================
    # Menu
    # ==================================================================
    def run_menu(self):
        """Show the main menu until the user chooses Exit."""
        labels = [label for label, _ in self.menu_options]
        exit_choice = str(len(self.menu_options) + 1)
        halt = False
        while not halt:
            display.print_menu(labels, len(self.courses))
            choice = prompts.prompt_input("Enter your choice")
            if choice == exit_choice:
                display.print_message(
                    "Thank you for using the Course Prerequisite System. Goodbye!")
                halt = True
            else:
                self.handle_menu_choice(choice)

    def handle_menu_choice(self, choice):
        """Run the option the user picked, or show an error if the choice is not on the menu."""
        count = len(self.menu_options)
        if not choice.isdecimal() or not 1 <= int(choice) <= count:
            display.print_error(f"Invalid choice. Please enter a number from 1 to {count + 1}.")
            return
        _, action = self.menu_options[int(choice) - 1]
        action()
        prompts.pause()

    # ==================================================================
    # Main Operations
    # ==================================================================
    def list_course_names(self):
        """Show the name of every course."""
        display.print_header("All Courses")
        display.print_course_names(self.graph.vertices())

    def view_course_details(self):
        """Core courses show everything. Electives show their name, then all details on request."""
        display.print_header("Course Details")
        course = self._find_course()
        display.print_course_profile(course)
        if not course.is_core():
            # Electives only showed their name, so offer the hidden details
            if not prompts.prompt_yes_no("Show all details? (Y/N)"):
                return
            display.print_message("All details:")          # ← New line
            display.print_course(course)
        display.print_links(self._prerequisite_codes(course),self._unlocked_codes(course))

    def view_prerequisites(self):
        """Show the courses that must be taken before a chosen course (its incoming edges)."""
        display.print_header("Prerequisites")
        course = self._find_course()
        display.print_message(
            f"Prerequisites of {course.course_code} - {course.course_name}:")
        display.print_course_table(self.graph.list_incoming_adjacent_vertex(course),
                                   "None. This course has no prerequisites.")

    def view_unlocked_courses(self):
        """Show the courses that a chosen course is a prerequisite for (its outgoing edges)."""
        display.print_header("Unlocked Courses")
        course = self._find_course()
        display.print_message(
            f"Completing {course.course_code} - {course.course_name} unlocks:")
        display.print_course_table(self.graph.list_outgoing_adjacent_vertex(course),
                                   "None. This course is not a prerequisite for any course.")

    def add_course(self):
        """Add a new course as a vertex once confirmed, then offer to link its prerequisites."""
        display.print_header("Add Course")
        if len(self.courses) >= self.max_courses:
            display.print_error(f"Cannot add more courses. The maximum is {self.max_courses}.")
            return

        new_course = self._ask_new_course()
        if new_course is None:  # The user did not confirm
            return
        self._store(new_course)
        display.print_message(f"Course {new_course.course_code} added successfully.")
        self._offer_prerequisites(new_course)

    def add_prerequisite(self):
        """Make one course a prerequisite of another by adding an edge, if the rules allow it."""
        display.print_header("Add Prerequisite")
        course = self._find_course("Enter Course to Update")
        self._ask_for_prerequisite(course, show_table=False)

    def remove_prerequisite(self):
        """Remove one of a course's prerequisites by deleting that edge."""
        display.print_header("Remove Prerequisite")
        course = self._find_course("Enter Course to Update")
        if not self.graph.list_incoming_adjacent_vertex(course):
            display.print_error(f"{course.course_code} has no prerequisites to remove.")
            return

        prerequisite = self._ask_current_prerequisite(course)
        if prompts.confirm_action("Remove Prerequisite"):
            self.graph.remove_edge(prerequisite, course)
            display.print_message(
                f"{prerequisite.course_code} is no longer a prerequisite of {course.course_code}.")
            self._print_updated_prerequisites(course)

    def view_study_order(self):
        """Group courses into stages so every prerequisite sits in an earlier stage."""
        display.print_header("Suggested Study Order")
        levels = self.graph.topological_levels()
        if levels is None:
            display.print_error("No valid order exists because the prerequisites form a loop.")
            return
        stages = []
        for level in levels:
            stages.append([(c, self._prerequisite_codes(c)) for c in level])
        display.print_study_stages(stages)

    # ==================================================================
    # Helpers
    # ==================================================================
    def _store(self, course):
        """Add the course to the graph and the lookup dictionary together."""
        self.graph.add_vertex(course)
        self.courses[course.course_code] = course

    def _find_course(self, text="Enter Course Code", show_table=True):
        """Keep asking for a course code until it matches an existing course, then return it."""
        if show_table:
            display.print_course_table(self.graph.vertices())
        course_code = prompts.prompt_code(text)
        while course_code not in self.courses:
            display.print_error(f"Course {course_code} does not exist. "
                                f"Please enter a code from the list above.")
            course_code = prompts.prompt_code(text)
        return self.courses[course_code]

    def _ask_new_course(self):
        """Ask for an unused code and the details. Return the course if confirmed, or None."""
        course_code = prompts.prompt_code()
        while course_code in self.courses:
            display.print_error(f"Course {course_code} already exists. Please enter a new code.")
            course_code = prompts.prompt_code()

        new_course = Course(course_code, *prompts.prompt_course_details())
        display.print_course(new_course)
        if prompts.confirm_action("Add Course"):
            return new_course
        return None

    def _offer_prerequisites(self, course):
        """Keep offering to add prerequisites to a newly added course until the user says no."""
        # A new course has no prerequisites yet, so offer to link them straight away
        adding = prompts.prompt_yes_no("Add prerequisites now? (Y/N)")
        while adding:
            self._ask_for_prerequisite(course)
            adding = prompts.prompt_yes_no("Add another prerequisite? (Y/N)")

    def _ask_for_prerequisite(self, course, show_table=True):
        """Ask for a prerequisite of course and add the edge if the rules allow it."""
        prerequisite = self._find_course("Enter Prerequisite Code", show_table=show_table)
        error = self._check_new_link(prerequisite.course_code, course.course_code)
        if error:  # A rule refused the link: explain why and stop
            display.print_error(error)
            return
        if prompts.confirm_action("Add Prerequisite"):
            self.graph.add_edge(prerequisite, course)
            display.print_message(
                f"{prerequisite.course_code} is now a prerequisite of {course.course_code}.")
            self._print_updated_prerequisites(course)

    def _ask_current_prerequisite(self, course):
        """Show course's prerequisites and keep asking until one of them is entered."""
        current = self.graph.list_incoming_adjacent_vertex(course)
        display.print_message(f"Current prerequisites of {course.course_code}:")
        display.print_course_table(current)

        prerequisite_code = prompts.prompt_code("Enter Prerequisite Code")
        # A code that doesn't exist gives None, which is never in the list either
        while self.courses.get(prerequisite_code) not in current:
            display.print_error(
                f"{prerequisite_code} is not a prerequisite of {course.course_code}. "
                f"Please enter a code from the list above.")
            prerequisite_code = prompts.prompt_code("Enter Prerequisite Code")
        return self.courses[prerequisite_code]

    def _check_new_link(self, prerequisite_code, course_code):
        """Return why prerequisite -> course is not allowed, or None if it is fine.

        Blocks missing courses, self-links, duplicates, loops and redundant links.
        """
        prerequisite = self.courses.get(prerequisite_code)
        course = self.courses.get(course_code)
        if prerequisite is None or course is None:
            return "Both courses must exist."
        if prerequisite == course:
            return "A course cannot be a prerequisite of itself."
        if self.graph.has_edge(prerequisite, course):
            return f"{prerequisite_code} is already a prerequisite of {course_code}."
        # If the course already leads to the prerequisite, the new link would form a loop
        if self.graph.has_path(course, prerequisite):
            return (f"Circular prerequisite: {course_code} already comes before "
                    f"{prerequisite_code}.")
        # If the prerequisite already leads to the course, a direct link would add nothing
        if self.graph.has_path(prerequisite, course):
            return (f"{prerequisite_code} is already required before {course_code} "
                    f"through other courses.")
        return None

    def _link(self, prerequisite_code, course_code):
        """Add prerequisite -> course if the rules allow it. Return the error, or None if added."""
        error = self._check_new_link(prerequisite_code, course_code)
        if error is None:
            self.graph.add_edge(self.courses[prerequisite_code], self.courses[course_code])
        return error

    def _print_updated_prerequisites(self, course):
        """Show a course's prerequisites after one has been added or removed."""
        display.print_message(f"Updated prerequisites of {course.course_code}:")
        display.print_course_table(self.graph.list_incoming_adjacent_vertex(course), "None")

    def _prerequisite_codes(self, course):
        """Return the codes of the courses that must be taken before course."""
        return [c.course_code for c in self.graph.list_incoming_adjacent_vertex(course)]

    def _unlocked_codes(self, course):
        """Return the codes of the courses that course is a prerequisite for."""
        return [c.course_code for c in self.graph.list_outgoing_adjacent_vertex(course)]