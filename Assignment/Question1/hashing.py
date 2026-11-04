"""A hash table that resolves collisions with open addressing and linear probing."""


def is_prime(n):
    """Return True if n is a prime number."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):  # Only check divisors up to square root n
        if n % i == 0:
            return False
    return True


def next_prime(n):
    """Return the smallest prime number greater than or equal to n."""
    while not is_prime(n):
        n += 1
    return n


class LinearProbingHashTable:
    """Generic hash table storing (key, value) pairs, where keys are strings.

    Collisions are resolved by linear probing: if a slot is taken, try the next one.
    Deleted slots are marked as tombstones so searches can keep going past them.
    """

    KEY = 0  # Position of the key in each (key, value) slot
    VALUE = 1  # Position of the value in each (key, value) slot

    def __init__(self, size, base, max_load_factor):
        if size < 1 or base < 2 or not 0 < max_load_factor < 1:
            raise ValueError("Need size >= 1, base >= 2 and 0 < max_load_factor < 1")
        self.size = size                        # Number of slots (a prime spreads keys best)
        self.base = base                        # Multiplier used by the hash function
        self.max_load_factor = max_load_factor  # How full the table may get before it grows
        self.count = 0                          # Number of stored items
        self.tombstones = 0                     # Number of deleted slots
        self.table = [None] * size              # Each slot: None or (key, value)
        self.deleted = [False] * size           # True where an item was deleted

    # ==================================================================
    # Public operations
    # ==================================================================

    def insert(self, key, value):
        """Store a new key-value pair. Return the slot used, or -1 if the key already exists.

        Before storing, the table grows if it is too full of real items, or is rebuilt
        if deleted slots are making searches long.
        """
        if self.search(key) is not None:  # Duplicate key
            return -1

        if self.load_factor(extra=1) >= self.max_load_factor: # Extra refers to pending item
            self._resize(next_prime(self.size * 2))  # Too many real items: grow, e.g. 101 → 211
        elif self.occupancy(extra=1) >= self.max_load_factor:
            self._resize(self.size)  # Too many deleted slots: rebuild at the same size

        return self._place(key, value)

    def search(self, key):
        """Return the value stored for key, or None if it is not found.

        May move the key into an earlier deleted slot so later searches are shorter.
        """
        index = self._find_slot(key)  # Probe for the key's slot
        return None if index is None else self.table[index][self.VALUE]

    def search_with_slot(self, key):
        """Return (slot index, value) for key, or (None, None) if it is not found."""
        index = self._find_slot(key)
        if index is None:
            return None, None
        return index, self.table[index][self.VALUE]

    def delete(self, key):
        """Remove key, leaving a tombstone. Return True if removed, False if not found.

        The slot is marked as deleted rather than emptied, so searches for keys
        further along the same probe chain do not stop early.
        """
        index = self._find_slot(key)
        if index is None:
            return False
        self.table[index] = None
        self.deleted[index] = True  # Tombstone
        self.count -= 1
        self.tombstones += 1
        return True

    def home_slot(self, key):
        """Return the slot key hashes to before any probing."""
        return self._hash_function(key)

    def load_factor(self, extra=0):
        """Return the share of slots holding real items, optionally counting extra future items."""
        return (self.count + extra) / self.size

    def occupancy(self, extra=0):
        """Return the share of slots searches must walk past (real items plus deleted slots)."""
        return (self.count + self.tombstones + extra) / self.size

    # ==================================================================
    # Internal helpers
    # ==================================================================

    def _hash_function(self, key):
        """Turn key into a slot number using Horner's method.

        Each character's code is combined in order (value * base + code), so 'PA01'
        and 'AP01' give different slots. Taking % size at every step keeps numbers small.
        """
        hash_value = 0
        for ch in key:
            # Horner's: multiply, then add
            hash_value = (hash_value * self.base + ord(ch)) % self.size
        return (hash_value * self.base) % self.size

    def _find_slot(self, key):
        """Return the index of the slot holding key, or None if it is not found.

        Probing skips tombstones and stops at the first never-used slot, since a new
        key would have been placed there. If the key is found after a tombstone, it
        is moved into that tombstone so the next search is shorter.
        """
        table, deleted, size = self.table, self.deleted, self.size  # Local lookups
        index = self._hash_function(key)
        first_tombstone = None
        counter = 0

        while counter < size:
            slot = table[index]  # Read the slot once
            if slot is None:
                if not deleted[index]:  # Never-used: key isn't here
                    return None
                if first_tombstone is None:  # Remember the first tombstone passed
                    first_tombstone = index  # The key can be moved here if found later
            elif slot[self.KEY] == key:  # Found
                if first_tombstone is not None:  # Move it closer to home
                    table[first_tombstone] = slot
                    deleted[first_tombstone] = False
                    table[index] = None
                    deleted[index] = True
                    return first_tombstone
                return index

            index = (index + 1) % size  # Probe the next slot
            counter += 1

        return None

    def _place(self, key, value):
        """Put the pair in the first free slot from its home slot (no checks)."""
        index = self._hash_function(key)
        while self.table[index] is not None:
            index = (index + 1) % self.size  # Slot taken: try the next one, wrapping around

        if self.deleted[index]:  # Reusing a tombstone
            self.tombstones -= 1
            self.deleted[index] = False  # Tombstone index no longer dead

        self.table[index] = (key, value)
        self.count += 1

        return index

    def _resize(self, new_size):
        """Re-insert every item into a fresh table of new_size, which also removes tombstones."""
        items = [slot for slot in self.table if slot is not None]  # Keep only live items
        self.size = new_size
        self.table = [None] * new_size
        self.deleted = [False] * new_size
        self.count = 0
        self.tombstones = 0
        for key, value in items:
            self._place(key, value)

