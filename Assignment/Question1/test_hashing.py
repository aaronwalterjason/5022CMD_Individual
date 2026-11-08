"""Compares hash table and 1D array search times on small, intermediate and large datasets."""
import benchmark
import constants
import display
import hashing
import one_dimensional_array
import product


def build_records(record_count):
    """Return record_count (ID, medicine) pairs: sample medicines first, then generated ones."""
    records = [(record[0], product.OTCMedicine(*record))
               for record in constants.PRELOADED_MEDICINES]
    used_ids = {medicine_id for medicine_id, _ in records}

    for number in range(1, 10 ** constants.NUMBER_LENGTH):
        for code in constants.CATEGORY_CODES:
            if len(records) >= record_count:
                return records[:record_count]
            medicine_id = f"{code}{number:0{constants.NUMBER_LENGTH}d}"
            if medicine_id not in used_ids:  # Skip IDs already used by the sample medicines
                records.append((medicine_id, product.OTCMedicine(
                    medicine_id, f"Test Medicine {len(records) + 1}", "1 pc", 1.00, 1)))
    return records[:record_count]


def load_structures(records):
    """Insert the same records, in the same order, into a new hash table and a new 1D array.

    Return (table, array, sizes), where sizes lists every size the table had, from first to last.
    """
    table = hashing.LinearProbingHashTable(
        constants.HASH_TABLE_SIZE, constants.HASH_BASE, constants.MAX_LOAD_FACTOR)
    array = one_dimensional_array.OneDimensionalArray()
    sizes = [table.size]

    for medicine_id, medicine in records:
        table.insert(medicine_id, medicine)
        array.insert(medicine_id, medicine)
        if table.size != sizes[-1]:  # The table resized during this insert
            sizes.append(table.size)
    return table, array, sizes


def search_cases(records):
    """Return the IDs to search: the first, middle and last in the array, and a missing one."""
    return [("First", records[0][0]),
            ("Middle", records[len(records) // 2][0]),
            ("Last", records[-1][0]),
            ("Missing", constants.MISSING_ID)]


def run_experiment():
    """Time every search case in both structures for each dataset size, and show the results."""
    repeats = constants.SEARCH_REPEATS
    for record_count in constants.DATASET_SIZES:
        records = build_records(record_count)
        table, array, sizes = load_structures(records)
        display.print_dataset_header(record_count, table.size, table.load_factor(), sizes)

        for position, medicine_id in search_cases(records):
            hash_time = benchmark.average_search_time(table.search_for_key, medicine_id, repeats)
            array_time = benchmark.average_search_time(array.search, medicine_id, repeats)
            display.print_search_row(position, medicine_id, hash_time, array_time)
    display.print_speed_up_note()


if __name__ == "__main__":
    run_experiment()