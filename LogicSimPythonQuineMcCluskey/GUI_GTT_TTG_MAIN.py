"""This program is the main GUI for all Thinkers involved!"""
import sys

import tkinter as tk
import tkinter.ttk as ttk

import GUIsForMainGUI.TTG_gui as TTG_gui
import GUIsForMainGUI.GTT_gui as GTT_gui
import GUIsForMainGUI.Info_gui as Info_gui

# Override tk widgets with themed ttk widgets if available
from tkinter.ttk import *
#pip install sv-ttk
# ipmort sun valley theme
import sv_ttk

class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Menu")
        self.geometry("300x200")

        self.btn_TTG_gui = Button(self, text="TruthTable to Gates", command=self.open_TTG_gui)
        self.btn_TTG_gui.pack(pady=10)

        self.btn_GTT_gui = Button(self, text="Gates to TruthTable", command=self.open_GTT_gui)
        self.btn_GTT_gui.pack(pady=10)

        self.btn_Info = Button(self, text="Info", command=self.open_Info_gui)
        self.btn_Info.pack(pady=10)

        self.btn_close = Button(self, text="Close", command=self.close_gui)
        self.btn_close.pack(pady=10)

        # Set the theme to light or dark
        sv_ttk.set_theme("dark")

    def open_TTG_gui(self):
        self.withdraw()  # Hide the main menu
        TTG_GUi = TTG_gui.TTG_gui(self)  # Pass reference to the main menu
        TTG_GUi.mainloop()
        self.deiconify()  # Show the main menu again when TTG_gui closes

    def open_GTT_gui(self):
        self.withdraw()  # Hide the main menu
        GTT_GUi = GTT_gui.GTT_gui(self)  # Pass reference to the main menu
        GTT_GUi.mainloop()
        self.deiconify()  # Show the main menu again when GTT_gui closes

    def open_Info_gui(self):
        self.withdraw()  # Hide the main menu
        INfo_GUi = Info_gui.Info_gui(self)  # Pass reference to the main menu
        INfo_GUi.mainloop()
        self.deiconify()  # Show the main menu again when Info_gui closes"""

    def close_gui(self):
        sys.exit() #Exit the program
        #self.destroy()


#Run the main Menu!-------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()



