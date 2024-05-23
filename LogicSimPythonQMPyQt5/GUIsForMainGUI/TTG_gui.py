import sys
import threading
import os
import sqlite3
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QFrame, QGroupBox, QScrollArea, QWidget, QSpinBox

try:
    import Thinkers.TruthTableToGatesThinker as TTG_Thinker
except ImportError:
    import Thinkers.TruthTableToGatesThinker as TTG_Thinker

class TTGGui(QDialog):
    # Define constants for frame widths
    INPUT_OUTPUT_FRAME_WIDTH = 300
    TRUTH_TABLE_CREATOR_FRAME_WIDTH = 1000
    OPERATIONS_FRAME_WIDTH = 200

    def __init__(self, main_menu_ref, position=(100, 100)):
        super().__init__(main_menu_ref)

        # Reference to hide/show main menu
        self.main_menu_ref = main_menu_ref
        self.main_menu_ref.hide()

        # Set window size and title
        self.resize(1250, 600)
        self.setWindowTitle('TTG')
        self.setFixedSize(1250, 600)

        # Set up the layout
        self.main_layout = QHBoxLayout()

        # Creating Frames for Input/Output, Truth Table Creator and Operations
        self.create_frames()

        # Create Widgets inside Frames
        self.create_input_output_widgets()
        self.create_operations_widgets()
        self.create_truth_table_widgets()  # Call this after creating operation widgets for proper reference setup

        self.setLayout(self.main_layout)

    def create_frames(self):
        """Creates the frames for the PyQt TTGGui program"""

        # inputOutputFrame frame will hold all the user inputs and outputs of the program
        self.input_output_frame = QGroupBox("Answer")
        self.input_output_layout = QVBoxLayout()
        self.input_output_frame.setLayout(self.input_output_layout)

        # TruthTableCreator frame holds the TruthTable frame that allows the user to interact with their truth table
        self.truth_table_creator_frame = QGroupBox("TruthTableCreator", self)
        self.truth_table_creator_layout = QVBoxLayout()
        self.truth_table_creator_frame.setLayout(self.truth_table_creator_layout)

        # OperationsFrame holds all the buttons and inputs for the program that are not directly connected to the output
        self.operations_frame = QGroupBox("Operations")
        self.operations_layout = QVBoxLayout()
        self.operations_frame.setLayout(self.operations_layout)

        # Set widths using the defined constants
        self.input_output_frame.setMaximumWidth(self.INPUT_OUTPUT_FRAME_WIDTH)
        self.truth_table_creator_frame.setMaximumWidth(self.TRUTH_TABLE_CREATOR_FRAME_WIDTH)
        self.operations_frame.setMaximumWidth(self.OPERATIONS_FRAME_WIDTH)

        # Add frames to the main layout
        self.main_layout.addWidget(self.input_output_frame)
        self.main_layout.addWidget(self.truth_table_creator_frame)
        self.main_layout.addWidget(self.operations_frame)

        # Adjust the stretch ratio to give less space to the input_output_frame
        self.main_layout.setStretch(0, 1)  # Smaller stretch for input_output_frame
        self.main_layout.setStretch(1, 2)  # Larger stretch for truth_table_creator_frame
        self.main_layout.setStretch(2, 1)  # Medium stretch for operations_frame

    def create_input_output_widgets(self):
        """Function creates all widgets related to IO frame"""

        # Label for entry box
        self.function_input_label = QLabel("Input Function:")
        self.function_input_box = QLineEdit()

        # Create output text box
        self.output_text_box = QTextEdit()
        self.output_text_box.setReadOnly(True)

        # Adding widgets to the layout
        self.input_output_layout.addWidget(self.function_input_label)
        self.input_output_layout.addWidget(self.function_input_box)
        self.input_output_layout.addWidget(self.output_text_box)

    def create_operations_widgets(self):
        """Function creates all widgets related to Operations frame"""

        # Create the calculate button
        self.btn_calculate = QPushButton("Calculate")
        self.btn_calculate.clicked.connect(self.calculate_answer)

        # Label that separates the functions
        self.function2_input_label = QLabel("--- TruthTable Functions ---")

        # Labels and entry for the number of inputs
        self.tt_num_inputs_label = QLabel("# inputs:")
        self.num_inputs_var = QSpinBox()
        self.num_inputs_var.setValue(4)

        self.tt_num_outputs_label = QLabel("# outputs:")
        self.num_outputs_var = QSpinBox()
        self.num_outputs_var.setValue(1)

        self.tt_separation_lbl = QLabel("                  ------           ")

        self.btn_generate_table = QPushButton("Generate Table")
        # Will connect slot in create_truth_table_widgets

        # Add widgets to the layout
        self.operations_layout.addWidget(self.btn_calculate)
        self.operations_layout.addWidget(self.function2_input_label)
        self.operations_layout.addWidget(self.tt_num_inputs_label)
        self.operations_layout.addWidget(self.num_inputs_var)
        self.operations_layout.addWidget(self.tt_num_outputs_label)
        self.operations_layout.addWidget(self.num_outputs_var)
        self.operations_layout.addWidget(self.tt_separation_lbl)
        self.operations_layout.addWidget(self.btn_generate_table)
        self.operations_layout.addWidget(QPushButton("Calculate Minterms", clicked=self.calculate_tt_minterms))
        self.operations_layout.addWidget(QPushButton("Calculate Maxterms", clicked=self.calculate_tt_maxterms))
        self.operations_layout.addWidget(QLabel(" --------------------------- "))
        self.operations_layout.addWidget(QPushButton("Back to main Menu", clicked=self.goto_main_menu))

    def create_truth_table_widgets(self):
        """Function creates all widgets related to TruthTableCreator frame"""
        self.truth_table_app = TruthTableApp(self.truth_table_creator_layout, self.num_inputs_var, self.num_outputs_var)
        self.btn_generate_table.clicked.connect(self.truth_table_app.wrapper_generate_table)

    def write_output_tb(self, string: str):
        """This function writes to the output box."""
        self.output_text_box.setPlainText(string)

    def calculate_answer(self):
        """Functions that starts the calculation process for single user input functions"""
        def calc():
            try:
                # Get the input from the function input box
                userfunction = self.function_input_box.text().replace(' ', '')
                TTGThinker = TTG_Thinker.TruthTableToGates(userfunction)
                self.update_output_box("Calculating!")
                TTGThinker.calculateanswer()
                answer = TTGThinker.get_Answer()
                # Update the output text box with the answer
                self.update_output_box(f"Answer ='s :\n{answer}")
            except:
                self.update_output_box("An error has occurred, try fixing your input")

        threading.Thread(target=calc).start()

    def calculate_tt_minterms(self):
        """Calculate TruthTable Minterms many outputs"""
        def calc():
            try:
                # Set up variables
                minterms, maxterms, dontcares = self.truth_table_app.GetTerms()
                num_inputs = self.truth_table_app.GetTableNumInputs()
                inputs, outputs, filenames = "", "", []

                # Calculate the numerous outputs
                for out in range(0, len(minterms)):
                    minterm = minterms[out]
                    dontcare = dontcares[out]
                    function = "F(" + ",".join([chr(65 + i) for i in range(num_inputs)]) + f") = Z'm({','.join(map(str, minterm))})"
                    if dontcare:
                        function += f"+Z'd({','.join(map(str, dontcare))})"
                    db_filename = f"{''.join(map(str, minterm[:7]))}pt{out + 1}.db"
                    filenames.append(db_filename)
                    TTGThinker = TTG_Thinker.TruthTableToGates(function, db_filename)
                    self.update_output_box("Calculating!\n")
                    TTGThinker.calculateanswer()
                    inputs += f"{function}\n"
                    outputs += f"{TTGThinker.get_Answer()}\n"
                    self.update_output_box(f"{inputs}\n{outputs}")
                    del TTGThinker
                else:
                    self.append_databases(f"{''.join(map(str, minterm[:7]))}_{len(minterms)}outputs.db", filenames)
                # Update the output text box with inputs and outputs
                self.update_output_box(f"Inputs ='s : \n{inputs}\n--\nOutputs ='s : \n{outputs}")
            except Exception as e:
                self.update_output_box(f"An error has occurred: {e}")

        threading.Thread(target=calc).start()

    def calculate_tt_maxterms(self):
        """Calculate TruthTable Maxterms many outputs"""
        def calc():
            try:
                # Set up variables
                minterms, maxterms, dontcares = self.truth_table_app.GetTerms()
                num_inputs = self.truth_table_app.GetTableNumInputs()
                inputs, outputs, filenames = "", "", []

                # Calculate the numerous outputs
                for out in range(0, len(maxterms)):
                    maxterm = maxterms[out]
                    dontcare = dontcares[out]
                    function = "F(" + ",".join([chr(65 + i) for i in range(num_inputs)]) + f") = Z'M({','.join(map(str, maxterm))})"
                    if dontcare:
                        function += f"+Z'd({','.join(map(str, dontcare))})"
                    db_filename = f"{''.join(map(str, maxterm[:7]))}pt{out + 1}.db"
                    filenames.append(db_filename)
                    TTGThinker = TTG_Thinker.TruthTableToGates(function, db_filename)
                    self.update_output_box("Calculating!\n")
                    TTGThinker.calculateanswer()
                    inputs += f"{function}\n"
                    outputs += f"{TTGThinker.get_Answer()}\n"
                    self.update_output_box(f"{inputs}\n{outputs}")
                    del TTGThinker
                else:
                    self.append_databases(f"{''.join(map(str, maxterm[:7]))}_{len(maxterms)}outputs.db", filenames)
                # Update the output text box with inputs and outputs
                self.update_output_box(f"Inputs ='s : \n{inputs}\n--\nOutputs ='s : \n{outputs}")
            except Exception as e:
                self.update_output_box(f"An error has occurred: {e}")

        threading.Thread(target=calc).start()

    def append_databases(self, dbname: str, filenames: list):
        """The AppendDatabases function creates a new SQLite database, drops any existing database with the same name,
        iterates through a list of SQLite database filenames, and integrates their contents into the new database."""

        validfilechars = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                          'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
        if os.path.exists(dbname):
            # Remove the existing database if it exists
            os.remove(dbname)
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        
        for index, filename in enumerate(filenames):
            db_conn = sqlite3.connect(filename)
            db_cursor = db_conn.cursor()
            db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = db_cursor.fetchall()
            for table_name in tables:
                original_table_name = table_name[0]
                new_table_name = f"{validfilechars[index]}_{original_table_name}"
                db_cursor.execute(f"SELECT sql FROM sqlite_master WHERE name='{original_table_name}';")
                create_table_sql = db_cursor.fetchone()[0]
                create_table_sql = create_table_sql.replace(original_table_name, new_table_name)
                cursor.execute(create_table_sql)
                db_cursor.execute(f"SELECT * FROM {original_table_name}")
                rows = db_cursor.fetchall()
                for row in rows:
                    placeholders = ', '.join(['?'] * len(row))
                    cursor.execute(f"INSERT INTO {new_table_name} VALUES ({placeholders})", row)
            db_conn.commit()
            db_conn.close()
            os.remove(filename)
        conn.commit()
        conn.close()

    def update_output_box(self, text):
        """Safely update the output box from worker threads"""
        QtCore.QMetaObject.invokeMethod(self.output_text_box, "setPlainText", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, text))

    def goto_main_menu(self):
        self.main_menu_ref.show()
        self.close()

