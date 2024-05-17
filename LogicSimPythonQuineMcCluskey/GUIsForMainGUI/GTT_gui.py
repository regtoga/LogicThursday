import sys
import threading

import tkinter as tk
import tkinter.ttk as ttk

try:
    import Thinkers.GatesToTableThinker as GTT_Thinker
except:
    #for local use, if it worked
    import Thinkers.GatesToTableThinker as GTT_Thinker

#START OF Gates to TruthTable GUI class!-------------------------------------------------------------------------------------------
class GTT_gui(tk.Toplevel):
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
            text="Enter Function info",
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
        self.btn_calculate = ttk.Button(
            self.operations_frame,
            text="Calculate",
            command=self.calculate_answer
        )
        
        # back to the main menu
        self.btn_back = ttk.Button(
            self.operations_frame,
            text="Back to main Menu",
            command=self.back_to_main_menu
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

        self.outputtextbox = tk.Text(
            self.entry_frame,
            height=30,
            width=40
        )

        # ------------------------- GRID WIDGETS ---------------------#
        
        # Create a vertical scrollbar
        scrollbar = tk.Scrollbar(self.entry_frame, orient=tk.VERTICAL, command=self.outputtextbox.yview)
        scrollbar.grid(row=1, column=2, sticky="NS")

        self.outputtextbox.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)
        self.outputtextbox.grid(row=1, columnspan=2, sticky="EW")

        #entry frame widgets
        self.functionInputBoxLabel.grid(row=0, column=0, sticky="EW")
        self.functionInputBox.grid(row=0, column=1, sticky="EW")
        self.outputtextbox.grid(row=1, columnspan=2, sticky="EW")

        #operations frame widgets
        self.btn_calculate.grid(row=0, column=0, sticky="EW")
        self.btn_back.grid(row=1, column=0, sticky="EW")

        # set padding between frame and window
        self.entry_frame.grid_configure(padx=20, pady=(20))
        self.operations_frame.grid_configure(padx=20, pady=(20))

        # Set padding for all widgets inside the frames
        for widget in self.operations_frame.winfo_children():
            widget.grid_configure(padx=7, pady=7)
            
        for widget in self.entry_frame.winfo_children():
            widget.grid_configure(padx=7, pady=7)

    def calculate_answer(self):
        userfunction = self.functionInputBox.get()
        
        def calc():
            try:
                self.Write_output_TB("Calculating!")
                gtt_Thinker = GTT_Thinker.TruthTableToGates(userfunction)

                self.Write_output_TB(f"{gtt_Thinker.get_AnswerFunction()}")
            except:
                self.Write_output_TB("An error has occured, try fixing your input")
        
        threading.Thread(target=calc).start()

    def back_to_main_menu(self):
        self.master.deiconify()  # Show main menu again
        self.destroy()  # Destroy current GUI

    def Write_output_TB(self, string:str):
        self.outputtextbox.config(state=tk.NORMAL)
        self.outputtextbox.delete('1.0', tk.END)
        self.outputtextbox.insert(tk.END, string)
        self.outputtextbox.config(state=tk.DISABLED)


#Run the GTT Menu!-------------------------------------------------------------------------------------------
if __name__ == "__main__":
    class MainMenu(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Main Menu")
            self.geometry("300x200")

            self.withdraw()  # Hide the main menu

            self.btn_close = tk.Button(self, text="Close", command=self.close_gui)
            self.btn_close.pack(pady=10)

            #Draw the GTT menu
            app = GTT_gui(self)
            app.mainloop()

        def close_gui(self):
            sys.exit() #Exit the program
            #self.destroy()

    gtt_gui = MainMenu()