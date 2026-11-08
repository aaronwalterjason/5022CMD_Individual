"""Fixed settings and sample data for the course prerequisite system."""

# (code, name, credit hours, level, description)
PRELOADED_COURSES = [
    ("DCS1101", "Programming Fundamentals", 4, "Core",
     "Basic programming concepts and problem solving."),
    ("ICT1104", "Database Management", 4, "Core",
     "Relational databases, SQL and data modelling."),
    ("ICT1105", "Fundamentals of Networking", 4, "Core",
     "Network models, protocols and basic network setup."),
    ("DCS2101", "Data Structure", 4, "Core",
     "Lists, stacks, queues, trees and hash tables."),
    ("ICT2113", "Object Oriented Programming", 4, "Core",
     "Classes, objects, inheritance and polymorphism."),
    ("ICT1106", "System Analysis and Design", 4, "Core",
     "Gathering requirements and modelling information systems."),
    ("DCS2103", "High Level Programming", 4, "Core",
     "Advanced programming techniques and larger applications."),
    ("CAP2100", "Capstone Project", 4, "Core",
     "Final-year project applying skills from the whole programme."),
    ("DCS2110", "Cybersecurity Fundamentals", 4, "Elective",
     "Threats, attacks and basic security controls."),
]

# (prerequisite, course): the first course must be taken before the second
PRELOADED_PREREQUISITES = [
    ("DCS1101", "DCS2101"),
    ("DCS1101", "ICT2113"),
    ("DCS2101", "DCS2103"),
    ("ICT1104", "ICT1106"),
    ("ICT1106", "CAP2100"),
    ("ICT2113", "CAP2100"),
    ("ICT1105", "DCS2110"),
]

# Course code: 3 letters + 4 digits (e.g. DCS1101)
CODE_PREFIX_LENGTH = 3
CODE_NUMBER_LENGTH = 4
CODE_LENGTH = CODE_PREFIX_LENGTH + CODE_NUMBER_LENGTH

# Course rules
CORE_LEVEL = "Core"
LEVELS = (CORE_LEVEL, "Elective")
MAX_CREDIT_HOURS = 6
MAX_COURSES = 10

# Display
DISPLAY_WIDTH = 64
PROMPT_WIDTH = 27
LABEL_WIDTH = 15
NO_COLUMN_WIDTH = 4
CODE_COLUMN_WIDTH = 8
NAME_COLUMN_WIDTH = 34
LEVEL_COLUMN_WIDTH = 8