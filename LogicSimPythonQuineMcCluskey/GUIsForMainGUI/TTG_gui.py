import sys
import threading

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

try:
    import Thinkers.TruthTableToGatesThinker as TTG_Thinker
except ImportError:
    # for local use, if it worked
    import Thinkers.TruthTableToGatesThinker as TTG_Thinker


class TTG_gui(tk.Toplevel):
    def __init__(self, main_menu_ref, position="+100+100"):
        super().__init__(main_menu_ref)

        self.geometry(position)
        self.geometry("1050x600")
        self.resizable(False, False)

        self.title("TTG")

        self.minterms = []
        self.maxterms = []

        self.create_frames()
        self.truth_table_frame = TruthTableApp(self.TruthTableCreator)
        self.create_widgets()
        

    def create_frames(self):
        self.entry_frame = ttk.LabelFrame(
            self,
            text="Answer",
            relief="groove"
        )
        self.operations_frame = ttk.LabelFrame(
            self,
            text="Operations",
            relief="groove"
        )

        self.TruthTableCreator = ttk.LabelFrame(
            self,
            text="TruthTableCreator",
            relief="groove",
            height=700  # Adjust the height here (700 pixels)
        )

        self.entry_frame.grid(row=0, column=0, sticky="NW")
        self.TruthTableCreator.grid(row=0, column=1, sticky="NW")
        self.operations_frame.grid(row=0, column=2, sticky="NW")

    def create_widgets(self):
        self.function1InputBoxLabel = ttk.Label(
            self.entry_frame,
            text="Function: "
        )

        self.functionInputBox = ttk.Entry(
            self.entry_frame
        )

        self.btn_calculate = ttk.Button(
            self.operations_frame,
            text="Calculate",
            command=self.calculate_answer
        )

        #TableWidgets
        self.function2InputBoxLabel = ttk.Label(
            self.operations_frame,
            text="--- TruthTable Functions ---"
        )

        self.TT_num_input_Label = ttk.Label(
            self.operations_frame,
            text="# inputs:"
        )

        self.num_inputs_entry = ttk.Entry(
            self.operations_frame,
            width=2, 
            textvariable=self.truth_table_frame.num_inputs_var
        )

        self.TT_num_output_Label = ttk.Label(
            self.operations_frame,
            text="# outputs:"
        )

        self.num_outputs_entry = ttk.Entry(
            self.operations_frame,
            width=2, 
            textvariable=self.truth_table_frame.num_outputs_var
        )

        self.TT_seperation_lbl = ttk.Label(
            self.operations_frame,
            text="                  ------           "
        )

        self.generate_table_btn = ttk.Button(
            self.operations_frame, 
            text="Generate Table", 
            command=self.truth_table_frame.generate_table
        )

        self.btn_Minterms_calculate = ttk.Button(
            self.operations_frame,
            text="Calculate Minterms",
            command=self.TT_minterms
        )

        self.btn_Maxterms_calculate = ttk.Button(
            self.operations_frame,
            text="Calculate Maxterms",
            command=self.TT_maxterms
        )

        #end table widgets

        self.exit_Label = ttk.Label(
            self.operations_frame,
            text=" --------------------------- "
        )

        self.btn_back = ttk.Button(
            self.operations_frame,
            text="Back to main Menu",
            command=self.back_to_main_menu
        )


        self.outputtextbox = tk.Text(
            self.entry_frame,
            height=30,
            width=40
        )

        self.outputtextbox.config(state=tk.DISABLED)
        self.outputtextbox.grid(row=1, columnspan=2, sticky="EW")


        self.function1InputBoxLabel.grid(row=0, column=0, sticky="EW")
        self.functionInputBox.grid(row=0, column=1, sticky="EW")

        self.btn_calculate.grid(row=1, columnspan=2, sticky="EW")

        self.function2InputBoxLabel.grid(row=2, columnspan=2, sticky="EW")
        self.TT_num_input_Label.grid(row=3, columnspan=2, sticky="EW")
        self.num_inputs_entry.grid(row=3, column=1, sticky="EW")
        self.TT_num_output_Label.grid(row=4, columnspan=2, sticky="EW")
        self.num_outputs_entry.grid(row=4, column=1, sticky="EW")
        self.generate_table_btn.grid(row=5, columnspan=2, sticky="EW")
        self.TT_seperation_lbl.grid(row=6, columnspan=2, sticky="EW")
        self.btn_Minterms_calculate.grid(row=7, columnspan=2, sticky="EW")
        self.btn_Maxterms_calculate.grid(row=8, columnspan=2, sticky="EW")

        self.exit_Label.grid(row=9, columnspan=2, sticky="EW")
        self.btn_back.grid(row=10, columnspan=2, sticky="EW")


        self.entry_frame.grid_configure(padx=20, pady=(20))
        self.operations_frame.grid_configure(padx=20, pady=(20))

        for widget in self.entry_frame.winfo_children():
            widget.grid_configure(padx=7, pady=7)

        for widget in self.operations_frame.winfo_children():
            widget.grid_configure(padx=7, pady=7)
        
        for widget in self.TruthTableCreator.winfo_children():
            widget.grid_configure(padx=7, pady=7)

    def calculate_answer(self):
        def calc():
            try:
                userfunction = self.functionInputBox.get()

                #this is hear because there is a bug in the ttg_thinker that breaks if the input has spaces for some reason.
                userfunction = userfunction.replace(" ",'')

                ttg_Thinker = TTG_Thinker.TruthTableToGates(userfunction)
                self.Write_output_TB("Calculating!")
                ttg_Thinker.calculateanswer()

                self.Write_output_TB(f"Answer ='s :\n{ttg_Thinker.get_Answer()}")
            except:
                self.Write_output_TB("An error has occurred, try fixing your input")

        threading.Thread(target=calc).start()

    #For Truthtable
    def TT_minterms(self):
        def calc():
            try:
                minterms = self.truth_table_frame.get_minterms()

                num_inputs = self.truth_table_frame.get_tablenuminputs()

                answer = ""
                
                for out in range(0, len(minterms)):
                    minterm = minterms[out]
                    function = "F("

                    for i in range(0, num_inputs):
                        function += f"{chr(65 + i)},"

                    function = function[:-1]

                    function += f") = Z'm({','.join(map(str, minterm))})"
                    self.functionInputBox.delete(0, tk.END)
                    self.functionInputBox.insert(tk.END, function)

                    ttg_Thinker = TTG_Thinker.TruthTableToGates(function, f"{''.join(map(str, minterm[:7]))}pt{out+1}")
                    self.Write_output_TB("Calculating!")
                    ttg_Thinker.calculateanswer()
                    answer += f"{ttg_Thinker.get_Answer()}\n"

                answer = answer[:-1]
                    
                self.Write_output_TB(f"Answer ='s : \n{answer}")
            except:
                self.Write_output_TB("An error has occurred, try fixing your input")

        threading.Thread(target=calc).start()

    def TT_maxterms(self):
        def calc():
            try:
                maxterms = self.truth_table_frame.get_maxterms()

                num_inputs = self.truth_table_frame.get_tablenuminputs()

                answer = ""
                
                for out in range(0, len(maxterms)):
                    minterm = maxterms[out]
                    function = "F("

                    for i in range(0, num_inputs):
                        function += f"{chr(65 + i)},"

                    function = function[:-1]

                    function += f") = Z'M({','.join(map(str, minterm))})"
                    self.functionInputBox.delete(0, tk.END)
                    self.functionInputBox.insert(tk.END, function)

                    ttg_Thinker = TTG_Thinker.TruthTableToGates(function, f"{''.join(map(str, minterm[:7]))}pt{out+1}")
                    self.Write_output_TB("Calculating!")
                    ttg_Thinker.calculateanswer()
                    answer += f"{ttg_Thinker.get_Answer()}\n"

                answer = answer[:-1]
                    
                self.Write_output_TB(f"Answer ='s : \n{answer}")
            except:
                self.Write_output_TB("An error has occurred, try fixing your input")

        threading.Thread(target=calc).start()

    def Write_output_TB(self, string:str):
        self.outputtextbox.config(state=tk.NORMAL)
        self.outputtextbox.delete('1.0', tk.END)
        self.outputtextbox.insert(tk.END, string)
        self.outputtextbox.config(state=tk.DISABLED)

    def back_to_main_menu(self):
        self.master.deiconify()  # Show main menu again
        self.destroy()  # Destroy current GUI


