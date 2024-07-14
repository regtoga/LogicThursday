import sys
import threading

#this is for the AppendDatabases function
import os
import sqlite3

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

try:
    import Thinkers.TruthTableToGatesThinker as TTG_Thinker
except ImportError:
    # for local use, if it worked
    import Thinkers as TTG_Thinker


class TTG_gui(tk.Toplevel):
    def __init__(self, MainMenuRef, position="+100+100"):
        super().__init__(MainMenuRef)

        #these variables set the posion and height/width of the TTG window, it is not resisable
        self.geometry(position)
        self.geometry("1500x700")
        self.resizable(False, False)

        #set the title to TTG
        self.title("TTG")

        #these are the setup functions that create the frames that the widgets go inside later
        self.CreateFrames()
        #this one creates the truthtablecreator section because its implemented very differently than the other widgets
        self.TruthTableFrame = TruthTableApp(self.TruthTableCreatorFrame)
        
        #Function creates all widgets related to IO frame
        self.CreateInputOutputWidgets()
        #Function creates all widgets related to TruthTableCreator frame
        self.CreateTruthTableWidgets()
        #Function creates all widgets related to Operations frame
        self.CreateOperationsWidgets()
        

    def CreateFrames(self):
        """Creates the frames for the tkinter TTG_gui program"""

        #inputOutputframe frame will hold all the user inputs and outputs of the program
        self.InputOutputFrame = ttk.LabelFrame(
            self,
            text="Answer",
            relief="groove"
        )
        #TruthTableCreator frame holds the TruthTable frame that allows the user to interact with their truth table
        self.TruthTableCreatorFrame = ttk.LabelFrame(
            self,
            text="TruthTableCreator",
            relief="groove",
            height=700  # Adjust the height here (700 pixels)
        )
        #OperationsFrame holds all of the buttons and inputs for the program that are not directly connected to the output 
        self.OperationsFrame = ttk.LabelFrame(
            self,
            text="Operations",
            relief="groove"
        )

        #grid the frames so that they are in the correct rows and columns
        self.InputOutputFrame.grid(row=0, column=0, sticky="NW")
        self.TruthTableCreatorFrame.grid(row=0, column=1, sticky="NW")
        self.OperationsFrame.grid(row=0, column=2, sticky="NW")

    def CreateInputOutputWidgets(self):
        """Function creates all widgets related to IO frame"""

        #create the widgets
        #label for entry box
        self.function1InputBoxLabel = ttk.Label(
            self.InputOutputFrame,
            text="Input Function: "
        )
        #entry box
        self.functionInputBox = ttk.Entry(
            self.InputOutputFrame
        )

        #create output Textbox
        self.outputtextbox = tk.Text(
            self.InputOutputFrame,
            height=30,
            width=40
        )

        # Create a vertical scrollbar
        scrollbar = tk.Scrollbar(self.InputOutputFrame, orient=tk.VERTICAL, command=self.outputtextbox.yview)
        scrollbar.grid(row=1, column=2, sticky="NS")
        #attach the scrollbar to the side of the outputextbox
        self.outputtextbox.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)
        self.outputtextbox.grid(row=1, columnspan=2, sticky="EW")

        #Grid the label and input box so that the label is left of the input box
        self.function1InputBoxLabel.grid(row=0, column=0, sticky="EW")
        self.functionInputBox.grid(row=0, column=1, sticky="EW")

        #pad the outside of the IO frame
        self.InputOutputFrame.grid_configure(padx=20, pady=(20))

        #pad each widget inside the IO frame
        for widget in self.InputOutputFrame.winfo_children():
            widget.grid_configure(padx=7, pady=7)

    def CreateTruthTableWidgets(self):
        """Function creates all widgets related to TruthTableCreator frame"""
        #pad each widget inside the TruthTableCreator frame
        for widget in self.TruthTableCreatorFrame.winfo_children():
            widget.grid_configure(padx=7, pady=7)

    def CreateOperationsWidgets(self):
        """Function creates all widgets related to Operations frame"""
        #Create the calculate button
        self.BtnCalculate = ttk.Button(
            self.OperationsFrame,
            text="Calculate",
            command=self.CalculateAnswer
        )

        #TableWidgets
        #creates the label that seperates these widgets from the rest
        self.function2InputBoxLabel = ttk.Label(
            self.OperationsFrame,
            text="--- TruthTable Functions ---"
        )

        #a label for the right side of the number of inputs entry box
        self.TTNumInputsLabel = ttk.Label(
            self.OperationsFrame,
            text="# inputs:"
        )
        #Create a variable inside the TruthTableFrame to store the number of inputs
        self.TruthTableFrame.NumInputsVar = tk.StringVar()
        self.TruthTableFrame.NumInputsVar.set('4')  # Set the default value to 4
        #the entry box that takes input from the user
        self.NumInputsEntry = ttk.Entry(
            self.OperationsFrame,
            width=2, 
            textvariable=self.TruthTableFrame.NumInputsVar
        )
        
        #a label for the right side of the number of outputs entry box
        self.TTNumOutputsLabel = ttk.Label(
            self.OperationsFrame,
            text="# outputs:"
        )
        #Create a variable inside the truthtableframe to store the number of outputs
        self.TruthTableFrame.NumOutputsVar = tk.StringVar()
        self.TruthTableFrame.NumOutputsVar.set('1')  # Set the default value to 1
        #the entry box that takes input from the user
        self.NumOutputsEntry = ttk.Entry(
            self.OperationsFrame,
            width=2, 
            textvariable=self.TruthTableFrame.NumOutputsVar
        )
        
        #seperation label between the inputs and operations of the TT
        self.TTSeperationLbl = ttk.Label(
            self.OperationsFrame,
            text="                  ------           "
        )
        
        #Btn that will delete old table and generate new table based on user inputs self.TruthTableFrame.GenerateTable
        self.BtnGenerateTable = ttk.Button(
            self.OperationsFrame, 
            text="Generate Table", 
            command=self.TruthTableFrame.GenerateTable
        )

        #Btn that will calculate the minterms based off of the inputs in the truth table
        self.BtnCalculateMinterms = ttk.Button(
            self.OperationsFrame,
            text="Calculate Minterms",
            command=self.CalculateTTMinterms
        )

        #Btn that will calculate the maxterms based off of the inputs in the truth table
        self.BtnCalculateMaxterms = ttk.Button(
            self.OperationsFrame,
            text="Calculate Maxterms",
            command=self.CalculateTTMaxterms
        )
        #end table widgets

        #Label that seperates the TT functions from the rest of the operations frame widgets
        self.LblExit = ttk.Label(
            self.OperationsFrame,
            text=" --------------------------- "
        )

        #Creates a btn that takes you back to the main menu
        self.BtnMainMenu = ttk.Button(
            self.OperationsFrame,
            text="Back to main Menu",
            command=self.GotoMainMenu
        )

        #Grids the functions inside of the create operations widgets
        self.BtnCalculate.grid(row=1, columnspan=2, sticky="EW")

        self.function2InputBoxLabel.grid(row=2, columnspan=2, sticky="EW")
        self.TTNumInputsLabel.grid(row=3, columnspan=2, sticky="EW")
        self.NumInputsEntry.grid(row=3, column=1, sticky="EW")
        self.TTNumOutputsLabel.grid(row=4, columnspan=2, sticky="EW")
        self.NumOutputsEntry.grid(row=4, column=1, sticky="EW")
        self.BtnGenerateTable.grid(row=5, columnspan=2, sticky="EW")
        self.TTSeperationLbl.grid(row=6, columnspan=2, sticky="EW")
        self.BtnCalculateMinterms.grid(row=7, columnspan=2, sticky="EW")
        self.BtnCalculateMaxterms.grid(row=8, columnspan=2, sticky="EW")

        self.LblExit.grid(row=9, columnspan=2, sticky="EW")
        self.BtnMainMenu.grid(row=10, columnspan=2, sticky="EW")

        #Pad the outside of the operations frame
        self.OperationsFrame.grid_configure(padx=20, pady=(20))

        #pad every widget inside the operations frame
        for widget in self.OperationsFrame.winfo_children():
            widget.grid_configure(padx=7, pady=7)       

    def CalculateAnswer(self):
        """Functions that starts the calculation process for single user input functions"""
        def calc():
            """Function for the worker thread to call so that the main program doesnt halt"""
            try:
                #Get the input boxes contents
                userfunction = self.functionInputBox.get()

                #this is hear because there is a bug in the TTGThinker that breaks if the input has spaces for some reason.
                userfunction = userfunction.replace(" ",'')

                #Do the calculation
                TTGThinker = TTG_Thinker.TruthTableToGates(userfunction)
                self.WriteOutputTB("Calculating!")
                TTGThinker.calculateanswer()

                #output the answer
                self.WriteOutputTB(f"Answer ='s :\n{TTGThinker.get_Answer()}")
            except:
                #output an error if user is dumb :)
                self.WriteOutputTB("An error has occurred, try fixing your input")

        #Create the worker thread
        threading.Thread(target=calc).start()

    #For Truthtable
    def CalculateTTMinterms(self):
        """Calculate TruthTable Minterms many outputs"""
        def calc():
            """Function for the worker thread to call so that the main program doesnt halt"""
            try:
                #set up variables
                minterms, Maxterms, dontcares = self.TruthTableFrame.GetTerms()
                numInputs = self.TruthTableFrame.GetTableNumInputs()
                inputs = ""
                outputs = ""
                filenames = []

                #calculate the numerous outputs
                for out in range(0, len(minterms)):
                    minterm = minterms[out]
                    dontcare = dontcares[out]
                    function = "F("
                    #this chr(65 + i) stuff essentially starts a loop at Capital A and then counts B, C, D, E...
                    #Makes the first part of the function F(A,B...
                    for i in range(0, numInputs):
                        function += f"{chr(65 + i)},"

                    #take the last comma off the end of the function string
                    function = function[:-1]
                    #add the rest of the function to the str version of the function
                    #The join function adds a comma between each minterm
                    function += f") = Z'm({','.join(map(str, minterm))})"

                    #+Z'd(6,7)
                    #add the dont cares to the end
                    if dontcares != [[]]:
                        function += f"+Z'd({','.join(map(str, dontcare))})"

                    #Each time something is being computed place the function inside the input space so that it makes since what the program is calculating at any moment
                    self.functionInputBox.delete(0, tk.END)
                    self.functionInputBox.insert(tk.END, function)

                    #Create the file name for the current database
                    DBFilename = f"{''.join(map(str, minterm[:7]))}pt{out+1}.db"
                    #append the file name to a list so that we can later take all of those files and incorporate them into a single file.
                    filenames.append(DBFilename)

                    #Do the calculation
                    TTGThinker = TTG_Thinker.TruthTableToGates(function, DBFilename)
                    self.WriteOutputTB("Calculating!")
                    TTGThinker.calculateanswer()

                    #append the input to the inputs str
                    inputs += f"{function}\n"
                    #append the output to the outputs str
                    outputs += f"{TTGThinker.get_Answer()}\n"
                    
                    #once done thinking delete the thinker
                    del TTGThinker
                
                else:
                    #this function should take all the individual databases and append them to a greater database?
                    self.AppendDatabases(f"{''.join(map(str, minterm[:7]))}_{len(minterms)}outputs.db", filenames)

                #Take the \n off the end of the strings
                inputs = inputs[:-1]
                outputs = outputs[:-1]

                self.WriteOutputTB(f"Inputs ='s : \n{inputs}\n--\nOutputs ='s : \n{outputs}")

            except:
                #output an error if user is dumb :)
                self.WriteOutputTB("An error has occurred, try making one of you output columns not all zeros")

        #Create the worker thread
        threading.Thread(target=calc).start()

    def CalculateTTMaxterms(self):
        """Calculate TruthTable Maxterms many outputs"""
        def calc():
            """Function for the worker thread to call so that the main program doesnt halt"""
            try:
                #set up variables
                minterms, Maxterms, dontcares = self.TruthTableFrame.GetTerms()
                numInputs = self.TruthTableFrame.GetTableNumInputs()
                inputs = ""
                outputs = ""
                filenames = []

                #calculate the numerous outputs
                for out in range(0, len(Maxterms)):
                    maxterm = Maxterms[out]
                    dontcare = dontcares[out]
                    function = "F("
                    #this chr(65 + i) stuff essentially starts a loop at Capital A and then counts B, C, D, E...
                    #Makes the first part of the function F(A,B...
                    for i in range(0, numInputs):
                        function += f"{chr(65 + i)},"

                    #take the last comma off the end of the function string
                    function = function[:-1]
                    #add the rest of the function to the str version of the function
                    #The join function adds a comma between each maxterm
                    function += f") = Z'M({','.join(map(str, maxterm))})"

                    #+Z'd(6,7)
                    #add the dont cares to the end
                    if dontcares != [[]]:
                        function += f"+Z'd({','.join(map(str, dontcare))})"

                    #Each time something is being computed place the function inside the input space so that it makes since what the program is calculating at any moment
                    self.functionInputBox.delete(0, tk.END)
                    self.functionInputBox.insert(tk.END, function)

                    #Create the file name for the current database
                    DBFilename = f"{''.join(map(str, maxterm[:7]))}pt{out+1}.db"
                    #append the file name to a list so that we can later take all of those files and incorporate them into a single file.
                    filenames.append(DBFilename)

                    #Do the calculation
                    TTGThinker = TTG_Thinker.TruthTableToGates(function, DBFilename)
                    self.WriteOutputTB("Calculating!")
                    TTGThinker.calculateanswer()

                    #append the input to the inputs str
                    inputs += f"{function}\n"
                    #append the output to the outputs str
                    outputs += f"{TTGThinker.get_Answer()}\n"
                    
                    #once done thinking delete the thinker
                    del TTGThinker
                
                else:
                    #this function should take all the individual databases and append them to a greater database?
                    self.AppendDatabases(f"{''.join(map(str, maxterm[:7]))}_{len(Maxterms)}outputs.db", filenames)

                #Take the \n off the end of the strings
                inputs = inputs[:-1]
                outputs = outputs[:-1]

                self.WriteOutputTB(f"Inputs ='s : \n{inputs}\n--\nOutputs ='s : \n{outputs}")

            except:
                #output an error if user is dumb :)
                self.WriteOutputTB("An error has occurred, try making one of you output columns not all zeros")

        #Create the worker thread
        threading.Thread(target=calc).start()

    def WriteOutputTB(self, string:str):
        """This function's only job is to write to the output box.
        its a function because first you have to enable editing on the box, then you have to paste the text, then you have to disable editing again!"""
        self.outputtextbox.config(state=tk.NORMAL)
        self.outputtextbox.delete('1.0', tk.END)
        self.outputtextbox.insert(tk.END, string)
        self.outputtextbox.config(state=tk.DISABLED)

    def AppendDatabases(self, dbname: str, filenames: list):
        """The AppendDatabases function creates a new SQLite database, dropping any existing database with the same name. It then iterates through a list of SQLite database filenames, 
        integrating their contents into the new database. To avoid name conflicts, it renames each table by appending a unique number based on the order of the database files. 
        After integrating each database, it deletes the original database files from the drive."""
        
        validfilechars = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')

        # Remove the existing database if it exists
        if os.path.exists(dbname):
            os.remove(dbname)

        # Connect to the new database
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()

        for index, filename in enumerate(filenames):
            # Connect to each database
            DbConn = sqlite3.connect(filename)
            DbCursor = DbConn.cursor()

            # Get the table names from the current database
            DbCursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = DbCursor.fetchall()

            for table_name in tables:
                original_table_name = table_name[0]
                new_table_name = f"{validfilechars[index]}_{original_table_name}"

                # Get the CREATE TABLE statement
                DbCursor.execute(f"SELECT sql FROM sqlite_master WHERE name='{original_table_name}';")
                CreateTableSQL = DbCursor.fetchone()[0]

                # Modify the CREATE TABLE statement to use the new table name
                CreateTableSQL = CreateTableSQL.replace(original_table_name, new_table_name)

                # Create the table in the new database
                cursor.execute(CreateTableSQL)

                # Copy all the data from the old database to the new database
                DbCursor.execute(f"SELECT * FROM {original_table_name}")
                rows = DbCursor.fetchall()
                for row in rows:
                    placeholders = ', '.join(['?'] * len(row))
                    cursor.execute(f"INSERT INTO {new_table_name} VALUES ({placeholders})", row)

            # Commit the transaction and close the old database connection
            DbConn.commit()
            DbConn.close()

            # Remove the old database file
            os.remove(filename)

        # Commit the transaction for the new database and close the connection
        conn.commit()
        conn.close()

    def GotoMainMenu(self):
        self.master.deiconify()  # Show main menu again
        self.destroy()  # Destroy current GUI

