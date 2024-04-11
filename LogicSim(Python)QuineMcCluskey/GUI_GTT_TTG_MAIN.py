"""This program is the main GUI for all Thinkers involved!"""
import sys

import tkinter as tk
import tkinter.ttk as ttk

import TruthTableToGatesThinker as TTG_Thinker
import GatesToTableThinker as GTT_Thinker

class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Menu")
        self.geometry("300x200")

        self.btn_GTT_gui = tk.Button(self, text="Gates to TruthTable", command=self.open_GTT_gui)
        self.btn_GTT_gui.pack(pady=10)
        
        self.btn_TTG_gui = tk.Button(self, text="TruthTable to Gates", command=self.open_TTG_gui)
        self.btn_TTG_gui.pack(pady=10)

        self.btn_Info = tk.Button(self, text="Info", command=self.open_Info_gui)
        self.btn_Info.pack(pady=10)

        self.btn_close = tk.Button(self, text="Close", command=self.close_gui)
        self.btn_close.pack(pady=10)

    def open_GTT_gui(self):
        self.withdraw()  # Hide the main menu
        GTT_GUi = GTT_gui(self)  # Pass reference to the main menu
        GTT_GUi.mainloop()
        self.deiconify()  # Show the main menu again when GTT_gui closes

    def open_TTG_gui(self):
        self.withdraw()  # Hide the main menu
        TTG_GUi = TTG_gui(self)  # Pass reference to the main menu
        TTG_GUi.mainloop()
        self.deiconify()  # Show the main menu again when TTG_gui closes

    def open_Info_gui(self):
        self.withdraw()  # Hide the main menu
        INfo_GUi = Info_gui(self)  # Pass reference to the main menu
        INfo_GUi.mainloop()
        self.deiconify()  # Show the main menu again when Info_gui closes"""

    def close_gui(self):
        sys.exit() #Exit the program
        #self.destroy()

#START OF Gates to TruthTable GUI class!-------------------------------------------------------------------------------------------
class GTT_gui(tk.Toplevel):
    def __init__(self, main_menu_ref):
        super().__init__(main_menu_ref)

        """Initialize program GUI"""

        # set window location on screen 400 pixels right 300 pixels down
        # the window size will change based on the controls
        self.geometry("+400+300")
        """self.iconbitmap("icon.ico")"""
        self.title("GTT")
        self.resizable(False, False)
        # create and grid all widgets
        self.create_frames()
        self.create_widgets()

# ---------------------------------- CREATE FRAMES -----------------------------------#
    def create_frames(self):
        self.entry_frame = ttk.LabelFrame(
            self,
            text="Enter Customer Info",
            relief="groove"
        )
        self.operations_frame = ttk.LabelFrame(
            self,
            text="Operations Frame",
            relief="groove"
        )
        # Grid the frames
        self.entry_frame.grid(row=0, column=0, sticky="NW")
        self.operations_frame.grid(row=0, column=1, sticky="N")

# ------------------------------- CREATE WIDGETS ----------------------------------#
    def create_widgets(self):
        # -------------------- CREATE BUTTONS -----------------------------#
        # back to the main menu
        self.btn_back = ttk.Button(
            self.operations_frame,
            text="Back to main Menu",
            command=self.back_to_main_menu
        )

        # ------------------------- GRID WIDGETS ---------------------#
        self.btn_back.grid(row=0, column=0, sticky="EW")

        # set padding between frame and window
        self.entry_frame.grid_configure(padx=20, pady=(20))
        self.operations_frame.grid_configure(padx=20, pady=(20))

        # Set padding for all widgets inside the frame
        for widget in self.operations_frame.winfo_children():
            widget.grid_configure(padx=7, pady=7)

    def back_to_main_menu(self):
        self.master.deiconify()  # Show main menu again
        self.destroy()  # Destroy current GUI

#START OF TruthTable to Gates GUI class!-------------------------------------------------------------------------------------------
class TTG_gui(tk.Toplevel):
    def __init__(self, main_menu_ref):
        super().__init__(main_menu_ref)

        """Initialize program GUI"""

        # set window location on screen 400 pixels right 300 pixels down
        # the window size will change based on the controls
        self.geometry("+400+300")
        """self.iconbitmap("icon.ico")"""
        self.title("TTG")
        self.resizable(False, False)
        # create and grid all widgets
        self.create_frames()
        self.create_widgets()

# ---------------------------------- CREATE FRAMES -----------------------------------#
    def create_frames(self):
        self.entry_frame = ttk.LabelFrame(
            self,
            text="Enter Customer Info",
            relief="groove"
        )
        self.operations_frame = ttk.LabelFrame(
            self,
            text="Operations Frame",
            relief="groove"
        )
        # Grid the frames
        self.entry_frame.grid(row=0, column=0, sticky="NW")
        self.operations_frame.grid(row=0, column=1, sticky="N")

# ------------------------------- CREATE WIDGETS ----------------------------------#
    def create_widgets(self):
        # -------------------- CREATE BUTTONS -----------------------------#
        # back to the main menu
        self.btn_back = ttk.Button(
            self.operations_frame,
            text="Back to main Menu",
            command=self.back_to_main_menu
        )

        # ------------------------- GRID WIDGETS ---------------------#
        self.btn_back.grid(row=0, column=0, sticky="EW")

        # set padding between frame and window
        self.entry_frame.grid_configure(padx=20, pady=(20))
        self.operations_frame.grid_configure(padx=20, pady=(20))

        # Set padding for all widgets inside the frame
        for widget in self.operations_frame.winfo_children():
            widget.grid_configure(padx=7, pady=7)

    def back_to_main_menu(self):
        self.master.deiconify()  # Show main menu again
        self.destroy()  # Destroy current GUI

#START OF INFO GUI class!-----------------------------------------------------------------------------------------------------------
class Info_gui(tk.Toplevel):
    def __init__(self, main_menu_ref):
        super().__init__(main_menu_ref)

        """Initialize program GUI"""

        # set window location on screen 400 pixels right 300 pixels down
        # the window size will change based on the controls
        self.geometry("+400+300")
        """self.iconbitmap("icon.ico")"""
        self.title("GTT")
        self.resizable(False, False)
        # create and grid all widgets
        self.create_frames()
        self.create_widgets()

# ---------------------------------- CREATE FRAMES -----------------------------------#
    def create_frames(self):
        self.entry_frame = ttk.LabelFrame(
            self,
            text="Enter Customer Info",
            relief="groove"
        )
        self.operations_frame = ttk.LabelFrame(
            self,
            text="Operations Frame",
            relief="groove"
        )
        # Grid the frames
        self.entry_frame.grid(row=0, column=0, sticky="NW")
        self.operations_frame.grid(row=0, column=1, sticky="N")

# ------------------------------- CREATE WIDGETS ----------------------------------#
    def create_widgets(self):
        # -------------------- CREATE BUTTONS -----------------------------#
        # back to the main menu
        self.btn_back = ttk.Button(
            self.operations_frame,
            text="Back to main Menu",
            command=self.back_to_main_menu
        )

        # ------------------------- GRID WIDGETS ---------------------#
        self.btn_back.grid(row=0, column=0, sticky="EW")

        # set padding between frame and window
        self.entry_frame.grid_configure(padx=20, pady=(20))
        self.operations_frame.grid_configure(padx=20, pady=(20))

        # Set padding for all widgets inside the frame
        for widget in self.operations_frame.winfo_children():
            widget.grid_configure(padx=7, pady=7)

    def back_to_main_menu(self):
        self.master.deiconify()  # Show main menu again
        self.destroy()  # Destroy current GUI


#Run the main Menu!-------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()



