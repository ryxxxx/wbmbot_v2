import hashlib


class Flat:
    """
    A class to represent a flat listing.

    This class takes a string representation of a flat listing, splits it by new lines,
    and assigns various attributes based on the content of each line.

    Attributes:
        title (str): The title of the flat listing.
        district (str): The district where the flat is located.
        street (str): The street address of the flat.
        zip_code (str): The postal code for the flat's location.
        city (str): The city where the flat is located.
        total_rent (str): The total rent cost for the flat.
        size (str): The size of the flat.
        rooms (str): The number of rooms in the flat.
        wbs (bool): A boolean indicating if the flat has a Wohnberechtigungsschein (WBS).
        hash (str): A SHA-256 hash of the flat listing details.
    """

    def __init__(self, flat_elem, test: bool):
        """
        Constructs all the necessary attributes for the flat object.

        Parameters:
            flat_elem (str): The string representation of the flat listing.
        """
        self.flat_elem = flat_elem
        self.test = test
        self.flat_attr = self.flat_elem.split("\n")
        if not self.test:
            self.flat_attr = [item for item in self.flat_attr if item.strip()]
        self.attr_size = len(self.flat_attr)
        print(self.flat_attr) if self.test else None
        (
            self.district,
            self.title,
            address,
            self.total_rent,
            ignore_1,
            self.size,
            ignore_2,
            self.rooms,
            *_,
        ) = self.flat_attr
        self.street, zip_info = address.rsplit(',', 1)
        self.zip_code, self.city = zip_info.split()
        self.wbs = "wbs" in self.title.lower() or "wbs" in self.flat_elem.lower()
        self.hash = hashlib.sha256(self.flat_elem.encode("utf-8")).hexdigest()
