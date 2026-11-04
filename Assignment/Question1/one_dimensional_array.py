"""A plain one-dimensional array, used as the baseline to compare the hash table against."""

class OneDimensionalArray:
    """Generic 1D array that stores (key, value) pairs and searches item by item. """

    def __init__(self):
        self.items = []  # Each item: (key, value)

    def __len__(self):
        """Return how many items are stored."""
        return len(self.items)

    def insert(self, key, value):
        """Add the pair at the end and return its position. O(1)."""
        self.items.append((key, value))
        return len(self.items) - 1

    def search(self, key):
        """Return the value for key by checking every item in turn, or None if not found. O(n)."""
        for stored_key, value in self.items:
            if stored_key == key:
                return value
        return None

    def delete(self, key):
        """Remove the pair with key. Return True if removed, False if not found.

        O(n): it scans to find the key, then every later item shifts down one place.
        """
        for index, (stored_key, _) in enumerate(self.items):
            if stored_key == key:
                del self.items[index]
                return True
        return False
