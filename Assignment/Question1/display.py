"""Everything the user sees on screen: menus, tables, messages and results."""
import constants


def print_menu():
    """Show the main menu."""
    print_title("Over The Counter Pharmacy Inventory System")
    print("1. Insert Medicine")
    print("2. Search Medicine")
    print("3. Edit Medicine")
    print("4. Delete Medicine")
    print("5. Exit")
    _print_line()


def print_edit_menu():
    """Show the fields that can be edited."""
    print_title("Edit Medicine")
    print("1. Name")
    print("2. Size")
    print("3. Price")
    print("4. Quantity")
    print("5. Done")
    _print_line()


def print_category_table():
    """Show the valid category codes, so the user knows what to type in an ID."""
    code_width = constants.CODE_COLUMN_WIDTH
    name_width = constants.CATEGORY_COLUMN_WIDTH
    border = f"+{'-' * (code_width + 2)}+{'-' * (name_width + 2)}+"

    print(border)
    print(f"| {'Code':<{code_width}} | {'Category':<{name_width}} |")
    print(border)
    for code, name in constants.CATEGORY_CODES.items():
        print(f"| {code:<{code_width}} | {name:<{name_width}} |")
    print(border)


def print_slot_info(slot, home_slot):
    """Show where a medicine is stored, and whether a collision moved it from its home slot."""
    if slot == home_slot:
        print(f"Stored in slot : [{slot}] (Home Slot)")
    else:
        print(f"Stored in slot : [{slot}] (Home Slot [{home_slot}] was taken)")


def print_search_times(hash_time, array_time, record_count):
    """Show the average search time of the hash table and the 1D array."""
    print(f"Average search time over {record_count} records:")
    print(f"  {'Hash Table':<10} : {hash_time:>10,.0f} ns")
    print(f"  {'1D Array':<10} : {array_time:>10,.0f} ns")


def print_error(text):
    """Show an error with blank lines around it, so it stands out."""
    print(f"\n{text}\n")


def print_title(title):
    """Show a title centred between two lines."""
    _print_line("=")
    print(f"{title:^{constants.DISPLAY_WIDTH}}")
    _print_line("=")


def _print_line(char="-"):
    """Print separator line across display."""
    print(char * constants.DISPLAY_WIDTH)
