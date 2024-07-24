# LogicThursday

LogicThursday is a logic simulator developed by a novice programmer. It provides a graphical user interface for working with truth tables and logic gates.

## Features

- **TruthTable to Gates**: Convert truth tables to logical gate representations.
- **Gates to TruthTable**: Generate truth tables from logical gate configurations.
- **Interactive GUI**: User-friendly interface for easy manipulation of truth tables and gates.
- **Dark Mode**: Utilizes the Sun Valley theme for a sleek, dark interface.

## Components

The project consists of several Python files:

1. `GUI_GTT_TTG_MAIN.py`: The main entry point of the application, containing the `MainMenu` class.
2. `TTG_gui.py`: GUI for the TruthTable to Gates functionality.
3. `GTT_gui.py`: GUI for the Gates to TruthTable functionality.
4. `Info_gui.py`: Information panel GUI.

## Dependencies

- Python 3.x
- tkinter
- sv_ttk (Sun Valley theme for ttk)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/regtoga/LogicThursday.git
   ```
2. Install the required dependencies:
   ```
   pip install sv-ttk
   ```

## Usage

Run the main script to start the application:

```
GUI_GTT_TTG_MAIN.py
```

From the main menu, you can access the following features:
- TruthTable to Gates
- Gates to TruthTable
- Information panel

## Contributing

As this is a project by a novice programmer, contributions, suggestions, and feedback are welcome. Please feel free to open issues or submit pull requests.

## Acknowledgements

- Sun Valley theme for ttk
- [Any other libraries or resources you've used]