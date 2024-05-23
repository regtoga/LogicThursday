import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget

import GUIsForMainGUI.TTG_gui as TTG_gui
import GUIsForMainGUI.GTT_gui as GTT_gui
import GUIsForMainGUI.Info_gui as Info_gui

import qdarkstyle

class MainMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 1050, 600)  # Adjust the size according to your needs
        self.setFixedSize(1050, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        self.layout = QVBoxLayout(central_widget)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.setSpacing(20)  # Increase spacing for better visual separation

        # Create buttons for the main menu
        self.buttons = []
        btn_names = ["TruthTable to Gates", "Gates to TruthTable", "Info", "Close"]
        for name in btn_names:
            button = QPushButton(name, self)
            if name == "Close":
                button.clicked.connect(self.close_gui)
            else:
                # Dynamically connect each button to the appropriate method
                button.clicked.connect(getattr(self, f"open_{name.replace(' ', '_').lower()}"))
            self.buttons.append(button)
            self.layout.addWidget(button)
        
        self.init_ui()

        # Apply dark theme
        self.apply_theme()

    def init_ui(self):
        self.show()

    def apply_theme(self):
        # Using a custom dark theme for PyQt5, including borders and padding
        #self.setStyleSheet(qdarkstyle.load_stylesheet())
        pass

    def open_truthtable_to_gates(self):
        self.hide()  # Hide the main menu
        self.ttg_gui = TTG_gui.TTGGui(self)
        self.ttg_gui.show()

    def open_gates_to_truthtable(self):
        self.hide()  # Hide the main menu
        self.gtt_gui = GTT_gui.GTTGui(self)
        self.gtt_gui.show()

    def open_info(self):
        self.hide()  # Hide the main menu
        self.info_gui = Info_gui.InfoGui(self)
        self.info_gui.show()

    def close_gui(self):
        sys.exit()  # Exit the program

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_menu = MainMenu()
    sys.exit(app.exec_())