"""The medicine record stored in the inventory."""
import constants


class OTCMedicine:
    """One over-the-counter medicine sold by the pharmacy."""

    def __init__(self, medicine_id, name, size, price, quantity):
        self._medicine_id = medicine_id  # str, e.g. "PR0001" (read-only, see below)
        self.name = name  # str, e.g. "Panadol"
        self.category = self._get_category()  # str, worked out from the ID's first two letters
        self.size = size  # str, free text such as "500mg" or "12 pcs"
        self.price = price  # float, in RM
        self.quantity = quantity  # int, units in stock

    @property
    def medicine_id(self):
        """Read-only, because changing it would leave the medicine in the wrong slot.
           Since hash index relies on medicine id"""
        return self._medicine_id

    def __str__(self):
        """Show the object's medicine details."""
        width = constants.LABEL_WIDTH
        return (f"\n{'Medicine ID':<{width}}: {self.medicine_id}\n"
                f"{'Name':<{width}}: {self.name}\n"
                f"{'Category':<{width}}: {self.category}\n"
                f"{'Size':<{width}}: {self.size}\n"
                f"{'Price':<{width}}: RM{self.price:.2f}\n"
                f"{'Stock':<{width}}: {self.quantity}\n")

    def _get_category(self):
        """Look up the category name from the ID's code (e.g. PR gives Pain Relief)."""
        return constants.CATEGORY_CODES[self.medicine_id[:constants.CODE_LENGTH]]
