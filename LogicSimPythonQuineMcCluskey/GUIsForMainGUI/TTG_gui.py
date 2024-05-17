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
    import Thinkers.TruthTableToGatesThinker as TTG_Thinker


class TTG_gui(tk.Toplevel):
    def __init__(self, MainMenuRef, position="+100+100"):
        super().__init__(MainMenuRef)

        #these variables set the posion and height/width of the TTG window, it is not resisable
        self.geometry(position)
        self.geometry("1050x600")
        self.resizable(False, False)

        #set the title to TTG
        self.title("TTG")

        #these variables are initialized to store the minterms and maxterms
        self.minterms = []
        self.maxterms = []

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
                minterms = self.TruthTableFrame.GetMinterms()
                numInputs = self.TruthTableFrame.GetTableNumInputs()
                inputs = ""
                outputs = ""
                filenames = []

                #calculate the numerous outputs
                for out in range(0, len(minterms)):
                    minterm = minterms[out]
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
                Maxterms = self.TruthTableFrame.GetMaxterms()
                numInputs = self.TruthTableFrame.GetTableNumInputs()
                inputs = ""
                outputs = ""
                filenames = []

                #calculate the numerous outputs
                for out in range(0, len(Maxterms)):
                    maxterm = Maxterms[out]
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
        #Ground this window inside one referenced
        self.root = root

        #Create the Frame where the magic will happen
        self.TruthTableCreatorFrame = ttk.LabelFrame(
            root,
            text="TruthTable: ",
            relief="groove"
        )
        #Pad the frame inside
        self.TruthTableCreatorFrame.grid(row=0, column=0, padx=10, pady=10)

        #Initalize inputs and outputs variables
        self.inputs = []
        self.outputs = []
        
        #Create a label with some directions
        self.LblDirections = tk.Label(
            self.TruthTableCreatorFrame,
            text="Click on output values to change them: "
        )
        self.LblDirections.grid(row=0, column=0)

        #Create a frame for the table to be attatched to
        self.TableFrame = tk.Frame(self.TruthTableCreatorFrame)
        self.TableFrame.grid(row=1, column=0, sticky="nsew")

        #Create a canvas for the parts of the TruthTable to sprall
        self.TableCanvas = tk.Canvas(self.TableFrame, height=490)  # Adjust the height here
        self.TableCanvas.grid(row=0, column=0, sticky="nsew")

        #makes a Up and Down Scrollbar
        self.TableScrollbaryY = tk.Scrollbar(self.TableFrame, orient=tk.VERTICAL, command=self.TableCanvas.yview)
        self.TableScrollbaryY.grid(row=0, column=1, sticky="ns")
        self.TableCanvas.configure(yscrollcommand=self.TableScrollbaryY.set)

        #Makes a left and right Scrollbar
        self.TableScrollbarX = tk.Scrollbar(self.TableFrame, orient=tk.HORIZONTAL, command=self.TableCanvas.xview)
        self.TableScrollbarX.grid(row=1, column=0, sticky="ew")
        self.TableCanvas.configure(xscrollcommand=self.TableScrollbarX.set)

        #Make a Table Frame
        self.Table = tk.Frame(self.TableCanvas)
        self.TableId = self.TableCanvas.create_window((0, 0), window=self.Table, anchor=tk.NW)

        #i dont actually understand what this does but i think it has to do with the scrollbars
        self.Table.bind("<Configure>", self.OnTableConfigure)

        #Generate initial table
        TABLENUMINPUTS = 4
        TABLENUMOUTPUTS = 1
        self.GenerateTable(TABLENUMINPUTS, TABLENUMOUTPUTS)

    def OnTableConfigure(self, event):
        #I dont get it
        self.TableCanvas.configure(scrollregion=self.TableCanvas.bbox("all"))

    def BinaryCountingWithList(self, list: list) -> list:
        "Function that will do binary counting on a list of boolean values"
        ListLen = len(list)
        index = ListLen - 1

        # all that this does is if the end of the list is already true when NOT'ing it it will make the next digit the new end and repeat the process
        while index >= 0:
            CurrentListValue = list[index]
            if CurrentListValue != True:
                list[index] = not (list[index])
                break
            list[index] = not (list[index])

            index -= 1

        return list

    def GenerateTable(self, inputs=0, outputs=0):
        """Generates Table in the Table Frame on the Table Canvos"""
        def generate():
            try:
                #If the inputs arenot default use the inputs
                if (inputs != 0 and outputs != 0):
                    numInputs = inputs
                    numOutputs = outputs
                #if theinputs are default get the values of the user input boxes
                else:
                    numInputs = int(self.NumInputsVar.get())
                    numOutputs = int(self.NumOutputsVar.get())

                #This section limits the ammount of outputs or inputs someone can generate
                MAXINPUTSANDOUTPUTS = 30
                if (numInputs + numOutputs) > MAXINPUTSANDOUTPUTS:
                    messagebox.showerror("Error", f"Inputs ({numInputs}) + Outputs({numOutputs}) = {numInputs + numOutputs} <- NEEDS to be less than {MAXINPUTSANDOUTPUTS}")
                    return
                
                #set these values for the getters
                self.TableNumInputs = numInputs
                self.TableNumOutputs = numOutputs
            except ValueError:
                #Throw Error if the user didnt input correct things
                messagebox.showerror("Error", "Please enter valid numbers for inputs and outputs.")
                return

            #Clears the canvus for new widgets
            self.ClearTable()

            #Calcualtes the number of rows in the table using the fact the binary is 2^inputs
            NumberRows = 2 ** numInputs

            # List of lists to store output values
            self.OutputValues = [[] for thing in range(numOutputs)]  

            #for each input append the next letter of the alphabet - columns
            for i in range(numInputs):
                label = tk.Label(self.Table, text=chr(65 + i))
                label.grid(row=0, column=i + 1)
                #i dont know why this is here i forgor
                self.inputs.append(0)

            #for the nubmer of outputs make more output label columns
            for j in range(numOutputs):
                label = tk.Label(self.Table, text=f"Output {j + 1}")
                label.grid(row=0, column=numInputs + j + 1)

            #Create the num column 
            label = tk.Label(self.Table, text="Num")
            label.grid(row=0, column=numInputs + numOutputs + 1)

            #make the rows
            for i in range(NumberRows):
                row_num = i
                rows = [int(bit) for bit in bin(i)[2:].zfill(numInputs)]

                for j in range(numInputs):
                    label = tk.Label(self.Table, text=str(rows[j]))
                    label.grid(row=i + 1, column=j + 1)
                    self.inputs[j] = rows[j]

                for k in range(numOutputs):
                    output = tk.Label(self.Table, text="0", bg="black", relief=tk.SOLID, borderwidth=1, width=5)
                    output.grid(row=i + 1, column=numInputs + k + 1)
                    output.bind("<Button-1>", lambda event, row=i, col=k: self.ToggleValueOutput(row, col))
                    self.OutputValues[k].append(output)  # Store output value in the corresponding list

                RowNumLbl = tk.Label(self.Table, text=str(row_num))
                RowNumLbl.grid(row=i + 1, column=numInputs + numOutputs + 1)

        #make it multithreaded so program doesnt halt
        threading.Thread(target=generate).start()

    def ToggleValueOutput(self, row, col):
        """Funtion toggles the value of a output button"""
        CurrentVal = int(self.OutputValues[col][row].cget("text"))
        NewVal = 1 - CurrentVal
        self.OutputValues[col][row].configure(text=str(NewVal))

    def GetMinterms(self) -> list:
        """Gets the minterms anything that has output value of 1"""
        minterms = []
        for col, outputs in enumerate(self.OutputValues):
            MintermsForOutput = []
            for row, output in enumerate(outputs):
                if int(output.cget("text")) == 1:
                    MintermsForOutput.append(row)
            minterms.append(MintermsForOutput)

        self.minterms = minterms
        # print(self.minterms)
        return minterms

    def GetMaxterms(self) -> list:
        """Gets the minterms anything that has output value of 0"""
        maxterms = []
        for col, outputs in enumerate(self.OutputValues):
            MaxtermsForOutput = []
            for row, output in enumerate(outputs):
                if int(output.cget("text")) == 0:
                    MaxtermsForOutput.append(row)
            maxterms.append(MaxtermsForOutput)

        self.maxterms = maxterms
        # print(self.maxterms)
        return maxterms

    def GetTableNumInputs(self):
        """Returns the number of Table Inputs"""
        return self.TableNumInputs
    
    def GetTableNumOutputs(self):
        """Returns the number of Table Outputs"""
        return self.TableNumOutputs

    def ClearTable(self):
        "Clears table"
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
