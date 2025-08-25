import hashlib
import re


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
            *_,
        ) = self.flat_attr
        self.wbs = "wbs" in self.title.lower() or "wbs" in self.flat_elem.lower()
        self.hash = hashlib.sha256(self.flat_elem.encode("utf-8")).hexdigest()
        
        for i, line in enumerate(self.flat_attr):                
            # Address: anything before comma, then 5-digit zip
            if ',' in line and re.search(r'\d{5}', line):
                parts = line.split(',', 1)
                self.street = parts[0].strip()
                zip_match = re.search(r'(\d{5})', parts[1])
                if zip_match:
                    self.zip_code = zip_match.group(1)
                    self.city = parts[1].replace(self.zip_code, '').strip()
            
            # Rent: any number ending with €
            if '€' in line:
                rent_text = re.sub(r'€.*', '', line).strip()
                # Handle German number format: remove dots, replace comma with dot
                rent_text = rent_text.replace('.', '')  # Remove all dots
                rent_text = rent_text.replace(',', '.')  # Decimal separator
                try:
                    self.total_rent = float(rent_text)
                except ValueError:
                    pass
            
            # Size: any number followed by m²
            size_match = re.search(r'([\d,\.]+)\s*m²', line)
            if size_match:
                size_text = size_match.group(1).replace(',', '.')
                try:
                    self.size = float(size_text)
                except ValueError:
                    pass
            
            # Rooms: digit followed by "Zimmer" (same or next line)
            if re.match(r'^\d+$', line):
                if (i + 1 < len(self.flat_attr) and self.flat_attr[i + 1] == "Zimmer") or "Zimmer" in line:
                    self.rooms = int(line)
            elif re.search(r'(\d+).*Zimmer', line):
                self.rooms = int(re.search(r'(\d+)', line).group(1))