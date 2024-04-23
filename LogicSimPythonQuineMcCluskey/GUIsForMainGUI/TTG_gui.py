import sys

import tkinter as tk
import tkinter.ttk as ttk

try:
    import Thinkers.TruthTableToGatesThinker as TTG_Thinker
except:
    #for local use, if it worked
    import Thinkers.TruthTableToGatesThinker as TTG_Thinker

#START OF TruthTable to Gates GUI class!-------------------------------------------------------------------------------------------
#This gui should take a truth table and output a minimized function
#this is how to initialize this classes thinker
#TtoG = Thinker.TruthTableToGates(userinput, databasenamefromuser)

class TTG_gui(tk.Toplevel):
    def __init__(self, main_menu_ref):
        super().__init__(main_menu_ref)

        """Initialize program GUI"""
        self.minorMax = tk.IntVar()

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
            text="Enter Function info",
            relief="groove"
        )
        self.operations_frame = ttk.LabelFrame(
            self,
            text="Operations",
            relief="groove"
        )
        #I plan to use the to let the user create whatever function they want using an interactive truthtable editor.
        self.TruthTableCreator = ttk.LabelFrame(
            self,
            text="TruthTableCreator",
            relief="groove"
        )
        
        # Grid the frames
        self.entry_frame.grid(row=0, column=0, sticky="NW")
        self.operations_frame.grid(row=0, column=1, sticky="NW")
        self.TruthTableCreator.grid(row=1, columnspan=3, sticky="N")

# ------------------------------- CREATE WIDGETS ----------------------------------#
    def create_widgets(self):
        # -------------------- CREATE BUTTONS and other interactable UI elements -----------------------------#
        # back to the main menu
        self.btn_back = ttk.Button(
            self.operations_frame,
            text="Back to main Menu",
            command=self.back_to_main_menu
        )

        #Calculate button
        self.btn_calculate = ttk.Button(
            self.operations_frame,
            text="Calculate",
            command=self.calculate_answer
        )

        #label for input box
        self.functionInputBoxLabel = ttk.Label(
            self.entry_frame,
            text="Function: "
        )
        #input box
        self.functionInputBox = ttk.Entry(
            self.entry_frame
        )

        #label for output box
        self.outputboxLabel = ttk.Label(
            self.entry_frame,
            text="Answer ='s "
        )

        self.lbloutputbox = ttk.Label(
            self.entry_frame,
            borderwidth=2,
            relief="solid",
            text="                 ",
        )

        """#-----
        #TruthTableCreator widgets

        #CheckButton that tell the program wether its solving for min or max terms
        self.checkbtn_minorMax = ttk.Checkbutton(
            self.TruthTableCreator,
            text="minterms(unchecked), Maxterms(checked)",
            offvalue=0,
            onvalue=1,
            variable=self.minorMax
        )"""

        # ------------------------- GRID WIDGETS ---------------------#
        #entry frame widgets
        self.functionInputBoxLabel.grid(row=0, column=0, sticky="EW")
        self.functionInputBox.grid(row=0, column=1, sticky="EW")

        self.outputboxLabel.grid(row=1, column=0, sticky="EW")
        self.lbloutputbox.grid(row=1, column=1, sticky="EW")

        #Operations frame widgets
        self.btn_calculate.grid(row=0, column=0, sticky="EW")
        self.btn_back.grid(row=1, column=0, sticky="EW")

        #Output frame widgets
        

        """#TruthTableCreator wigets
        self.checkbtn_minorMax.grid(row=0, column=0, sticky="EW")"""
        

        # set padding between frame and window
        self.entry_frame.grid_configure(padx=20, pady=(20))
        self.operations_frame.grid_configure(padx=20, pady=(20))
        self.TruthTableCreator.grid_configure(padx=20, pady=(20))

        # Set padding for all widgets inside the frames
        for widget in self.entry_frame.winfo_children():
            widget.grid_configure(padx=7, pady=7)

        for widget in self.operations_frame.winfo_children():
            widget.grid_configure(padx=7, pady=7)

        for widget in self.TruthTableCreator.winfo_children():
            widget.grid_configure(padx=7, pady=7)

    def calculate_answer(self):
        userfunction = self.functionInputBox.get()
        """minorMax = self.minorMax.get() """

        #print(userfunction)

        try:
            ttg_Thinker = TTG_Thinker.TruthTableToGates(userfunction)
            ttg_Thinker.calculateanswer()
            
            self.lbloutputbox.config(text=f"{ttg_Thinker.get_Answer()}")
        except:
            self.lbloutputbox.config(text=f"An error has occured, try fixing your input")
        

    def back_to_main_menu(self):
        self.master.deiconify()  # Show main menu again
        self.destroy()  # Destroy current GUI

#Run the TTG Menu!-------------------------------------------------------------------------------------------
if __name__ == "__main__":
    class MainMenu(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Main Menu")
            self.geometry("300x200")

            self.withdraw()  # Hide the main menu

            self.btn_close = tk.Button(self, text="Close", command=self.close_gui)
            self.btn_close.pack(pady=10)

            #Draw the TTG menu
            app = TTG_gui(self)
            app.mainloop()


        def close_gui(self):
            sys.exit() #Exit the program
            #self.destroy()

    ttg_gui = MainMenu()