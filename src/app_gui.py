"""
A module containing AppGui class to create the object
that functions as the app's GUI
"""


# Third-party Library Modules
import customtkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
from docx.opc.exceptions import PackageNotFoundError
from docx import Document

# Local Modules
from custom_errors import *


class AppGui:
    """
    Represents the app's GUI.

    Contains CustomTkinter elements and methods that
    define the buttons' functions
    """
    font_styling = {
        "title": ('Moon Light', 45),
        "subtitle": ('Moon Bold', 20),
        "body": ('Moon Light', 18),
        "body_2": ('Moon Light', 14),
        "body_2_case_sensitive": ('Moon 2.0 Bold', 14)
    }

    def __init__(self, master, config):
        self.config = config
        self.frame = customtkinter.CTkFrame(
            master,
            fg_color="transparent"
        )
        self.title = customtkinter.CTkLabel(
            self.frame,
            text="C h o r d   T r a n s l a t o r",
            font=AppGui.font_styling["title"]
        )
        self.key_label = customtkinter.CTkLabel(
            self.frame,
            text="Insert key here: ",
            font=AppGui.font_styling["body"]
        )
        self.key_input = customtkinter.CTkEntry(
            self.frame,
            width=50,
            textvariable=self.config._assigned_key,
            font=AppGui.font_styling["body_2_case_sensitive"]
        )
        self.accidental_button_flat = customtkinter.CTkButton(
            self.frame,
            text="♭",
            font=AppGui.font_styling["body"],
            command=lambda: self.accidental_button_function("Scale: Flat")
        )
        self.accidental_button_sharp = customtkinter.CTkButton(
            self.frame,
            text="♯",
            font=AppGui.font_styling["body"],
            command=lambda: self.accidental_button_function("Scale: Sharp")
        )
        self.accidental_label = customtkinter.CTkLabel(
            self.frame,
            textvariable=self.config._accidental,
            font=AppGui.font_styling["body_2"]
        )
        self.og_file = customtkinter.CTkButton(
            self.frame,
            text="Select .docx file",
            font=AppGui.font_styling["body"],
            command=lambda: self.og_file_button_function()
        )
        self.og_file_label = customtkinter.CTkLabel(
            self.frame,
            textvariable=self.config._og_filename,
            font=AppGui.font_styling["body_2"]
        )
        self.new_file = customtkinter.CTkButton(
            self.frame,
            text="Save as",
            font=AppGui.font_styling["body"],
            command=lambda: self.save_as_button_function()
        )
        self.new_file_label = customtkinter.CTkLabel(
            self.frame,
            textvariable=self.config._filename,
            font=AppGui.font_styling["body_2"]
        )
        self.conversion_status_label = customtkinter.CTkLabel(
            self.frame,
            text="",
            font=AppGui.font_styling["body_2"]
        )
        self.convert_button = customtkinter.CTkButton(
            self.frame,
            text="Convert",
            font=AppGui.font_styling["subtitle"],
            command=lambda: self.convert_button_function()
        )
        self.space = customtkinter.CTkLabel(
            self.frame,
            text=" ",
            height=1
        )

        # Size of GUI components
        self.key_label.configure(width=300)
        self.key_input.configure(width=300)
        self.accidental_button_flat.configure(width=50)
        self.accidental_button_sharp.configure(width=50)
        self.accidental_label.configure(width=300)
        self.og_file.configure(width=250)
        self.og_file_label.configure(width=300)
        self.new_file.configure(width=250)
        self.new_file_label.configure(width=300)
        self.convert_button.configure(width=250)
        self.conversion_status_label.configure(width=300)

        # Placement of GUI components
        self.frame.place(relx=.5, rely=.5, anchor="c")
        self.title.grid(row=0, column=0, columnspan=2, pady=3)
        self.space.grid(row=1, column=0)
        self.key_label.grid(row=2, column=0, columnspan=2, pady=3)
        self.key_input.grid(row=3, column=0, columnspan=2, pady=3)
        self.accidental_button_flat.grid(row=4, column=0, pady=3, padx=1.5, sticky="E")
        self.accidental_button_sharp.grid(row=4, column=1, pady=3, padx=1.5, sticky="W")
        self.accidental_label.grid(row=5, column=0, columnspan=2, pady=3)
        self.og_file.grid(row=6, column=0, columnspan=2, pady=3)
        self.og_file_label.grid(row=7, column=0, columnspan=2, pady=3)
        self.new_file.grid(row=8, column=0, columnspan=2, pady=3)
        self.new_file_label.grid(row=9, column=0, columnspan=2, pady=3)
        self.convert_button.grid(row=10, column=0, columnspan=2, pady=3)
        self.conversion_status_label.grid(row=11, column=0, columnspan=2, pady=3)

    def validate_input(self):
        """
        A method to raise and handle errors if user input is invalid.

        Returns True if all inputs are valid, else False.
        """
        validity = True

        # To validate the scale key
        try:
            if self.config.assigned_key not in self.config.scale_dict["scale"] + self.config.scale_dict["scale_2"]:
                raise InvalidKeyError
        except InvalidKeyError as error:
            validity = error.handle_error()
            self.key_input.delete(0, 'end')
            self.key_input.insert(0, "Please input a proper key.")

        # To ensure user has selected whether to write accidentals as sharp or flat
        try:
            if self.config.accidental not in ["Scale: Sharp", "Scale: Flat"]:
                raise InvalidScaleError
        except InvalidScaleError as error:
            validity = error.handle_error()
            self.config.accidental = "Please select sharp or flat scale."

        # To check if inputted file is a valid docx file
        try:
            self.config.document = Document(self.config.og_filename)
        except PackageNotFoundError:
            print("Invalid file inputted.")
            self.config.og_filename = "Invalid File."
            validity = False

        # To check if edited file is saved as a valid docx file
        try:
            if self.config.filename in ["", "Please select file destination."]:
                raise InvalidFileError
        except InvalidFileError as error:
            validity = error.handle_error()
            self.config.filename = "Please select file destination."

        return validity

    def convert_button_function(self):
        """
        A method to define the function of the convert button.
        Executes all the main methods defined by AppConfig.
        """
        valid = self.validate_input()
        if valid:
            new_scale_list = self.config.create_new_scale()
            self.config.clean_chart()
            self.config.convert_chart(new_scale_list)
            self.config.save_result()
            print("Conversion success.")
            self.conversion_status_label.configure(text="Successfully converted! File has been saved.")
        else:
            try:
                raise ConversionError
            except ConversionError as error:
                error.handle_error()
                self.conversion_status_label.configure(text="Please fix any errors before proceeding.")

    def save_as_button_function(self):
        """
        A method to define the function of the save as button, setting
        the new docx filename.
        """
        self.config.filename = asksaveasfilename(defaultextension=".docx", filetypes=[("Word Document", ".docx")])
        if self.config.filename.split(".")[-1] == "docx" or self.config.filename == "":
            pass
        else:
            self.config.filename += ".docx"

    def accidental_button_function(self, button_name):
        """
        A method to define the function of the accidental buttons.

        Args:
        1. button_name (str): Behaviour depends on whether the flat or
           sharp button is pressed.
        """
        self.config.accidental = button_name

    def og_file_button_function(self):
        """
        A method to define the function of the button for selecting
        original docx file to be edited.
        """
        self.config.og_filename = askopenfilename()
