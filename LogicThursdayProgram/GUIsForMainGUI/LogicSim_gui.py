import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import pickle
import os
import threading
import math

import Thinkers.GatesToTableThinker as GTT_Thinker
import Thinkers.TruthTableToGatesThinker as TTG_Thinker

CHIP_DIR = "chips/"

if not os.path.exists(CHIP_DIR):
    os.makedirs(CHIP_DIR)

class Gate:
    def __init__(self, name, inputs, outputs, boolean_exprs):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.boolean_exprs = boolean_exprs

    def evaluate(self, input_state):
        results = []
        for expr in self.boolean_exprs:
            try:
                output = GTT_Thinker.calculateFunctionOutput(expr.replace(" ", ""), input_state)
                results.append(output)
            except Exception as e:
                print(f"Error evaluating function: {e}")
                results.append(False)
        return tuple(results)

class LogicSim_gui(tk.Toplevel):
    def __init__(self, main_menu_ref, position="+100+100"):
        super().__init__(main_menu_ref)
        self.main_menu_ref = main_menu_ref
        self.title("Logic Circuit Designer")
        self.geometry(position)
        self.geometry("1055x600")
        
        self.gate_definitions = {
            "AND": (2, 1, ["AB"]),
            "OR": (2, 1, ["A+B"]),
            "NOT": (1, 1, ["A'"])
        }
        
        self.gates = {name: Gate(name, *details) for name, details in self.gate_definitions.items()}
        self.workspace_objects = {}
        self.connections = {}
        self.states = {}

        self.preview_item = None
        self.dragged_gate = None
        self.selected_node = None
        self.moving_gate = None
        self.move_start = None

        self.create_frames()
        self.load_custom_gates()

    def create_frames(self):
        self.operations_frame = tk.Frame(self, width=200)
        self.operations_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.workspace_frame = tk.Frame(self, bg='white')
        self.workspace_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.workspace_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Button-3>", self.cancel_action)

        self.create_buttons()

    def create_buttons(self):
        self.buttons_frame = tk.Frame(self.operations_frame)
        self.buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.add_input_button = tk.Button(self.buttons_frame, text="Add Input", command=self.add_input)
        self.add_input_button.pack(fill=tk.X, pady=2)

        self.add_output_button = tk.Button(self.buttons_frame, text="Add Output", command=self.add_output)
        self.add_output_button.pack(fill=tk.X, pady=2)

        self.save_circuit_button = tk.Button(self.buttons_frame, text="Save Circuit as Gate", command=self.save_circuit_as_gate)
        self.save_circuit_button.pack(fill=tk.X, pady=2)

        self.clear_board_button = tk.Button(self.buttons_frame, text="Clear Board", command=self.clear_board)
        self.clear_board_button.pack(fill=tk.X, pady=2)

        self.clear_board_button = tk.Button(self.buttons_frame, text="Import Chip", command=self.import_custom_gates)
        self.clear_board_button.pack(fill=tk.X, pady=2)

        self.back_button = tk.Button(self.buttons_frame, text="Back to Menu", command=self.back_to_main_menu)
        self.back_button.pack(fill=tk.X, pady=2)

        self.populate_operations()

    def populate_operations(self):
        for widget in self.operations_frame.winfo_children():
            if isinstance(widget, tk.Button) and widget not in self.buttons_frame.winfo_children():
                widget.destroy()

        for gate_name in self.gates:
            button = tk.Button(self.operations_frame, text=gate_name)
            button.bind("<Button-1>", self.start_drag)
            if gate_name not in self.gate_definitions:  # Custom gates
                button.bind("<Button-3>", self.delete_gate_file)
            button.pack(pady=2)

    def start_drag(self, event):
        widget = event.widget
        gate = widget.cget("text")
        self.dragged_gate = self.gates[gate]
        self.canvas.bind("<Motion>", self.update_preview)

    def update_preview(self, event):
        if self.preview_item:
            self.canvas.delete(self.preview_item)
        x, y = event.x, event.y
        self.preview_item = self.canvas.create_rectangle(x, y, x+80, y+40, dash=(5, 2), outline="gray")

    def on_canvas_click(self, event):
        item = self.canvas.find_withtag('current')
        if self.dragged_gate:
            self.place_gate(event.x, event.y)
        elif item:
            if 'gate' in self.canvas.gettags(item):
                self.select_gate(item[0])

    def place_gate(self, x, y):
        gate_obj = self.canvas.create_rectangle(x, y, x+80, y+40, fill="lightblue", tag="gate")
        text_obj = self.canvas.create_text(x+40, y+20, text=self.dragged_gate.name, tags=("text",))

        self.workspace_objects[gate_obj] = {'gate': self.dragged_gate, 'nodes': [], 'text': text_obj}

        for i in range(self.dragged_gate.inputs):
            input_node = self.canvas.create_oval(x-5, y+10*i+10, x+5, y+10*i+20, fill="black", tags=("node", "gate_input"))
            self.workspace_objects[gate_obj]['nodes'].append(input_node)
            self.workspace_objects[input_node] = {'parent': gate_obj, 'type': 'gate_input'}
            self.canvas.tag_bind(input_node, "<Button-1>", self.select_node)

        for i in range(self.dragged_gate.outputs):
            output_node = self.canvas.create_oval(x+75, y+10*i+10, x+85, y+10*i+20, fill="black", tags=("node", "gate_output"))
            self.workspace_objects[gate_obj]['nodes'].append(output_node)
            self.workspace_objects[output_node] = {'parent': gate_obj, 'type': 'gate_output'}
            self.canvas.tag_bind(output_node, "<Button-1>", self.select_node)

        self.dragged_gate = None
        self.canvas.delete(self.preview_item)
        self.canvas.unbind("<Motion>")

        self.canvas.tag_bind(gate_obj, "<Button-3>", self.prompt_delete_gate)

    def select_gate(self, gate_id):
        if gate_id in self.workspace_objects and 'gate' in self.workspace_objects[gate_id]:
            self.moving_gate = gate_id
            self.invert_gate_colors(gate_id)
            self.move_start = self.canvas.coords(gate_id)[:2]
            self.canvas.bind("<B1-Motion>", self.move_gate)
            self.canvas.bind("<ButtonRelease-1>", self.end_move_gate)

    def prompt_delete_gate(self, event):
        gate_id = self.canvas.find_withtag('current')[0]
        result = messagebox.askyesno("Delete Confirmation", "Do you want to delete this gate?", parent=self.canvas)
        if result:
            self.delete_gate(gate_id)

    def delete_gate(self, gate_id):
        connections_to_delete = [(start, end) for start, end in self.connections if start in self.workspace_objects[gate_id]['nodes'] or end in self.workspace_objects[gate_id]['nodes']]

        for conn in connections_to_delete:
            line = self.connections[conn]
            self.canvas.delete(line)
            del self.connections[conn]

        for node in self.workspace_objects[gate_id]['nodes']:
            self.canvas.delete(node)
            del self.workspace_objects[node]

        text = self.workspace_objects[gate_id]['text']
        self.canvas.delete(text)

        self.canvas.delete(gate_id)
        del self.workspace_objects[gate_id]

    def move_gate(self, event):
        if self.moving_gate and self.move_start:
            dx = event.x - self.move_start[0]
            dy = event.y - self.move_start[1]
            self.canvas.move(self.moving_gate, dx, dy)

            for node in self.workspace_objects[self.moving_gate]['nodes']:
                self.canvas.move(node, dx, dy)
                for connection, line in self.connections.items():
                    if node in connection:
                        self.update_line(connection, line)

            text = self.workspace_objects[self.moving_gate]['text']
            self.canvas.move(text, dx, dy)
            self.move_start = (event.x, event.y)

    def update_line(self, nodes, line):
        start_node, end_node = nodes
        start_coords = self.canvas.coords(start_node)
        end_coords = self.canvas.coords(end_node)
        color = "red" if self.states.get(start_node, False) else "grey"
        self.canvas.itemconfig(line, fill=color)
        self.canvas.coords(line, start_coords[0]+5, start_coords[1]+5, end_coords[0]+5, end_coords[1]+5)

    def end_move_gate(self, event):
        if self.moving_gate:
            self.invert_gate_colors(self.moving_gate)
        self.moving_gate = None
        self.move_start = None
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def select_node(self, event):
        node_id = self.canvas.find_withtag('current')[0]
        node_tags = self.canvas.gettags(node_id)

        if self.selected_node:
            selected_node_tags = self.canvas.gettags(self.selected_node)
            if (('workspace_input' in selected_node_tags and 'gate_input' in node_tags) or
                ('gate_output' in selected_node_tags and 'workspace_output' in node_tags) or
                ('gate_output' in selected_node_tags and 'gate_input' in node_tags)):
                self.connect_nodes(self.selected_node, node_id)

            self.canvas.itemconfig(self.selected_node, fill="black")
            self.selected_node = None
        else:
            self.selected_node = node_id
            self.canvas.itemconfig(node_id, fill="blue")

    def connect_nodes(self, start_node, end_node):
        if (start_node, end_node) in self.connections or start_node == end_node:
            return

        start_coords = self.canvas.coords(start_node)
        end_coords = self.canvas.coords(end_node)
        line = self.canvas.create_line(start_coords[0]+5, start_coords[1]+5, end_coords[0]+5, end_coords[1]+5, width=6, tags="wire")
        self.connections[(start_node, end_node)] = line
        self.canvas.tag_bind(line, "<Button-3>", self.delete_wire)
        self.simulate_circuit()

    def delete_wire(self, event):
        line_id = self.canvas.find_withtag('current')[0]
        for conn, line in list(self.connections.items()):
            if line == line_id:
                del self.connections[conn]
                break
        self.canvas.delete(line_id)

    def delete_workspace_element(self, element_id):
        if element_id in self.workspace_objects:
            element = self.workspace_objects[element_id]
            if 'type' in element and element['type'] in ['workspace_input', 'workspace_output']:
                if element['type'] == 'workspace_input':
                    toggle_button = element.get('toggle')
                    if toggle_button:
                        self.canvas.delete(toggle_button)
                if element['type'] == 'workspace_output':
                    indicator = element.get('indicator')
                    if indicator:
                        self.canvas.delete(indicator)
                self.canvas.delete(element_id)
                del self.workspace_objects[element_id]

    def invert_gate_colors(self, gate_id):
        current_fill = self.canvas.itemcget(gate_id, "fill")
        inverted_fill = "blue" if current_fill == "lightblue" else "lightblue"
        self.canvas.itemconfig(gate_id, fill=inverted_fill)

    def save_circuit_as_gate(self):
        name = simpledialog.askstring("New Gate", "Enter the name for the new gate (max 14 characters):")
        if not name or len(name) > 14:
            messagebox.showerror("Error", "Invalid gate name. Must be 1-14 characters.")
            return

        input_nodes = [obj for obj, details in self.workspace_objects.items() if details.get('type') == 'workspace_input']
        output_nodes = [obj for obj, details in self.workspace_objects.items() if details.get('type') == 'workspace_output']

        num_inputs = len(input_nodes)
        num_outputs = len(output_nodes)

        truth_table = {}
        functions = []

        for out_idx in range(num_outputs):
            minterms = []

            for i in range(2 ** num_inputs):
                input_state = [(i >> bit) & 1 for bit in range(num_inputs)]
                for idx, node in enumerate(input_nodes):
                    self.states[node] = input_state[idx] == 1

                self.simulate_circuit()

                output_state = self.states.get(output_nodes[out_idx], False)
                truth_table[tuple(input_state)] = output_state

                if output_state:
                    minterm = ''.join([f"{chr(65 + idx)}" if val else f"{chr(65 + idx)}'" for idx, val in enumerate(input_state)])
                    if minterm:
                        minterms.append(minterm)

            minimized_function = ' + '.join(minterms)
            functions.append(minimized_function)

        self.gates[name] = Gate(name, num_inputs, num_outputs, boolean_exprs=functions)

        with open(os.path.join(CHIP_DIR, f"{name}.pkl"), 'wb') as f:
            pickle.dump((num_inputs, num_outputs, functions), f)

        self.clear_board()
        self.populate_operations()

    def simulate_circuit(self):
        change_flag = True
        while change_flag:
            change_flag = False
            for gate_obj, details in self.workspace_objects.items():
                if 'gate' not in details:
                    continue

                gate = details['gate']
                input_nodes = [n for n in details['nodes'] if 'gate_input' in self.canvas.gettags(n)]
                output_nodes = [n for n in details['nodes'] if 'gate_output' in self.canvas.gettags(n)]

                inputs = tuple(self.states.get(node, False) for node in input_nodes)
                result = gate.evaluate(inputs)

                for idx, output_node in enumerate(output_nodes):
                    if idx < len(result) and self.states.get(output_node) != result[idx]:
                        self.states[output_node] = result[idx]
                        change_flag = True

            for (start_node, end_node), line in self.connections.items():
                state = self.states.get(start_node, False)
                self.canvas.itemconfig(line, fill="red" if state else "grey")
                if self.states.get(end_node) != state:
                    self.states[end_node] = state
                    change_flag = True

            for obj, details in self.workspace_objects.items():
                if details.get('type') == 'workspace_output':
                    connected_nodes = [start for (start, end) in self.connections if end == obj]
                    indicator_color = "red" if any(self.states.get(node, False) for node in connected_nodes) else "grey"
                    self.canvas.itemconfig(details['indicator'], fill=indicator_color)

    def add_input(self):
        coords = (5, 10 + len([w for w in self.workspace_objects.values() if w.get('type') == 'workspace_input']) * 30)
        toggle_button = self.canvas.create_oval(*coords, coords[0]+20, coords[1]+20, fill="grey", tag="toggle_button")
        connect_node = self.canvas.create_oval(coords[0]+25, coords[1]+5, coords[0]+35, coords[1]+15, fill="black", tags=("node", "workspace_input"))

        self.workspace_objects[connect_node] = {'type': 'workspace_input', 'toggle': toggle_button}
        self.states[connect_node] = False

        self.canvas.tag_bind(toggle_button, "<Button-1>", lambda event, toggle=connect_node: self.toggle_input(toggle))
        self.canvas.tag_bind(connect_node, "<Button-1>", self.select_node)
        self.canvas.tag_bind(connect_node, "<Button-3>", lambda event, element=connect_node: self.delete_workspace_element(element))

    def add_output(self):
        coords = (self.canvas.winfo_width() - 50, 10 + len([w for w in self.workspace_objects.values() if w.get('type') == 'workspace_output']) * 30)
        connect_node = self.canvas.create_oval(coords[0], coords[1]+5, coords[0]+10, coords[1]+15, fill="black", tags=("node", "workspace_output"))
        indicator = self.canvas.create_oval(coords[0]+15, coords[1], coords[0]+35, coords[1]+20, fill="grey", tag="output_indicator")

        self.workspace_objects[connect_node] = {'type': 'workspace_output', 'indicator': indicator}

        self.canvas.tag_bind(connect_node, "<Button-1>", self.select_node)
        self.canvas.tag_bind(connect_node, "<Button-3>", lambda event, element=connect_node: self.delete_workspace_element(element))

    def toggle_input(self, toggle):
        self.states[toggle] = not self.states.get(toggle, False)
        self.canvas.itemconfig(self.workspace_objects[toggle]['toggle'], fill="red" if self.states[toggle] else "grey")
        self.simulate_circuit()

    def clear_board(self):
        self.canvas.delete("all")
        self.workspace_objects.clear()
        self.connections.clear()
        self.states.clear()

    def cancel_action(self, event):
        if self.selected_node:
            self.canvas.itemconfig(self.selected_node, fill="black")
            self.selected_node = None

        if self.preview_item:
            self.canvas.delete(self.preview_item)

        if self.moving_gate:
            self.invert_gate_colors(self.moving_gate)
            self.moving_gate = None
            self.move_start = None
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")

    def back_to_main_menu(self):
        """Return to the main menu"""
        self.main_menu_ref.deiconify()
        self.destroy()

    def delete_gate_file(self, event):
        """Delete gate file via right-click on custom gate button."""
        button = event.widget
        gate_name = button.cget("text")
        should_delete = messagebox.askyesno("Delete Gate", f"Are you sure you want to delete the gate '{gate_name}'?")
        if should_delete:
            # Remove the gate from the internal dictionary
            if gate_name in self.gates:
                del self.gates[gate_name]
            
            # Delete the associated file
            filepath = os.path.join(CHIP_DIR, f"{gate_name}.pkl")
            if os.path.exists(filepath):
                os.remove(filepath)
                
            # Refresh the gate buttons on UI
            self.populate_operations()

    def import_custom_gates(self):
        def calc():
            root = tk.Tk()
            root.withdraw()

            file_path = filedialog.askopenfilename(
                initialdir="/",
                title="Select a File",
                filetypes=(("Pickle Files", "*.pkl*"), ("all files", "*.*"))
            )

            if file_path:
                try:
                    with open(file_path, "rb") as file:
                        TableFromStorage = pickle.load(file)

                    # Load and unpack all expressions for the custom gate
                    name_without_ext = os.path.basename(file_path).replace(".pkl", "")

                    if len(TableFromStorage) == 3:
                        num_inputs = TableFromStorage[0]
                        num_outputs = TableFromStorage[1]
                        function_exprs = TableFromStorage[2]
                        
                        
                    else:
                        name_without_ext = os.path.basename(file_path).replace(".pkl", "")
                        num_inputs = int(math.log(len(TableFromStorage), 2))
                        num_outputs = len(TableFromStorage[0])
                        function_exprs = []
                        for depth in range(0, len(TableFromStorage[0])):
                            stuff = []
                            for item in TableFromStorage:
                                stuff.append(item[depth])

                            stuff2 = "Z'm("
                            for minterm in range(0, len(stuff)):
                                if stuff[minterm] == "1":
                                    stuff2 += (f"{minterm},")

                            #remove the last comma
                            stuff2 = stuff2[:-1]
                            stuff2 += ")"

                            #print(stuff2)

                            ttg_thinker = TTG_Thinker.TruthTableToGates(stuff2, f"importpt{depth}")
                            ttg_thinker.calculateanswer()
                            #append result to the answer bit
                            function_exprs.append(ttg_thinker.get_Answer().replace("F = ", ""))
                            del ttg_thinker
                            os.remove(f"importpt{depth}")
                            

                    self.gates[name_without_ext] = Gate(name_without_ext, num_inputs, num_outputs, boolean_exprs=function_exprs)

                    #look into this one cheef...

                    with open(os.path.join(CHIP_DIR, f"{name_without_ext}.pkl"), 'wb') as f:
                        pickle.dump((num_inputs, num_outputs, function_exprs), f)

                    self.populate_operations()


                except:
                    messagebox.showerror("Error", "Something went wrong when loading the file!")
                    del TableFromStorage  # Clear the variable
        
        #Create the worker thread
        threading.Thread(target=calc).start()
        
    def load_custom_gates(self):
        """Load custom gates from the CHIP_DIR."""
        files = os.listdir(CHIP_DIR)
        for filename in files:
            if filename.endswith('.pkl'):
                filepath = os.path.join(CHIP_DIR, filename)
                with open(filepath, 'rb') as f:
                    try:
                        # Load and unpack all expressions for the custom gate
                        num_inputs, num_outputs, function_exprs = pickle.load(f)
                        name_without_ext = os.path.splitext(filename)[0]
                        self.gates[name_without_ext] = Gate(name_without_ext, num_inputs, num_outputs, boolean_exprs=function_exprs)
                    except Exception as e:
                        print(f"Failed to load gate from {filename}: {e}")

        self.populate_operations()

if __name__ == '__main__':
    class MainMenu(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Main Menu")
            self.geometry("300x200")

            self.withdraw()  # Hide the main menu on startup

            open_design_button = tk.Button(self, text="Open Circuit Designer", command=self.open_designer)
            open_design_button.pack(pady=10)

        def open_designer(self):
            self.withdraw()  # Hide the main menu
            designer = LogicSim_gui(self, position="+100+100")
            designer.mainloop()

    # Instantiate MainMenu for standalone execution
    app = MainMenu()
    app.mainloop()