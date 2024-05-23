import sys
import threading  # this is for the AppendDatabases function
import os
import sqlite3

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, \
    QFrame, QGroupBox, QScrollArea, QWidget, QSpinBox

try:
    import Thinkers.TruthTableToGatesThinker as TTG_Thinker
except ImportError:
    # for local use, if it worked
    import Thinkers.TruthTableToGatesThinker as TTG_Thinker


class TTGGui(QDialog):
    def __init__(self, main_menu_ref, position=(100, 100)):
        super().__init__(main_menu_ref)
        
        # Reference to hide/show main menu
        self.main_menu_ref = main_menu_ref
        self.main_menu_ref.hide()
        
        self.resize(1050, 600)
        self.setWindowTitle('TTG')
        self.setFixedSize(1050, 600)

        # Set up the layout
        self.main_layout = QHBoxLayout()
        
        # Creating Frames for Input/Output, Truth Table Creator and Operations
        self.create_frames()
        
        # Create Widgets inside Frames
        self.create_input_output_widgets()
        self.create_truth_table_widgets()
        self.create_operations_widgets()

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
        
        # Add frames to the main layout
        self.main_layout.addWidget(self.input_output_frame)
        self.main_layout.addWidget(self.truth_table_creator_frame)
        self.main_layout.addWidget(self.operations_frame)
        
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
        
    def create_truth_table_widgets(self):
        """Function creates all widgets related to TruthTableCreator frame"""
        self.truth_table_app = TruthTableApp(self.truth_table_creator_layout)
        
    def create_operations_widgets(self):
        """Function creates all widgets related to Operations frame"""
        # Create the calculate button
        self.btn_calculate = QPushButton("Calculate")
        self.btn_calculate.clicked.connect(self.calculate_answer)
        
        self.function2_input_label = QLabel("--- TruthTable Functions ---")
        
        # labels and entry for number of inputs
        self.tt_num_inputs_label = QLabel("# inputs:")
        self.num_inputs_var = QSpinBox()
        self.num_inputs_var.setValue(4)

        self.tt_num_outputs_label = QLabel("# outputs:")
        self.num_outputs_var = QSpinBox()
        self.num_outputs_var.setValue(1)

        self.tt_separation_lbl = QLabel("                  ------           ")

        self.btn_generate_table = QPushButton("Generate Table")
        self.btn_generate_table.clicked.connect(self.truth_table_app.generate_table)

        self.btn_calculate_minterms = QPushButton("Calculate Minterms")
        self.btn_calculate_minterms.clicked.connect(self.calculate_tt_minterms)

        self.btn_calculate_maxterms = QPushButton("Calculate Maxterms")
        self.btn_calculate_maxterms.clicked.connect(self.calculate_tt_maxterms)

        self.lbl_exit = QLabel(" --------------------------- ")

        self.btn_main_menu = QPushButton("Back to main Menu")
        self.btn_main_menu.clicked.connect(self.goto_main_menu)

        self.operations_layout.addWidget(self.btn_calculate)
        self.operations_layout.addWidget(self.function2_input_label)
        self.operations_layout.addWidget(self.tt_num_inputs_label)
        self.operations_layout.addWidget(self.num_inputs_var)
        self.operations_layout.addWidget(self.tt_num_outputs_label)
        self.operations_layout.addWidget(self.num_outputs_var)
        self.operations_layout.addWidget(self.tt_separation_lbl)
        self.operations_layout.addWidget(self.btn_generate_table)
        self.operations_layout.addWidget(self.btn_calculate_minterms)
        self.operations_layout.addWidget(self.btn_calculate_maxterms)
        self.operations_layout.addWidget(self.lbl_exit)
        self.operations_layout.addWidget(self.btn_main_menu)
    
    def write_output_tb(self, string: str):
        """This function writes to the output box."""
        self.output_text_box.setPlainText(string)
    
    def calculate_answer(self):
        """Functions that starts the calculation process for single user input functions"""
        def calc():
            try:
                userfunction = self.function_input_box.text().replace(' ', '')
                TTGThinker = TTG_Thinker.TruthTableToGates(userfunction)
                self.update_output_box("Calculating!")
                TTGThinker.calculateanswer()
                answer = TTGThinker.get_Answer()
                self.update_output_box(f"Answer ='s :\n{answer}")
            except:
                self.update_output_box("An error has occurred, try fixing your input")
        
        threading.Thread(target=calc).start()
    
    def calculate_tt_minterms(self):
        """Calculate TruthTable Minterms many outputs"""
        def calc():
            try:
                minterms, maxterms, dontcares = self.truth_table_app.get_terms()
                num_inputs = self.truth_table_app.get_table_num_inputs()
                inputs, outputs, filenames = "", "", []

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
                self.update_output_box(f"Inputs ='s : \n{inputs}\n--\nOutputs ='s : \n{outputs}")
            except Exception as e:
                self.update_output_box(f"An error has occurred: {e}")
        
        threading.Thread(target=calc).start()

    def calculate_tt_maxterms(self):
        """Calculate TruthTable Maxterms many outputs"""
        def calc():
            try:
                minterms, maxterms, dontcares = self.truth_table_app.get_terms()
                num_inputs = self.truth_table_app.get_table_num_inputs()
                inputs, outputs, filenames = "", "", []

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
                self.update_output_box(f"Inputs ='s : \n{inputs}\n--\nOutputs ='s : \n{outputs}")
            except Exception as e:
                self.update_output_box(f"An error has occurred: {e}")
        
        threading.Thread(target=calc).start()

    def append_databases(self, dbname: str, filenames: list):
        validfilechars = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
        if os.path.exists(dbname):
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
        """Safely update output box from worker threads"""
        QtCore.QMetaObject.invokeMethod(self.output_text_box, "setPlainText", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, text))

    def goto_main_menu(self):
        self.main_menu_ref.show()
        self.close()