class TruthTableApp:
    def __init__(self, layout, num_inputs_var, num_outputs_var):
        """Initialize TruthTableApp with layout, number of inputs and outputs"""
        self.main_layout = layout
        self.num_inputs_var = num_inputs_var
        self.num_outputs_var = num_outputs_var

        # Create the TruthTable frame and layout
        self.truth_table_creator_frame = QGroupBox("TruthTable")
        self.table_layout = QVBoxLayout()
        self.truth_table_creator_frame.setLayout(self.table_layout)
        self.main_layout.addWidget(self.truth_table_creator_frame)

        # Label with some directions
        self.LblDirections = QLabel("Click on output values to change them:")
        self.table_layout.addWidget(self.LblDirections)

        # Create a frame for the table
        self.table_frame = QFrame()
        self.table_layout.addWidget(self.table_frame)

        # Create a scroll area for the table
        self.TableScrollArea = QScrollArea()
        self.TableScrollArea.setWidgetResizable(True)
        self.table_layout.addWidget(self.TableScrollArea)

        # Create the widget and layout for the table
        self.TableWidget = QWidget()
        self.TableLayoutInner = QVBoxLayout()
        self.TableLayoutInner.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.TableWidget.setLayout(self.TableLayoutInner)
        self.TableScrollArea.setWidget(self.TableWidget)

        # Initialize inputs, outputs, and term variables
        self.inputs = []
        self.outputs = []
        self.minterms = []
        self.maxterms = []
        self.dontcares = []

        self.NumInputsVar = self.num_inputs_var.value()
        self.NumOutputsVar = self.num_outputs_var.value()

        # Generate the initial table
        self.GenerateTableInitalizer(self.NumInputsVar, self.NumOutputsVar, force=True)

    def wrapper_generate_table(self):
        """Wrapper function to generate the table with the current number of inputs and outputs"""
        inputs = self.num_inputs_var.value()
        outputs = self.num_outputs_var.value()
        self.GenerateTableInitalizer(inputs, outputs)

    def GenerateTableInitalizer(self, inputs=0, outputs=0, force=False):
        threading.Thread(target=self.GenerateTable(inputs, outputs, force)).start()

    def GenerateTable(self, inputs=0, outputs=0, force=False):
        """Generate the TruthTable with the specified number of inputs and outputs"""
        self.ClearTable()

        numberofwidgets = 0

        try:
            if inputs == 0:
                inputs = self.NumInputsVar
            if outputs == 0:
                outputs = self.NumOutputsVar

            numberofwidgets = (inputs*(2**inputs)) + (outputs*(2**inputs)) + (2**inputs)

            if numberofwidgets > 36864:
                QMessageBox.critical(None, "Error, TruthTable is Too large", f"Number of widgets cannont excede 36864\n widgets formula: inputs(2^inputs)+outputs(2^inputs)+(2^inputs)\n you had: {numberofwidgets}")
                return

            self.NumInputsVar = inputs
            self.NumOutputsVar = outputs
        except ValueError:
            QMessageBox.critical(None, "Error", "Please enter valid numbers for inputs and outputs.")
            return

        number_rows = 2 ** inputs
        self.output_values = [[] for _ in range(outputs)]

        # Define fixed column widths
        fixed_width_input = 10  # Reduced width for input columns
        fixed_width_output = 50
        fixed_width_num = 40

        # Create the header layout
        header_layout = QHBoxLayout()
        header_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        input_ids = [chr(i + 65) if i < 26 else chr(i + 71) for i in range(inputs)]
        for i in input_ids:
            label = QLabel(i)
            label.setFixedWidth(fixed_width_input)
            label.setAlignment(QtCore.Qt.AlignCenter)
            header_layout.addWidget(label)

        for j in range(outputs):
            label = QLabel(f"Output {j + 1}")
            label.setFixedWidth(fixed_width_output)
            label.setAlignment(QtCore.Qt.AlignCenter)
            header_layout.addWidget(label)

        label = QLabel("Num")
        label.setFixedWidth(fixed_width_num)
        label.setAlignment(QtCore.Qt.AlignCenter)
        header_layout.addWidget(label)
        self.TableLayoutInner.addLayout(header_layout)

        for i in range(number_rows):
            row_num = i
            row_layout = QHBoxLayout()
            row_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
            rows = [int(bit) for bit in bin(i)[2:].zfill(inputs)]

            for bit in rows:
                label = QLabel(str(bit))
                label.setFixedWidth(fixed_width_input)
                label.setAlignment(QtCore.Qt.AlignCenter)
                row_layout.addWidget(label)
                self.inputs.append(bit)

            for k in range(outputs):
                output = QLabel("0")
                output.setFixedSize(fixed_width_output, 30)
                output.setAlignment(QtCore.Qt.AlignCenter)
                output.setStyleSheet("background-color: white; color: black; border: 1px solid;")
                output.mousePressEvent = lambda event, row=i, col=k: self.ToggleValueOutput(row, col)
                row_layout.addWidget(output)
                self.output_values[k].append(output)

            row_num_lbl = QLabel(str(row_num))
            row_num_lbl.setFixedWidth(fixed_width_num)
            row_num_lbl.setAlignment(QtCore.Qt.AlignCenter)
            row_layout.addWidget(row_num_lbl)

            self.TableLayoutInner.addLayout(row_layout)

    def ToggleValueOutput(self, row, col):
        """Toggle the value of an output cell"""
        current_val = self.output_values[col][row].text()
        new_val = "1" if current_val == "0" else "X" if current_val == "1" else "0"
        self.output_values[col][row].setText(new_val)

    def GetTerms(self):
        """Returns three lists: minterms, maxterms, dontcares"""
        self.minterms = []
        self.maxterms = []
        self.dontcares = []

        for col, outputs in enumerate(self.output_values):
            minterms_for_output = []
            maxterms_for_output = []
            dontcares_for_output = []

            for row, output in enumerate(outputs):
                if output.text() == "1":
                    minterms_for_output.append(row)
                elif output.text() == "0":
                    maxterms_for_output.append(row)
                elif output.text() == "X":
                    dontcares_for_output.append(row)

            self.minterms.append(minterms_for_output)
            self.maxterms.append(maxterms_for_output)
            self.dontcares.append(dontcares_for_output)

        return self.minterms, self.maxterms, self.dontcares

    def GetTableNumInputs(self):
        """Returns the number of Table Inputs"""
        return self.NumInputsVar

    def GetTableNumOutputs(self):
        """Returns the number of Table Outputs"""
        return self.NumOutputsVar

    def ClearTable(self):
        """Clears the table"""
        for i in reversed(range(self.TableLayoutInner.count())):
            layout_item = self.TableLayoutInner.itemAt(i)
            widget = layout_item.widget()
            if widget:
                widget.deleteLater()
            else:
                self.clear_layout(layout_item.layout())
        self.inputs.clear()
        self.outputs.clear()

    def clear_layout(self, layout):
        """Recursively clears all layouts."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

class MainMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setGeometry(300, 200, 300, 200)

        self.btn_close = QPushButton("Close", self)
        self.btn_close.clicked.connect(self.close_application)
        self.btn_close.setGeometry(100, 80, 100, 30)
        self.hide()
        self.init_ttg_gui()

    def init_ui(self):
        self.show()

    def close_application(self):
        """Exit the application"""
        sys.exit()

    def init_ttg_gui(self):
        """Initialize the TTG GUI"""
        self.ttg_gui = TTGGui(self)
        self.ttg_gui.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())