class TruthTableApp:
    def __init__(self, root):
        self.root = root

        self.TruthTableCreator = ttk.LabelFrame(
            root,
            text="TruthTable: ",
            relief="groove"
        )
        self.TruthTableCreator.grid(row=0, column=0, padx=10, pady=10)

        self.num_inputs_var = tk.StringVar()
        self.num_outputs_var = tk.StringVar()

        self.inputs = []
        self.outputs = []

        self.outputboxLabel = tk.Label(
            self.TruthTableCreator,
            text="Enter number of inputs: "
        )
        self.outputboxLabel.grid(row=0, column=0)

        self.table_frame = tk.Frame(self.TruthTableCreator)
        self.table_frame.grid(row=1, column=0, sticky="nsew")

        self.table_canvas = tk.Canvas(self.table_frame, height=490)  # Adjust the height here
        self.table_canvas.grid(row=0, column=0, sticky="nsew")

        self.table_scrollbar_y = tk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.table_canvas.yview)
        self.table_scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.table_canvas.configure(yscrollcommand=self.table_scrollbar_y.set)

        self.table_scrollbar_x = tk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL, command=self.table_canvas.xview)
        self.table_scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.table_canvas.configure(xscrollcommand=self.table_scrollbar_x.set)

        self.table = tk.Frame(self.table_canvas)
        self.table_id = self.table_canvas.create_window((0, 0), window=self.table, anchor=tk.NW)

        self.table.bind("<Configure>", self.on_table_configure)

        self.tablenuminputs = 4
        self.tablenumoutputs = 1
        self.generate_table(self.tablenuminputs, self.tablenumoutputs)

    def on_table_configure(self, event):
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))

    def binaryCountingWithList(self, list: list) -> list:
        "function that will do binary counting on a list of boolean values"
        listlen = len(list)
        index = listlen - 1

        # all that this does is if the end of the list is already true when NOT'ing it it will make the next digit the new end and repeat the process
        while index >= 0:
            currentlistvalue = list[index]
            if currentlistvalue != True:
                list[index] = not (list[index])
                break
            list[index] = not (list[index])

            index -= 1

        return list

    def generate_table(self, inputs=0, outputs=0):
        def generate():
            try:
                if (inputs != 0 and outputs != 0):
                    num_inputs = inputs
                    num_outputs = outputs
                else:
                    num_inputs = int(self.num_inputs_var.get())
                    num_outputs = int(self.num_outputs_var.get())

                if num_inputs >= 13 or num_outputs >= 13:
                    return

                self.tablenuminputs = num_inputs
                self.tablenumoutputs = num_outputs
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for inputs and outputs.")
                return

            self.clear_table()

            num_rows = 2 ** num_inputs

            self.output_values = [[] for _ in range(num_outputs)]  # List of lists to store output values

            for i in range(num_inputs):
                label = tk.Label(self.table, text=chr(65 + i))
                label.grid(row=0, column=i + 1)
                self.inputs.append(0)

            for j in range(num_outputs):
                label = tk.Label(self.table, text=f"Output {j + 1}")
                label.grid(row=0, column=num_inputs + j + 1)

            label = tk.Label(self.table, text="Num")
            label.grid(row=0, column=num_inputs + num_outputs + 1)

            for i in range(num_rows):
                row_num = i
                rows = [int(bit) for bit in bin(i)[2:].zfill(num_inputs)]

                for j in range(num_inputs):
                    label = tk.Label(self.table, text=str(rows[j]))
                    label.grid(row=i + 1, column=j + 1)
                    self.inputs[j] = rows[j]

                for k in range(num_outputs):
                    output = tk.Label(self.table, text="0", bg="black", relief=tk.SOLID, borderwidth=1, width=5)
                    output.grid(row=i + 1, column=num_inputs + k + 1)
                    output.bind("<Button-1>", lambda event, row=i, col=k: self.toggle_output(row, col))
                    self.output_values[k].append(output)  # Store output value in the corresponding list

                row_num_lbl = tk.Label(self.table, text=str(row_num))
                row_num_lbl.grid(row=i + 1, column=num_inputs + num_outputs + 1)

        threading.Thread(target=generate).start()

    def toggle_output(self, row, col):
        current_val = int(self.output_values[col][row].cget("text"))
        new_val = 1 - current_val
        self.output_values[col][row].configure(text=str(new_val))

    def get_minterms(self) -> list:
        minterms = []
        for col, outputs in enumerate(self.output_values):
            minterms_for_output = []
            for row, output in enumerate(outputs):
                if int(output.cget("text")) == 1:
                    minterms_for_output.append(row)
            minterms.append(minterms_for_output)

        self.minterms = minterms
        # print(self.minterms)
        return minterms

    def get_maxterms(self) -> list:
        maxterms = []
        for col, outputs in enumerate(self.output_values):
            maxterms_for_output = []
            for row, output in enumerate(outputs):
                if int(output.cget("text")) == 0:
                    maxterms_for_output.append(row)
            maxterms.append(maxterms_for_output)

        self.maxterms = maxterms
        # print(self.maxterms)
        return maxterms

    def get_tablenuminputs(self):
        return self.tablenuminputs

    def clear_table(self):
        for widget in self.table.winfo_children():
            widget.destroy()
        self.inputs.clear()
        self.outputs.clear()



# Run the TTG Menu!
if __name__ == "__main__":
    class MainMenu(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Main Menu")
            self.geometry("300x200")

            self.withdraw()  # Hide the main menu

            self.btn_close = tk.Button(self, text="Close", command=self.close_gui)
            self.btn_close.pack(pady=10)

            # Draw the TTG menu
            app = TTG_gui(self)
            app.mainloop()

        def close_gui(self):
            sys.exit()  # Exit the program

    ttg_gui = MainMenu()