class TruthTableApp:
    def __init__(self, layout):
        self.main_layout = layout

        self.truth_table_creator_frame = QGroupBox("TruthTable")
        self.table_layout = QVBoxLayout()
        self.truth_table_creator_frame.setLayout(self.table_layout)
        self.main_layout.addWidget(self.truth_table_creator_frame)

        self.lbl_directions = QLabel("Click on output values to change them:")
        self.table_layout.addWidget(self.lbl_directions)

        self.table_frame = QFrame()
        self.table_layout.addWidget(self.table_frame)

        self.table_scroll_area = QScrollArea()
        self.table_scroll_area.setWidgetResizable(True)
        self.table_layout.addWidget(self.table_scroll_area)

        self.table_widget = QWidget()
        self.table_layout_inner = QVBoxLayout()
        self.table_widget.setLayout(self.table_layout_inner)

        self.table_scroll_area.setWidget(self.table_widget)

        self.inputs = []
        self.outputs = []
        self.minterms = []
        self.maxterms = []
        self.dontcares = []    

        self.NumInputsVar = 4
        self.NumOutputsVar = 1

        self.generate_table(force=True)

    def GenerateTable(self):
        """Wrapper for generating table using current input and output values."""
        inputs = self.main_layout.parent().num_inputs_var.value()
        outputs = self.main_layout.parent().num_outputs_var.value()
        self.generate_table(inputs, outputs, force=True)

    def generate_table(self, inputs=0, outputs=0, force=False):
        if not force:
            try:
                if inputs == 0:
                    inputs = self.NumInputsVar
                if outputs == 0:
                    outputs = self.NumOutputsVar

                if inputs + outputs > 30:
                    QMessageBox.critical(None, "Error", f"Inputs ({inputs}) + Outputs ({outputs}) = {inputs + outputs} <- NEEDS to be less than 30")
                    return

                self.NumInputsVar = inputs
                self.NumOutputsVar = outputs
            except ValueError:
                QMessageBox.critical(None, "Error", "Please enter valid numbers for inputs and outputs.")
                return

        self.clear_table()
        number_rows = 2 ** inputs
        self.output_values = [[] for _ in range(outputs)]

        header_layout = QHBoxLayout()
        input_ids = [chr(i + 65) if i < 26 else chr(i + 71) for i in range(inputs)]
        for i in input_ids:
            label = QLabel(i)
            label.setFixedWidth(30)
            header_layout.addWidget(label)

        for j in range(outputs):
            label = QLabel(f"Output {j + 1}")
            label.setFixedWidth(70)
            header_layout.addWidget(label)

        label = QLabel("Num")
        label.setFixedWidth(30)
        header_layout.addWidget(label)
        self.table_layout_inner.addLayout(header_layout)

        for i in range(number_rows):
            row_num = i
            row_layout = QHBoxLayout()
            rows = [int(bit) for bit in bin(i)[2:].zfill(inputs)]

            for bit in rows:
                label = QLabel(str(bit))
                label.setFixedWidth(30)
                row_layout.addWidget(label)
                self.inputs.append(bit)

            for k in range(outputs):
                output = QLabel("0")
                output.setFixedSize(30, 30)
                output.setAlignment(QtCore.Qt.AlignCenter)
                output.setStyleSheet("background-color: white; color: black; border: 1px solid;")
                output.mousePressEvent = lambda event, row=i, col=k: self.toggle_value_output(row, col)
                row_layout.addWidget(output)
                self.output_values[k].append(output)

            row_num_lbl = QLabel(str(row_num))
            row_num_lbl.setFixedWidth(30)
            row_layout.addWidget(row_num_lbl)

            self.table_layout_inner.addLayout(row_layout)

    def toggle_value_output(self, row, col):
        current_val = self.output_values[col][row].text()
        new_val = "1" if current_val == "0" else "X" if current_val == "1" else "0"
        self.output_values[col][row].setText(new_val)

    def get_terms(self):
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

    def get_table_num_inputs(self):
        return self.NumInputsVar

    def get_table_num_outputs(self):
        return self.NumOutputsVar

    def clear_table(self):
        for i in reversed(range(self.table_layout_inner.count())):
            layout_item = self.table_layout_inner.itemAt(i)
            if layout_item:
                widget = layout_item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    layout_item.deleteLater()
        self.inputs.clear()
        self.outputs.clear()

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
        sys.exit()

    def init_ttg_gui(self):
        self.ttg_gui = TTGGui(self)
        self.ttg_gui.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())