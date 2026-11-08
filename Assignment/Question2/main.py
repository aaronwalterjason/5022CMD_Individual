"""Starts the Course Prerequisite System."""
import course_system


def main():
    """Set up the system with the sample courses, then show the menu."""
    system = course_system.CourseSystem()
    system.load_preloaded_courses()
    system.run_menu()

    
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Closes cleanly if the user presses Ctrl+C or the input ends
        print("\n\nProgram closed. Goodbye!")