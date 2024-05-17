import sys
import os

import tkinter as tk
import tkinter.ttk as ttk

#START OF INFO GUI class!-----------------------------------------------------------------------------------------------------------
class Info_gui(tk.Toplevel):
    def __init__(self, main_menu_ref, position="+100+100"):
        super().__init__(main_menu_ref)

        """Initialize program GUI"""

        # set window location on screen 100 pixels right 100 pixels down
        # the window size will change based on the controls
        self.geometry(position)
        self.geometry("1050x600")
        self.resizable(False, False)

        """self.iconbitmap("icon.ico")"""
        self.title("GTT")
        
        # create and grid all widgets
        self.create_frames()
        self.create_widgets()

# ---------------------------------- CREATE FRAMES -----------------------------------#
    def create_frames(self):
        self.entry_frame = ttk.LabelFrame(
            self,
            text="About this program",
            relief="groove"
        )
        self.operations_frame = ttk.LabelFrame(
            self,
            text="Operations",
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

        # Create a scrollbar
        self.scrollbar = tk.Scrollbar(self.entry_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the Text widget
        self.textbox = tk.Text(
            self.entry_frame,
            height=20,
            width=100,
            yscrollcommand=self.scrollbar.set
        )

        # Configure the scrollbar to work with the Text widget
        self.scrollbar.config(command=self.textbox.yview)

        # ------------------------- GRID WIDGETS ---------------------#
        self.btn_back.grid(row=0, column=0, sticky="EW")

        # set padding between frame and window
        self.entry_frame.grid_configure(padx=20, pady=(20))
        self.operations_frame.grid_configure(padx=20, pady=(20))

        # Set padding for all widgets inside the frame
        for widget in self.operations_frame.winfo_children():
            widget.grid_configure(padx=7, pady=7)

        self.textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Load the content of info.txt into the Text widget
        try:
            # Get the directory where the script is located
            script_dir = os.path.dirname(__file__)
            # Construct the full path to the info.txt file
            file_path = os.path.join(script_dir, 'info.txt')

            with open(file_path, 'r') as file:
                content = file.read()
                self.textbox.insert(tk.END, content)
        except FileNotFoundError:
            self.textbox.insert(tk.END, "info.txt file not found.")

        # Make the textbox uneditable
        self.textbox.config(state=tk.DISABLED)

    def back_to_main_menu(self):
        self.master.deiconify()  # Show main menu again
        self.destroy()  # Destroy current GUI

#Run the Info Menu!-------------------------------------------------------------------------------------------
if __name__ == "__main__":
    class MainMenu(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Main Menu")
            self.geometry("300x200")

            self.withdraw()  # Hide the main menu

            self.btn_close = tk.Button(self, text="Close", command=self.close_gui)
            self.btn_close.pack(pady=10)

            #Draw the info menu
            app = Info_gui(self)
            app.mainloop()


        def close_gui(self):
            sys.exit() #Exit the program
            #self.destroy()

    info_gui = MainMenu()

    