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
            relief="groove"
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

        
        self.outputtextbox.grid(row=1, columnspan=2, sticky="EW")


        self.function1InputBoxLabel.grid(row=0, column=0, sticky="EW")
        self.functionInputBox.grid(row=0, column=1, sticky="EW")

        self.btn_calculate.grid(row=1, columnspan=2, sticky="EW")

        self.function2InputBoxLabel.grid(row=2, columnspan=2, sticky="EW")
        self.TT_num_input_Label.grid(row=3, columnspan=2, sticky="EW")
        self.num_inputs_entry.grid(row=3, column=1, sticky="EW")
        self.generate_table_btn.grid(row=4, columnspan=2, sticky="EW")
        self.TT_seperation_lbl.grid(row=5, columnspan=2, sticky="EW")
        self.btn_Minterms_calculate.grid(row=6, columnspan=2, sticky="EW")
        self.btn_Maxterms_calculate.grid(row=7, columnspan=2, sticky="EW")

        self.exit_Label.grid(row=8, columnspan=2, sticky="EW")
        self.btn_back.grid(row=9, columnspan=2, sticky="EW")


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

                ttg_Thinker = TTG_Thinker.TruthTableToGates(userfunction)
                self.Write_output_TB("Calculating!")
                ttg_Thinker.calculateanswer()

                self.Write_output_TB(f"Answer ='s : {ttg_Thinker.get_Answer()}")
            except:
                self.Write_output_TB("An error has occurred, try fixing your input")

        threading.Thread(target=calc).start()

    #For Truthtable
    def TT_minterms(self):
        def calc():
            try:
                minterms = self.truth_table_frame.get_minterms()

                num_inputs = self.truth_table_frame.get_tablenuminputs()

                function = "F("

                for i in range(0, num_inputs):
                    function += f"{chr(65 + i)},"

                function = function[:-1]

                function += f") = Z'm({','.join(map(str, minterms))})"
                self.functionInputBox.delete(0, tk.END)
                self.functionInputBox.insert(tk.END, function)

                ttg_Thinker = TTG_Thinker.TruthTableToGates(function)
                self.Write_output_TB("Calculating!")
                ttg_Thinker.calculateanswer()

                self.Write_output_TB(f"Answer ='s : {ttg_Thinker.get_Answer()}")
            except:
                self.Write_output_TB("An error has occurred, try fixing your input")

        threading.Thread(target=calc).start()

    def TT_maxterms(self):
        def calc():
            try:
                maxterms = self.truth_table_frame.get_minterms()
                function = f"Z'M({','.join(map(str, maxterms))})"
                self.functionInputBox.delete(0, tk.END)
                self.functionInputBox.insert(tk.END, function)

                ttg_Thinker = TTG_Thinker.TruthTableToGates(function)
                self.Write_output_TB("Calculating!")
                ttg_Thinker.calculateanswer()

                self.Write_output_TB(f"Answer ='s : {ttg_Thinker.get_Answer()}")
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
        self.TruthTableCreator.pack(padx=10, pady=10)

        self.num_inputs_var = tk.StringVar()

        self.inputs = []
        self.outputs = []

        self.outputboxLabel = tk.Label(
            self.TruthTableCreator,
            text="Enter number of inputs: "
        )

        self.table_frame = tk.Frame(self.TruthTableCreator)
        self.table_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.table_canvas = tk.Canvas(self.table_frame)
        self.table_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.table_scrollbar = tk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.table_canvas.yview)
        self.table_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_canvas.configure(yscrollcommand=self.table_scrollbar.set)

        self.table = tk.Frame(self.table_canvas)
        self.table_id = self.table_canvas.create_window((0, 0), window=self.table, anchor=tk.NW)

        self.table.bind("<Configure>", self.on_table_configure)


        self.tablenuminputs = 3
        self.generate_table(self.tablenuminputs)

    def on_table_configure(self, event):
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))

    def binaryCountingWithList(self, list:list) -> list:
        "function that will do binary counting on a list of boolean values"
        listlen = len(list)
        index = listlen-1

        #all that this does is if the end of the list is already true when NOT'ing it it will make the next digit the new end and repeat the process
        while index >= 0:
            currentlistvalue = list[index]
            if currentlistvalue != True:
                list[index] = not(list[index])
                break
            list[index] = not(list[index])

            index -=1

        return list

    def generate_table(self, inputs=0):
        def generate():
            try:
                if inputs != 0:
                    num_inputs = inputs
                else:   
                    num_inputs = int(self.num_inputs_var.get())

                self.tablenuminputs = num_inputs

                if num_inputs >= 13:
                    return

            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")
                return

            self.clear_table()

            num_rows = 2 ** num_inputs

            for i in range(num_inputs):
                label = tk.Label(self.table, text=chr(65 + i))
                label.grid(row=0, column=i + 1)
                self.inputs.append(0)

            label = tk.Label(self.table, text="Output")
            label.grid(row=0, column=num_inputs + 1)

            label = tk.Label(self.table, text="Num")
            label.grid(row=0, column=num_inputs + 2)

            rows = [False for thing in range(num_inputs)]

            for i in range(num_rows):
                row_num = i

                for j in range(num_inputs):

                    if rows[j] == True:
                        val = 1
                    else:
                        val = 0

                    label = tk.Label(self.table, text=str(val))
                    label.grid(row=i + 1, column=j + 1)
                    self.inputs[j] = val

                output = tk.Label(self.table, text="0", bg="black", relief=tk.SOLID, borderwidth=1, width=5)
                output.grid(row=i + 1, column=num_inputs + 1)
                output.bind("<Button-1>", lambda event, row=i: self.toggle_output(row))
                self.outputs.append(output)
                
                row_num_lbl = tk.Label(self.table, text=str(row_num))
                row_num_lbl.grid(row=i + 1, column=num_inputs + 2)

                rows = self.binaryCountingWithList(rows)

        threading.Thread(target=generate).start()

    def toggle_output(self, row):
        current_val = int(self.outputs[row].cget("text"))
        new_val = 1 - current_val
        self.outputs[row].configure(text=str(new_val))

    def get_minterms(self):
        rows_with_output_1 = [i for i, output in enumerate(self.outputs) if int(output.cget("text")) == 1]
        self.minterms = rows_with_output_1
        return rows_with_output_1
        #messagebox.showinfo("Minterms", rows_with_output_1)

    def get_Maxterms(self):
        rows_with_output_0 = [i for i, output in enumerate(self.outputs) if int(output.cget("text")) == 0]
        self.maxterms = rows_with_output_0
        return rows_with_output_0
        #messagebox.showinfo("Maxterms", rows_with_output_0)

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
