import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton, QTextEdit, QScrollArea, QLabel

class InfoGui(QDialog):
    def __init__(self, main_menu_ref, position=(100, 100)):
        super().__init__(main_menu_ref)

        # Reference to hide/show main menu
        self.main_menu_ref = main_menu_ref
        self.main_menu_ref.hide()

        # Set window size and title
        self.resize(1050, 600)
        self.setWindowTitle('GTT')
        self.setFixedSize(1050, 600)

        # Set up the layout
        self.main_layout = QHBoxLayout()

        # Creating Frames for Information and Operations
        self.create_frames()

        # Create Widgets inside Frames
        self.create_info_widgets()
        self.create_operations_widgets()

        self.setLayout(self.main_layout)

    def create_frames(self):
        """Creates the frames for the PyQt InfoGui program"""

        # infoFrame will hold all the information about the program
        self.entry_frame = QGroupBox("About this program")
        self.entry_frame_layout = QVBoxLayout()
        self.entry_frame.setLayout(self.entry_frame_layout)

        # operationsFrame holds the buttons for the program
        self.operations_frame = QGroupBox("Operations")
        self.operations_layout = QVBoxLayout()
        self.operations_frame.setLayout(self.operations_layout)

        # Add frames to the main layout
        self.main_layout.addWidget(self.entry_frame)
        self.main_layout.addWidget(self.operations_frame)

    def create_info_widgets(self):
        """Function creates all widgets related to info frame"""

        # Create the Text widget for showing information
        self.textbox = QTextEdit()
        self.textbox.setReadOnly(True)

        # Adding widgets to the layout
        self.entry_frame_layout.addWidget(self.textbox)

        # Load the content of info.txt into the Text widget
        try:
            script_dir = os.path.dirname(__file__)
            file_path = os.path.join(script_dir, 'info.txt')
            with open(file_path, 'r') as file:
                content = file.read()
                self.textbox.setPlainText(content)
        except FileNotFoundError:
            self.textbox.setPlainText("info.txt file not found.")

    def create_operations_widgets(self):
        """Function creates all widgets related to Operations frame"""

        # Create the back button
        self.btn_back = QPushButton("Back to main Menu")
        self.btn_back.clicked.connect(self.back_to_main_menu)

        # Add the button to the layout
        self.operations_layout.addWidget(self.btn_back)

    def back_to_main_menu(self):
        """Go back to main menu"""
        self.main_menu_ref.show()
        self.close()

class MainMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setGeometry(300, 200, 300, 200)

        self.btn_close = QPushButton("Close", self)
        self.btn_close.clicked.connect(self.close_application)
        self.btn_close.setGeometry(100, 80, 100, 30)
        self.hide()
        self.init_info_gui()

    def init_ui(self):
        self.show()

    def close_application(self):
        """Exit the application"""
        sys.exit()

    def init_info_gui(self):
        """Initialize the Info GUI"""
        self.info_gui = InfoGui(self)
        self.info_gui.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_menu = MainMenu()
    sys.exit(app.exec_())