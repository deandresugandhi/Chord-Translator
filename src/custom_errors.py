"""
A module containing all custom errors used in the program.
"""


class CustomError(Exception):
    """
    Base custom error template for all custom errors. Stores
    a unique message as attribute.
    """
    def __init__(self, message="Custom Message"):
        super().__init__(message)
        self.custom_message = message

    def handle_error(self):
        """
        A method that defines how errors are handled, by printing
        custom error messages.

        Returns False, to be used for validation purposes in other
        functions or methods.
        """
        print(self.custom_message)
        return False


class InvalidKeyError(CustomError):
    """Raised when an invalid key is encountered."""
    def __init__(self, message="Invalid key inputted."):
        super().__init__(message)


class InvalidScaleError(CustomError):
    """Raised when an invalid scale is encountered."""
    def __init__(self, message="Invalid scale inputted."):
        super().__init__(message)


class InvalidFileError(CustomError):
    """Raised when an invalid file is encountered."""
    def __init__(self, message="Invalid file inputted."):
        super().__init__(message)


class ConversionError(CustomError):
    """Raised when the conversion process fails."""
    def __init__(self, message="Conversion Error. Please ensure all input are valid."):
        super().__init__(message)
