"""Quick checks that the hash table inserts, finds, rejects duplicates, grows and deletes correctly."""
from hashing import LinearProbingHashTable

table = LinearProbingHashTable(7, 37, 0.7)  # Small table so collisions are easy to see

print("=== Home slots ===")
for key in ["PR0001", "DG0001", "PR0003", "CC0001"]:
    print(key, "->", table.home_slot(key))

print("\n=== Insert ===")
for key, name in [("PR0001", "Panadol"), ("DG0001", "Gaviscon"),
                  ("PR0003", "Nurofen"), ("CC0001", "Strepsils")]:
    print(key, "-> slot", table.insert(key, name))
print("Table size:", table.size, "| Load factor:", round(table.load_factor(), 2))

print("\n=== Search ===")
for key in ["PR0001", "DG0001", "CC0001", "XX9999"]:
    print(key, ":", table.search(key))

print("\n=== Duplicate ===")
print("Insert PR0001 again ->", table.insert("PR0001", "Copy"), "(expected -1)")

print("\n=== Growing ===")
print("5th insert would pass the 0.7 limit, so the table grows first")
print("AL0001 -> slot", table.insert("AL0001", "Zyrtec"))
print("Table size:", table.size, "(was 7) | Load factor:", round(table.load_factor(), 2))
print("All keys still found:",
      all(table.search(k) is not None for k in ["PR0001", "DG0001", "PR0003", "CC0001", "AL0001"]))

print("\n=== Tombstone ===")
print("Delete PR0001 ->", table.delete("PR0001"))
print("Search PR0001 :", table.search("PR0001"), "(expected None)")
print("Search DG0001 :", table.search("DG0001"), "(still found)")
print("Tombstones:", table.tombstones)
