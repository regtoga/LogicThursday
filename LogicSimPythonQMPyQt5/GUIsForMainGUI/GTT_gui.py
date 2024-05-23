import sys
import threading
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QGroupBox

try:
    import Thinkers.GatesToTableThinker as GTT_Thinker
except ImportError:
    import Thinkers.GatesToTableThinker as GTT_Thinker

class GTTGui(QDialog):

    output_signal = QtCore.pyqtSignal(str)

    def __init__(self, main_menu_ref):
        super().__init__(main_menu_ref)

        self.output_signal.connect(self.write_output_tb)

        # Reference to hide/show main menu
        self.main_menu_ref = main_menu_ref
        self.main_menu_ref.hide()

        # Set window size and title
        self.resize(1050, 600)
        self.setWindowTitle('GTT')
        self.setFixedSize(1050, 600)

        # Set up the layout
        self.main_layout = QHBoxLayout()

        # Creating Frames for Input/Output and Operations
        self.create_frames()

        # Create Widgets inside Frames
        self.create_input_output_widgets()
        self.create_operations_widgets()

        self.setLayout(self.main_layout)

    def create_frames(self):
        """Creates the frames for the PyQt GTTGui program"""

        # inputOutputFrame frame will hold all the user inputs and outputs of the program
        self.entry_frame = QGroupBox("Enter Function info")
        self.entry_frame_layout = QVBoxLayout()
        self.entry_frame.setLayout(self.entry_frame_layout)

        # OperationsFrame holds all the buttons and inputs for the program that are not directly connected to the output
        self.operations_frame = QGroupBox("Operations")
        self.operations_layout = QVBoxLayout()
        self.operations_frame.setLayout(self.operations_layout)

        # Add frames to the main layout
        self.main_layout.addWidget(self.entry_frame)
        self.main_layout.addWidget(self.operations_frame)

    def create_input_output_widgets(self):
        """Function creates all widgets related to input/output frame"""

        # Label for entry box
        self.function_input_label = QLabel("Function:")
        self.function_input_box = QLineEdit()

        # Create output text box
        self.output_text_box = QTextEdit()
        self.output_text_box.setReadOnly(True)

        # Adding widgets to the layout
        self.entry_frame_layout.addWidget(self.function_input_label)
        self.entry_frame_layout.addWidget(self.function_input_box)
        self.entry_frame_layout.addWidget(self.output_text_box)

    def create_operations_widgets(self):
        """Function creates all widgets related to Operations frame"""

        # Create the calculate button
        self.btn_calculate = QPushButton("Calculate")
        self.btn_calculate.clicked.connect(self.calculate_answer)

        # Back to main menu button
        self.btn_back = QPushButton("Back to main Menu")
        self.btn_back.clicked.connect(self.back_to_main_menu)

        # Add widgets to the layout
        self.operations_layout.addWidget(self.btn_calculate)
        self.operations_layout.addWidget(self.btn_back)

    def calculate_answer(self):
        """Functions that starts the calculation process for user input functions"""
        def calc():
            try:
                # Get the input from the function input box
                userfunction = self.function_input_box.text().replace(' ', '')
                self.output_signal.emit("Calculating!")
                gtt_thinker = GTT_Thinker.TruthTableToGates(userfunction)
                answer = gtt_thinker.get_AnswerFunction()
                # Update the output text box with the answer
                self.output_signal.emit(answer)
            except Exception as e:
                self.output_signal.emit(f"An error has occurred: {e}")

        threading.Thread(target=calc).start()

    def back_to_main_menu(self):
        """Go back to main menu"""
        self.main_menu_ref.show()
        self.close()

    @QtCore.pyqtSlot(str)
    def write_output_tb(self, string: str):
        """This function writes to the output box."""
        self.output_text_box.setPlainText(string)

class MainMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setGeometry(300, 200, 300, 200)

        self.btn_close = QPushButton("Close", self)
        self.btn_close.clicked.connect(self.close_application)
        self.btn_close.setGeometry(100, 80, 100, 30)
        self.hide()
        self.init_gtt_gui()

    def init_ui(self):
        self.show()

    def close_application(self):
        """Exit the application"""
        sys.exit()

    def init_gtt_gui(self):
        """Initialize the GTT GUI"""
        self.gtt_gui = GTTGui(self)
        self.gtt_gui.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())