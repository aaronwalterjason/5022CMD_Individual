"""The inventory system: the menu and every action the user can take."""
import display
import prompts
import product
import hashing
import constants
import validation
import one_dimensional_array
import benchmark


class InventorySystem:
    """Store medicine in a hash table, with a 1D array copy for search-time comparison."""

    def __init__(self):
        self.table = hashing.LinearProbingHashTable(
            constants.HASH_TABLE_SIZE, constants.HASH_BASE, constants.MAX_LOAD_FACTOR)
        self.array = one_dimensional_array.OneDimensionalArray()  # Same data, for comparison

    # ==================================================================
    # Setup
    # ==================================================================

    def load_preloaded_medicines(self):
        """Insert the sample records from constants, skipping any that are invalid."""
        for record in constants.PRELOADED_MEDICINES:
            if not validation.validate_medicine(record):  # Catch typos in the sample data
                display.print_error(f"Skipped invalid record: {record}")
                continue
            if self._store(product.OTCMedicine(*record)) == -1:  # Same ID listed twice
                display.print_error(f"Skipped duplicate record: {record}")

    # ==================================================================
    # Menu
    # ==================================================================

    def run_menu(self):
        """Show the main menu until the user chooses Exit."""
        halt = False
        while not halt:
            display.print_menu()
            choice = prompts.prompt_input("Enter Choice")
            halt = self.handle_menu_choice(choice)

    def handle_menu_choice(self, choice):
        """Run the action for choice. Return True if the user chose to exit."""
        match choice:
            case "1":
                self.insert_medicine()
            case "2":
                self.search_medicine()
            case "3":
                self.edit_medicine()
            case "4":
                self.delete_medicine()
            case "5":
                print("Exiting Inventory System. Goodbye!")
                return True
            case _:
                display.print_error("Invalid choice. Please enter 1–5.")
        return False

    # ==================================================================
    # Main operations
    # ==================================================================

    def insert_medicine(self):
        """Ask for a new medicine's details, show them, and store it once confirmed."""
        medicine_id = prompts.prompt_id()

        if self._id_exists(medicine_id):  # Check before asking for more details
            display.print_error(f"Medicine ID {medicine_id} already exists.")
            return

        name, size, price, quantity = prompts.prompt_medicine()
        medicine = product.OTCMedicine(medicine_id, name, size, price, quantity)

        print(medicine)

        if not prompts.confirm_action("INSERT"):
            return

        slot = self._store(medicine)
        print(f"\nMedicine inserted successfully into : Slot [{slot}]\n")

    def search_medicine(self):
        """Find a medicine, then compare how long the hash table and 1D array take to find it."""
        medicine = self._find_medicine()
        if medicine is not None:
            self._compare_search_times(medicine.medicine_id)

    def edit_medicine(self):
        """Edit a copy of a medicine's details, and apply them only if the user saves."""
        medicine = self._find_medicine()
        if medicine is None:  # Not found: the helper already showed the error
            return

        draft = {"name": medicine.name, "size": medicine.size,
                 "price": medicine.price, "quantity": medicine.quantity}

        self._run_edit_menu(draft)

        preview = product.OTCMedicine(medicine.medicine_id, **draft)
        print(preview)  # Edited version

        if not prompts.prompt_yes_no("Save changes? (Y/N)"):
            print("Edit cancelled.")
            return

        medicine.name, medicine.size = draft["name"], draft["size"]  # Apply to the stored object
        medicine.price, medicine.quantity = draft["price"], draft["quantity"]
        print("Medicine updated successfully.")

    def delete_medicine(self):
        """Delete a medicine after confirmation, leaving a tombstone in its slot."""
        medicine = self._find_medicine()
        if medicine is None:  # Not found: the helper already showed the error
            return

        if not prompts.confirm_action(f"DELETE {medicine.medicine_id} ({medicine.name})"):
            return

        if self.table.delete(medicine.medicine_id):  # Leaves a tombstone in the table
            self.array.delete(medicine.medicine_id)
            print(f"Medicine {medicine.medicine_id} deleted successfully. "
                  f"Load factor is now {self.table.load_factor():.2f}.")
        else:  # Should not happen, since the medicine was just found
            display.print_error(f"Medicine {medicine.medicine_id} could not be deleted.")

    # ==================================================================
    # Helpers
    # ==================================================================

    def _store(self, medicine):
        """Add a medicine to both the hash table and the 1D array.

        Return its table slot, or -1 if the ID already exists (then neither structure changes).
        """
        slot = self.table.insert(medicine.medicine_id, medicine)
        if slot != -1:  # Only copy to the array if the table accepted it, so both stay identical
            self.array.insert(medicine.medicine_id, medicine)
        return slot

    def _id_exists(self, medicine_id):
        """Return True if medicine_id is already in the inventory."""
        return self.table.search_for_key(medicine_id) is not None

    def _find_medicine(self):
        """Ask for an ID and return the matching medicine, or None if it doesn't exist."""
        medicine_id = prompts.prompt_id()
        slot, medicine = self.table.search_for_slot(medicine_id)
        if medicine is None:
            display.print_error(f"Medicine {medicine_id} does not exist.")
            return None
        print(medicine)
        display.print_slot_info(slot, self.table.home_slot(medicine_id))
        return medicine

    def _run_edit_menu(self, draft):
        """Show the edit menu until the user chooses Done, updating draft in place."""
        finished = False
        while not finished:
            display.print_edit_menu()
            choice = prompts.prompt_input("Enter Choice")
            finished = self._handle_edit_choice(choice, draft)

    def _handle_edit_choice(self, choice, draft):
        """Update one field of draft. Return True when the user chooses Done."""
        match choice:
            case "1":
                draft["name"] = prompts.prompt_name()
            case "2":
                draft["size"] = prompts.prompt_size()
            case "3":
                draft["price"] = prompts.prompt_price()
            case "4":
                draft["quantity"] = prompts.prompt_quantity()
            case "5":
                return True
            case _:
                display.print_error("Invalid choice. Please enter 1–5.")
        return False

    def _compare_search_times(self, medicine_id):
        """Time the same search in the hash table and the 1D array, then show both."""
        repeats = constants.SEARCH_REPEATS
        hash_time = benchmark.average_search_time(self.table.search_for_key, medicine_id, repeats)
        array_time = benchmark.average_search_time(self.array.search, medicine_id, repeats)
        display.print_search_times(hash_time, array_time, len(self.array))
