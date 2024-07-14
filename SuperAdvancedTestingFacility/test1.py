import tkinter as tk
from tkinter import simpledialog, ttk

class ButtonApp(tk.Tk):
    def __init__(self, total_buttons, initial_rows_per_page, initial_widgets_per_row):
        super().__init__()

        self.title("Dynamic Button Pager")
        self.geometry("800x600")  # Fixed size window
        
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
        self.scrollbar_x = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.scrollbar_y = tk.Scrollbar(self, orient=tk.VERTICAL)

        self.canvas = tk.Canvas(self, xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_x.config(command=self.canvas.xview)
        self.scrollbar_y.config(command=self.canvas.yview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.frame = tk.Frame(self.canvas)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.frame_controls = tk.Frame(self)
        self.frame_controls.pack(side=tk.TOP, pady=10)

        tk.Label(self.frame_controls, text="Rows per page:").pack(side=tk.LEFT)
        self.entry_rows_per_page = tk.Entry(self.frame_controls, width=5)
        self.entry_rows_per_page.insert(0, str(self.rows_per_page))
        self.entry_rows_per_page.pack(side=tk.LEFT, padx=5)

        tk.Label(self.frame_controls, text="Widgets per row:").pack(side=tk.LEFT)
        self.entry_widgets_per_row = tk.Entry(self.frame_controls, width=5)
        self.entry_widgets_per_row.insert(0, str(self.widgets_per_row))
        self.entry_widgets_per_row.pack(side=tk.LEFT, padx=5)

        self.redraw_button = tk.Button(self.frame_controls, text="Redraw", command=self.redraw)
        self.redraw_button.pack(side=tk.LEFT, padx=5)

        self.page_info = tk.Label(self, text=f"Page {self.current_page} of {self.total_pages}")
        self.page_info.pack(side=tk.TOP, pady=10)

        self.navigation_frame = tk.Frame(self)
        self.navigation_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.prev_button = tk.Button(self.navigation_frame, text="<< Previous", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.navigation_frame, text="Next >>", command=self.next_page)
        self.next_button.pack(side=tk.RIGHT)

        self.show_page(self.current_page)

        self.frame.bind("<Configure>", self.on_frame_configure)

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
            button = tk.Button(self.frame, text=str(i + 1))
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

if __name__ == "__main__":
    total_buttons = 5000
    initial_rows_per_page = 5
    initial_widgets_per_row = 6
    app = ButtonApp(total_buttons, initial_rows_per_page, initial_widgets_per_row)
    app.mainloop()