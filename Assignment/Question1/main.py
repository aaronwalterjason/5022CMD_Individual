"""     Starts the Over-The-Counter Pharmacy Inventory System.      """
import inventory


def main():
    """Set up the inventory with sample medicines, then show the menu."""
    system = inventory.InventorySystem()
    system.load_preloaded_medicines()
    try:
        system.run_menu()
    except (KeyboardInterrupt, EOFError):   # User forced the program to halt (Ctrl+C / Ctrl+D
        print("\nExiting Inventory System. Goodbye!")


if __name__ == "__main__":
    main()
