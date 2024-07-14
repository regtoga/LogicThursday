import tkinter as tk
from tkinter import ttk
import sv_ttk

class ButtonApp(tk.Tk):
    def __init__(self, total_buttons, initial_rows_per_page, initial_widgets_per_row):
        super().__init__()

        self.title("Dynamic Button Pager")
        self.geometry("1000x600")  # Fixed size window

        # Apply sv_ttk dark theme
        sv_ttk.set_theme("dark")
        
        self.total_buttons = total_buttons
        self.rows_per_page = initial_rows_per_page
        self.widgets_per_row = initial_widgets_per_row
        self.widgets_per_page = self.rows_per_page * self.widgets_per_row
        self.total_pages = (self.total_buttons // self.widgets_per_page) + (1 if self.total_buttons % self.widgets_per_page != 0 else 0)
        
        self.current_page = 1
        
        self.create_widgets()
        
        # Update pages when widgets per page or per row changes
        self.update_pages()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        self.scrollbar_y = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky='ns')
        
        # Move the scrollbar above the input and navigation buttons
        self.scrollbar_x = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_x.grid(row=1, column=0, sticky='ew')

        self.canvas.configure(xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)

        self.frame = ttk.Frame(self.canvas)
        self.frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

        self.input_navigation_frame = ttk.Frame(self.canvas_frame)
        self.input_navigation_frame.grid(row=2, column=0, pady=(5, 0), sticky='ew')

        self.input_subframe = ttk.Frame(self.input_navigation_frame)
        self.input_subframe.pack()

        ttk.Label(self.input_subframe, text="Rows per page:").pack(side=tk.LEFT)
        self.entry_rows_per_page = ttk.Entry(self.input_subframe, width=5)
        self.entry_rows_per_page.insert(0, str(self.rows_per_page))
        self.entry_rows_per_page.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.input_subframe, text="Widgets per row:").pack(side=tk.LEFT)
        self.entry_widgets_per_row = ttk.Entry(self.input_subframe, width=5)
        self.entry_widgets_per_row.insert(0, str(self.widgets_per_row))
        self.entry_widgets_per_row.pack(side=tk.LEFT, padx=5)

        self.redraw_button = ttk.Button(self.input_subframe, text="Redraw", command=self.redraw)
        self.redraw_button.pack(side=tk.LEFT, padx=5)

        self.navigation_subframe = ttk.Frame(self.input_navigation_frame)
        self.navigation_subframe.pack()

        # Navigation Buttons and Page Info
        self.prev_button = ttk.Button(self.navigation_subframe, text="<< Previous", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT)

        self.page_info = ttk.Label(self.navigation_subframe, text=f"Page {self.current_page} of {self.total_pages}")
        self.page_info.pack(side=tk.LEFT, padx=10)

        self.next_button = ttk.Button(self.navigation_subframe, text="Next >>", command=self.next_page)
        self.next_button.pack(side=tk.LEFT)

        self.goto_entry = ttk.Entry(self.navigation_subframe, width=5)
        self.goto_entry.pack(side=tk.LEFT, padx=5)

        self.goto_button = ttk.Button(self.navigation_subframe, text="Go to Page", command=self.goto_page)
        self.goto_button.pack(side=tk.LEFT, padx=5)
        
        self.show_page(self.current_page)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def show_page(self, page_number):
        for widget in self.frame.winfo_children():
            widget.destroy()

        start_idx = (page_number - 1) * self.widgets_per_page
        end_idx = min(start_idx + self.widgets_per_page, self.total_buttons)

        current_row = 0
        current_col = 0

        for i in range(start_idx, end_idx):
            button = ttk.Button(self.frame, text=str(i + 1))
            button.grid(row=current_row, column=current_col, padx=5, pady=5)

            current_col += 1
            if current_col >= self.widgets_per_row:
                current_col = 0
                current_row += 1
        
        self.page_info.config(text=f"Page {self.current_page} of {self.total_pages}")

    def update_pages(self):
        self.widgets_per_page = self.rows_per_page * self.widgets_per_row
        self.total_pages = (self.total_buttons // self.widgets_per_page) + (1 if self.total_buttons % self.widgets_per_page != 0 else 0)
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages
        self.show_page(self.current_page)

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.show_page(self.current_page)
        
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.show_page(self.current_page)

    def redraw(self):
        try:
            rows_per_page = int(self.entry_rows_per_page.get())
            widgets_per_row = int(self.entry_widgets_per_row.get())

            self.rows_per_page = rows_per_page
            self.widgets_per_row = widgets_per_row
            self.update_pages()
        except ValueError:
            pass  # Handle invalid input gracefully

    def goto_page(self):
        try:
            page = int(self.goto_entry.get())
            if 1 <= page <= self.total_pages:
                self.current_page = page
                self.show_page(page)
        except ValueError:
            pass  # Handle invalid input gracefully

if __name__ == "__main__":
    total_buttons = 5000
    initial_rows_per_page = 8
    initial_widgets_per_row = 8
    app = ButtonApp(total_buttons, initial_rows_per_page, initial_widgets_per_row)
    app.mainloop()