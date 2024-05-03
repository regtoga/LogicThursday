import sys

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

        self.textbox = tk.Text(
            self.entry_frame,
            height=20,
            width=100
        )

        # ------------------------- GRID WIDGETS ---------------------#
        self.btn_back.grid(row=0, column=0, sticky="EW")

        # set padding between frame and window
        self.entry_frame.grid_configure(padx=20, pady=(20))
        self.operations_frame.grid_configure(padx=20, pady=(20))

        # Set padding for all widgets inside the frame
        for widget in self.operations_frame.winfo_children():
            widget.grid_configure(padx=7, pady=7)

        self.textbox.pack()

        #set the textbox to have text
        self.textbox.insert(tk.END, 
"""This is the info page: 
This program in its very crude state while fully* functional should get better in the future.
There are so many things i want to add i could literally spend a full year developing this thing,
but I digress.

it is here that I will explain the GTT program at a simple level: 
the GTT (Gates to TruthTable) program takes gates in this form 
F = AB'C'DEF'G + A'B'C'D'E'FG' + A'B'C'D'E'F'G
and returns a function that describes a truth table, meaning you can construct every possible input and output from the function.

The TTG (Truth Table to Gates) program on the other hand does the opposite with a truth table,
we can minimize the ammount of logic gates needed to fufill the table.
This process is called circut minimization. These functions look like this:
F(A,B,C) = Z'm(2,3,4,5)+Z'd(6,7)

Now hopefully enough of that made sense that you can try it out for your self...
I am very thankful for anyone who has read this far and thank you for taking a look at my program!""")
        
        #make the textbox uneditable
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

    