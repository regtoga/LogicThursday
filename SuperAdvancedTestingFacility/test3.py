import tkinter as tk
from tkinter import font

# Function to update text and font size in the main Text widget
def update_text():
    # Get the new font size from the Entry widget in pop-up window
    new_font_size = font_size_entry.get()
    # Get the new text from the Entry widget in pop-up window
    new_text = text_entry.get()
    
    # Check if the input for font size is a digit
    if new_font_size.isdigit():
        main_font.config(size=int(new_font_size))  # Update font size
    
    # Update text in the main text widget
    main_text.delete(1.0, tk.END)
    main_text.insert(tk.END, new_text)
    
    # Close the pop-up window
    popup_window.destroy()

# Function to bring up the pop-up window with options
def show_popup():
    global popup_window, font_size_entry, text_entry
    
    # Create pop-up window
    popup_window = tk.Toplevel(root)
    popup_window.geometry("300x200")
    popup_window.title("Options")
    
    # Label and Entry for changing font size
    font_size_label = tk.Label(popup_window, text="Font Size:")
    font_size_label.pack(pady=5)
    font_size_entry = tk.Entry(popup_window)
    font_size_entry.pack(pady=5)
    
    # Label and Entry for changing text
    text_label = tk.Label(popup_window, text="New Text:")
    text_label.pack(pady=5)
    text_entry = tk.Entry(popup_window)
    text_entry.pack(pady=5)
    
    # Submit button to apply changes
    submit_button = tk.Button(popup_window, text="Submit", command=update_text)
    submit_button.pack(pady=10)

# Create main window
root = tk.Tk()
root.geometry("500x300")
root.title("Main Window")

# Default font settings
main_font = font.Font(family="Helvetica", size=12)

# Frame to organize the text box and button horizontally
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Text widget in main window with starter text
main_text = tk.Text(main_frame, font=main_font, height=10, width=50)
main_text.insert(tk.END, "This is some starter text.")
main_text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# Button to open pop-up window placed next to the text box
popup_button = tk.Button(main_frame, text="Options", command=show_popup)
popup_button.pack(side=tk.LEFT, padx=10, pady=10)

# Run the application
root.mainloop()