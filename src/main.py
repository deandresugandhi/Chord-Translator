"""
The main module from which the program will be executed.
"""
# Standard Library Modules
import platform

# Third-party Library Modules
from PIL import Image, ImageTk
import customtkinter
import pyglet

# Local Modules
from app_config import AppConfig
from app_gui import AppGui


# Add font files that will be used and functionalities to ensure font works
pyglet.options['win32_gdi_font'] = True
pyglet.font.add_file('./assets/fonts/Moon_Bold.otf')
pyglet.font.add_file('./assets/fonts/Moon_Light.otf')
pyglet.font.add_file('./assets/fonts/Moon2.0-Bold.otf')
pyglet.font.add_file('./assets/fonts/Moon2.0-Light.otf')
pyglet.font.add_file('./assets/fonts/Moon2.0-Regular.otf')

# Set GUI base
root = customtkinter.CTk()
root.title("Chord Translator")
root.geometry("800x500")

icon_image = Image.open("./assets/chordtranslatorlogo.png")
photo_image = ImageTk.PhotoImage(icon_image)

root.iconphoto(False, photo_image)
root.wm_iconphoto(True, photo_image)

if platform.system() == "Windows":
    root.iconbitmap('./assets/chordtranslatorlogo.ico')

# Set GUI theme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

# Create app_config for main functions, and app_gui for main interface
app_config = AppConfig()
app_gui = AppGui(root, app_config)

root.mainloop()
