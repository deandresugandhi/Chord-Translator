"""
A module containing AppConfig class to create the object
performing the main back-end functions.
"""


# Third-party Library Modules
import customtkinter


# Global variables
class AppConfig:
    """
    Represents the app's configuration and back-end functions.

    Contains data that have been inputted by the user as its
    attribute, and the app's main functionality as its methods
    """
    def __init__(self):
        self._accidental = customtkinter.StringVar()
        self._assigned_key = customtkinter.StringVar()
        self._filename = customtkinter.StringVar()
        self._og_filename = customtkinter.StringVar()
        self._document = None
        self._scale_dict = {
            "numerical_scale": "1 2b 2 3b 3 4 5b 5 6b 6 7b 7".split(),
            "numerical_scale_2": "1 1# 2 2# 3 4 4# 5 5# 6 6# 7".split(),
            "scale": "A Bb B C Db D Eb E F Gb G Ab".split(),
            "scale_2": "A A# B C C# D D# E F F# G G#".split()
        }

    @property
    def accidental(self):
        return self._accidental.get()

    @accidental.setter
    def accidental(self, value):
        self._accidental.set(value)

    @property
    def assigned_key(self):
        return self._assigned_key.get()

    @assigned_key.setter
    def assigned_key(self, value):
        self._assigned_key.set(value)

    @property
    def filename(self):
        return self._filename.get()

    @filename.setter
    def filename(self, value):
        self._filename.set(value)

    @property
    def og_filename(self):
        return self._og_filename.get()

    @og_filename.setter
    def og_filename(self, value):
        self._og_filename.set(value)

    @property
    def document(self):
        return self._document

    @document.setter
    def document(self, value):
        self._document = value

    @property
    def scale_dict(self):
        return self._scale_dict

    @scale_dict.setter
    def scale_dict(self, value):
        self._scale_dict = value

    def create_new_scale(self):
        """
        A method to create a chromatic scale based on inputted scale key.

        Returns the new scale as a list twelve notes, as strings.
        """
        new_scale_list = []
        chosen_scale = self.scale_dict["scale"] \
            if self.accidental == "Scale: Flat" \
            else self.scale_dict["scale_2"]
        pos_scale = chosen_scale.index(self.assigned_key)

        for i in range(12):
            new_scale_list.append(chosen_scale[(pos_scale + i) % 12])

        return new_scale_list

    def clean_chart(self):
        """
        A method to ensure all accidentals are written as sharps,
        not flats, to ease the conversion process.
        """
        universal_dictionary = dict(
            zip(self.scale_dict["numerical_scale_2"],
                self.scale_dict["numerical_scale"])
        )
        for k, v in universal_dictionary.items():
            for p in self.document.paragraphs:
                if p.text.find(k) >= 0:
                    p.text = p.text.replace(k, v)

    def convert_chart(self, new_scale_list):
        """
        A method to convert chords written in the Nashville number system
        into the traditional letter-based chord notations.

        Args:
        1. new_scale_list (list): Chromatic scale (12 notes) based on
           user-inputted scale key. Returned by create_new_scale() method.
        """
        transpose_dictionary = dict(
            zip(self.scale_dict["numerical_scale"],
                new_scale_list)
        )
        for k, v in transpose_dictionary.items():
            for p in self.document.paragraphs:
                if p.text.find(k) >= 0:
                    p.text = p.text.replace(k, v)

    def save_result(self):
        """
        A method to save the edited document.
        """
        self.document.save(self.filename)
