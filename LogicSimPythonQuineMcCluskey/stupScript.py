import sys
from cx_Freeze import setup, Executable

# base=”Win32GUI” should only be used with the Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

# Dependencies are automatically detected, but may need to be adjusted.
build_exe_options = {
    "excludes": ["unittest"],
    "zip_include_packages": ["encodings", "PySide6"],
}

setup(
    name = "LogicThursdayV1.7",
    version = "1.7",
    description = "AidanNewberry's Basic Logic Simulation Platform",
    options={"build_exe": build_exe_options},
    executables = [Executable("GUI_GTT_TTG_MAIN.py", base=base)]
)