class TruthTableApp:
    def __init__(self, root):
        # Ground this window inside one referenced
        self.root = root

        # Create the Frame where the magic will happen
        self.TruthTableCreatorFrame = ttk.LabelFrame(
            root,
            text="TruthTable: ",
            relief="groove"
        )
        self.TruthTableCreatorFrame.grid(row=0, column=0, padx=10, pady=10)

        # Initialize inputs and outputs variables
        self.inputs = []
        self.outputs = []

        # these variables are initialized to store the minterms and maxterms
        self.minterms = []
        self.maxterms = []
        self.dontcares = []

        # Create a label with some directions
        self.LblDirections = tk.Label(
            self.TruthTableCreatorFrame,
            text="Click on output values to change them: "
        )
        self.LblDirections.grid(row=0, column=0)

        # Create a frame for the table to be attached to
        self.TableFrame = ttk.Frame(self.TruthTableCreatorFrame)
        self.TableFrame.grid(row=1, column=0, sticky="nsew")

        # Initialize pagination variables
        self.current_page = 0
        self.rows_per_page = 16  # Default number of rows per page now set to 16

        # Initialize input/output variable holders
        self.NumInputsVar = tk.StringVar()
        self.NumOutputsVar = tk.StringVar()
        self.NumInputsVar.set("4")  # default value
        self.NumOutputsVar.set("1")  # default value

        # Set default number of inputs/outputs
        self.TableNumInputs = int(self.NumInputsVar.get())
        self.TableNumOutputs = int(self.NumOutputsVar.get())

        # Create pagination controls
        self.CreatePaginationControls()

        # Create actual table container inside scrollable canvas
        self.TableCanvas = tk.Canvas(self.TableFrame)
        self.TableCanvas.grid(row=0, column=0, sticky="nsew")
        self.Table = ttk.Frame(self.TableCanvas)
        self.TableId = self.TableCanvas.create_window((0, 0), window=self.Table, anchor=tk.NW)
        self.Table.bind("<Configure>", self.OnTableConfigure)

        # Scrollbars
        self.TableScrollbaryY = ttk.Scrollbar(self.TableFrame, orient=tk.VERTICAL, command=self.TableCanvas.yview)
        self.TableScrollbaryY.grid(row=0, column=1, sticky="ns")
        self.TableCanvas.configure(yscrollcommand=self.TableScrollbaryY.set)

        self.TableScrollbarX = ttk.Scrollbar(self.TableFrame, orient=tk.HORIZONTAL, command=self.TableCanvas.xview)
        self.TableScrollbarX.grid(row=1, column=0, sticky="ew")
        self.TableCanvas.configure(xscrollcommand=self.TableScrollbarX.set)

        # Generate initial table
        self.GenerateTable()

    def OnTableConfigure(self, event):
        self.TableCanvas.configure(scrollregion=self.TableCanvas.bbox("all"))

    def CreatePaginationControls(self):
        """Create pagination controls"""
        nav_frame = ttk.Frame(self.TruthTableCreatorFrame)
        nav_frame.grid(row=2, column=0, pady=10)

        self.rows_per_page_var = tk.StringVar(value=self.rows_per_page)
        rows_per_page_label = ttk.Label(nav_frame, text="Rows per page:")
        rows_per_page_label.grid(row=0, column=0, padx=5)
        rows_per_page_entry = ttk.Entry(nav_frame, textvariable=self.rows_per_page_var, width=5)
        rows_per_page_entry.grid(row=0, column=1, padx=5)

        update_rows_btn = ttk.Button(nav_frame, text="Update Rows per Page", command=self.UpdateRowsPerPage)
        update_rows_btn.grid(row=0, column=2, padx=5)

        prev_btn = ttk.Button(nav_frame, text="<< Previous", command=self.PrevPage)
        prev_btn.grid(row=1, column=0, padx=5)

        self.page_label = ttk.Label(nav_frame, text="Page 1")
        self.page_label.grid(row=1, column=1, padx=5)

        next_btn = ttk.Button(nav_frame, text="Next >>", command=self.NextPage)
        next_btn.grid(row=1, column=2, padx=5)

        go_to_page_label = ttk.Label(nav_frame, text="Go to Page")
        go_to_page_label.grid(row=2, column=0, padx=5)
        self.go_to_page_var = tk.StringVar(value="1")
        go_to_page_entry = ttk.Entry(nav_frame, textvariable=self.go_to_page_var, width=5)
        go_to_page_entry.grid(row=2, column=1, padx=5)
        go_to_page_btn = ttk.Button(nav_frame, text="Go", command=self.GoToPage)
        go_to_page_btn.grid(row=2, column=2, padx=5)

    def UpdateRowsPerPage(self):
        try:
            self.rows_per_page = int(self.rows_per_page_var.get())
            self.current_page = 0
            self.GenerateTable()
        except ValueError:
            pass
            messagebox.showerror("Error", "Please enter a valid number for rows per page.")

    def UpdatePageLabel(self):
        total_rows = 2 ** self.TableNumInputs
        total_pages = (total_rows + self.rows_per_page - 1) // self.rows_per_page
        self.page_label.config(text=f"Page {self.current_page + 1} of {total_pages}")

    def PrevPage(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.GenerateTable()

    def NextPage(self):
        total_rows = 2 ** self.TableNumInputs
        total_pages = (total_rows + self.rows_per_page - 1) // self.rows_per_page
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.GenerateTable()

    def GoToPage(self):
        try:
            page = int(self.go_to_page_var.get()) - 1
            total_rows = 2 ** self.TableNumInputs
            total_pages = (total_rows + self.rows_per_page - 1) // self.rows_per_page
            if 0 <= page < total_pages:
                self.current_page = page
                self.GenerateTable()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid page number.")

    def GenerateTable(self, inputs=0, outputs=0):
        """Generates Table in the Table Frame on the Table Canvas"""
        try:
            # If the inputs aren't default use the inputs
            if inputs != 0 and outputs != 0:
                numInputs = inputs
                numOutputs = outputs
            else:  # if the inputs are default get the values of the user input boxes
                numInputs = int(self.NumInputsVar.get())
                numOutputs = int(self.NumOutputsVar.get())

            # Get rows per page from input
            try:
                rows_per_page = int(self.rows_per_page_var.get())
            except ValueError:
                rows_per_page = self.rows_per_page

            self.rows_per_page = rows_per_page

            """# This section limits the amount of outputs or inputs someone can generate
            MAXINPUTSANDOUTPUTS = 30
            if numInputs + numOutputs > MAXINPUTSANDOUTPUTS:
                messagebox.showerror("Error", f"Inputs ({numInputs}) + Outputs({numOutputs}) = {numInputs + numOutputs} <- NEEDS to be less than {MAXINPUTSANDOUTPUTS}")
                return"""

            # set these values for the getters
            self.TableNumInputs = numInputs
            self.TableNumOutputs = numOutputs

            # Ensure self.inputs is correctly sized
            self.inputs = [0] * numInputs
            self.OutputValues = [[] for _ in range(numOutputs)]

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for inputs and outputs.")  # Throw Error if the user didn't input correct things
            return

        # Clears the canvas for new widgets
        self.ClearTable()

        # Calculate the number of rows in the table using the fact the binary is 2^inputs
        NumberRows = 2 ** numInputs

        # Calculate rows for the current page
        page_start = self.current_page * self.rows_per_page
        page_end = min(page_start + self.rows_per_page, NumberRows)

        self.UpdatePageLabel()

        # for each input append the next letter of the alphabet - columns
        for i in range(numInputs):
            label = tk.Label(self.Table, text=chr(65 + i))
            label.grid(row=0, column=i + 1)

        # for the number of outputs make more output label columns
        for j in range(numOutputs):
            label = tk.Label(self.Table, text=f"Output {j + 1}")
            label.grid(row=0, column=numInputs + j + 1)

        # Create the num column
        label = tk.Label(self.Table, text="Num")
        label.grid(row=0, column=numInputs + numOutputs + 1)

        # make the rows
        for i in range(page_start, page_end):
            row_num = i
            rows = [int(bit) for bit in bin(i)[2:].zfill(numInputs)]

            for j in range(numInputs):
                label = tk.Label(self.Table, text=str(rows[j]))
                label.grid(row=i - page_start + 1, column=j + 1)

            for k in range(numOutputs):
                output = tk.Label(self.Table, text="0", bg="black", relief=tk.SOLID, borderwidth=1, width=5)
                output.grid(row=i - page_start + 1, column=numInputs + k + 1)
                output.bind("<Button-1>", lambda event, row=i, col=k: self.ToggleValueOutput(row, col))
                self.OutputValues[k].append(output)  # Store output value in the corresponding list

            RowNumLbl = tk.Label(self.Table, text=str(row_num))
            RowNumLbl.grid(row=i - page_start + 1, column=numInputs + numOutputs + 1)

        # Update page label once after generating table to correct the initial miscalculation
        self.UpdatePageLabel()

    def ToggleValueOutput(self, row, col):
        """Function toggles the value of an output button"""
        visible_row = row % self.rows_per_page
        CurrentVal = self.OutputValues[col][visible_row].cget("text")
        if CurrentVal == "0":
            NewVal = 1
        elif CurrentVal == "1":
            NewVal = "X"
        elif CurrentVal == "X":
            NewVal = 0
        self.OutputValues[col][visible_row].configure(text=str(NewVal))

    def GetTerms(self) -> list:
        """returns three things: minterms, Maxterms, dontcares"""
        self.minterms = []
        self.maxterms = []
        self.dontcares = []
        for col, outputs in enumerate(self.OutputValues):
            mintermsForOutput = []
            maxtermsForOutput = []
            dontcaresForOutput = []
            for row, output in enumerate(outputs):
                if output.cget("text") == "1":
                    mintermsForOutput.append(row + (self.current_page * self.rows_per_page))
                elif output.cget("text") == "0":
                    maxtermsForOutput.append(row + (self.current_page * self.rows_per_page))
                elif output.cget("text") == "X":
                    dontcaresForOutput.append(row + (self.current_page * self.rows_per_page))
            self.minterms.append(mintermsForOutput)
            self.maxterms.append(maxtermsForOutput)
            self.dontcares.append(dontcaresForOutput)
        return self.minterms, self.maxterms, self.dontcares

    def GetTableNumInputs(self):
        """Returns the number of Table Inputs"""
        return self.TableNumInputs

    def GetTableNumOutputs(self):
        """Returns the number of Table Outputs"""
        return self.TableNumOutputs

    def ClearTable(self):
        """Clears table"""
        for widget in self.Table.winfo_children():
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
