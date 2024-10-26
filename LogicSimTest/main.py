import tkinter as tk
from tkinter import simpledialog, messagebox

class Gate:
    def __init__(self, name, inputs, outputs, truth_table=None):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.truth_table = truth_table

    def evaluate(self, input_state):
        return self.truth_table.get(input_state, (False,))

class LogicCircuitDesigner(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Logic Circuit Designer")
        self.geometry("1200x800")

        self.gates = {
            'AND': Gate('AND', 2, 1),
            'OR': Gate('OR', 2, 1),
            'NOT': Gate('NOT', 1, 1),
        }

        self.operations_frame = tk.Frame(self, bg='lightgray', width=200)
        self.operations_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.workspace_frame = tk.Frame(self, bg='white')
        self.workspace_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.workspace_objects = {}
        self.connections = {}
        self.states = {}

        self.canvas = tk.Canvas(self.workspace_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Button-3>", self.cancel_action)

        self.operations_frame_gates = tk.Frame(self.operations_frame, bg='lightgray')
        self.operations_frame_gates.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.operations_frame_buttons = tk.Frame(self.operations_frame, bg='lightgray')
        self.operations_frame_buttons.pack(side=tk.BOTTOM, fill=tk.X)

        self.add_input_button = tk.Button(self.operations_frame_buttons, text="Add Input", command=self.add_input)
        self.add_input_button.pack(pady=5)

        self.add_output_button = tk.Button(self.operations_frame_buttons, text="Add Output", command=self.add_output)
        self.add_output_button.pack(pady=5)

        self.save_circuit_button = tk.Button(self.operations_frame_buttons, text="Save Circuit as Gate", command=self.save_circuit_as_gate)
        self.save_circuit_button.pack(pady=5)

        self.clear_board_button = tk.Button(self.operations_frame_buttons, text="Clear Board", command=self.clear_board)
        self.clear_board_button.pack(pady=5)

        self.populate_operations()

        self.dragged_gate = None
        self.selected_node = None
        self.preview_item = None
        self.moving_gate = None
        self.move_start = None

        self.simulation_running = False

    def populate_operations(self):
        for widget in self.operations_frame_gates.winfo_children():
            widget.destroy()

        for gate_name in self.gates:
            button = tk.Button(self.operations_frame_gates, text=gate_name)
            button.bind("<Button-1>", self.start_drag)
            button.pack(pady=5)

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
        if item and item[0] in self.workspace_objects and 'node' not in self.canvas.gettags(item[0]) and 'wire' not in self.canvas.gettags(item[0]):
            self.select_gate(item[0])
        elif self.dragged_gate:
            self.place_gate(event.x, event.y)

    def place_gate(self, x, y):
        gate_obj = self.canvas.create_rectangle(x, y, x+80, y+40, fill="lightblue", tag="gate")
        text_obj = self.canvas.create_text(x+40, y+20, text=self.dragged_gate.name)
        self.workspace_objects[gate_obj] = {'gate': self.dragged_gate, 'nodes': [], 'text': text_obj}

        for i in range(self.dragged_gate.inputs):
            input_node = self.canvas.create_oval(x-5, y+10*i+10, x+5, y+10*i+20, fill="black", tags=("node", "gate_input"))
            self.workspace_objects[gate_obj]['nodes'].append(input_node)
            self.workspace_objects[input_node] = {'parent': gate_obj, 'type': 'gate_input'}
            self.canvas.tag_bind(input_node, "<Button-1>", self.select_node)
            self.canvas.tag_bind(input_node, "<Enter>", lambda e, id=input_node: self.on_node_hover(id, True))
            self.canvas.tag_bind(input_node, "<Leave>", lambda e, id=input_node: self.on_node_hover(id, False))

        for i in range(self.dragged_gate.outputs):
            output_node = self.canvas.create_oval(x+75, y+10*i+10, x+85, y+10*i+20, fill="black", tags=("node", "gate_output"))
            self.workspace_objects[gate_obj]['nodes'].append(output_node)
            self.workspace_objects[output_node] = {'parent': gate_obj, 'type': 'gate_output'}
            self.canvas.tag_bind(output_node, "<Button-1>", self.select_node)
            self.canvas.tag_bind(output_node, "<Enter>", lambda e, id=output_node: self.on_node_hover(id, True))
            self.canvas.tag_bind(output_node, "<Leave>", lambda e, id=output_node: self.on_node_hover(id, False))

        self.dragged_gate = None
        self.canvas.delete(self.preview_item)
        self.canvas.unbind("<Motion>")

        self.canvas.tag_bind(gate_obj, "<Button-3>", self.select_gate_right_click)

    def select_gate(self, gate_id):
        self.moving_gate = gate_id
        self.invert_gate_colors(gate_id)
        self.move_start = self.canvas.coords(gate_id)[:2]
        self.canvas.bind("<B1-Motion>", self.move_gate)
        self.canvas.bind("<ButtonRelease-1>", self.end_move_gate)

    def invert_gate_colors(self, gate_id):
        current_fill = self.canvas.itemcget(gate_id, "fill")
        inverted_fill = "blue" if current_fill == "lightblue" else "lightblue"
        self.canvas.itemconfig(gate_id, fill=inverted_fill)

    def select_gate_right_click(self, event):
        gate_id = self.canvas.find_withtag('current')[0]
        result = messagebox.askyesno("Delete Confirmation", "Do you want to delete this gate?", parent=self.canvas)
        if result:
            self.delete_gate(gate_id)

    def move_gate(self, event):
        if self.moving_gate and self.move_start:
            if 'gate' in self.workspace_objects[self.moving_gate]:
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

    def end_move_gate(self, event):
        if self.moving_gate:
            self.invert_gate_colors(self.moving_gate)
        self.moving_gate = None
        self.move_start = None
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def update_line(self, nodes, line):
        start_node, end_node = nodes
        start_coords = self.canvas.coords(start_node)
        end_coords = self.canvas.coords(end_node)
        color = "red" if self.states.get(start_node, False) else "grey"
        self.canvas.itemconfig(line, fill=color)
        self.canvas.coords(line, start_coords[0]+5, start_coords[1]+5, end_coords[0]+5, end_coords[1]+5)

    def delete_gate(self, gate_id):
        connections_to_delete = []
        for ((start, end), line) in self.connections.items():
            if start in self.workspace_objects[gate_id]['nodes'] or end in self.workspace_objects[gate_id]['nodes']:
                connections_to_delete.append((start, end))

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

    def add_input(self):
        starting_y = 10
        next_offset = 40
        x = 5
        y = starting_y + (len([obj for obj in self.workspace_objects.values() if obj.get('type') == 'workspace_input']) * next_offset)

        toggle_button = self.canvas.create_oval(x, y, x+20, y+20, fill="grey", tag="toggle_button")
        connect_node = self.canvas.create_oval(x+25, y+5, x+35, y+15, fill="black", tags=("node", "workspace_input"))
        self.workspace_objects[connect_node] = {'toggle': toggle_button, 'type': 'workspace_input'}
        self.states[connect_node] = False

        self.canvas.tag_bind(toggle_button, "<Button-1>", lambda e, toggle=connect_node: self.toggle_input(toggle))
        self.canvas.tag_bind(connect_node, "<Button-1>", self.select_node)
        self.canvas.tag_bind(connect_node, "<Enter>", lambda e, id=connect_node: self.on_node_hover(id, True))
        self.canvas.tag_bind(connect_node, "<Leave>", lambda e, id=connect_node: self.on_node_hover(id, False))

    def add_output(self):
        starting_y = 10
        next_offset = 40
        x = self.canvas.winfo_width()-35
        y = starting_y + (len([obj for obj in self.workspace_objects.values() if obj.get('type') == 'workspace_output']) * next_offset)

        connect_node = self.canvas.create_oval(x, y+5, x+10, y+15, fill="black", tag=("node", "workspace_output"))
        output_indicator = self.canvas.create_oval(x+15, y, x+35, y+20, fill="grey", tag="output_indicator")
        self.workspace_objects[connect_node] = {'indicator': output_indicator, 'type': 'workspace_output'}

        self.canvas.tag_bind(connect_node, "<Button-1>", self.select_node)
        self.canvas.tag_bind(connect_node, "<Enter>", lambda e, id=connect_node: self.on_node_hover(id, True))
        self.canvas.tag_bind(connect_node, "<Leave>", lambda e, id=connect_node: self.on_node_hover(id, False))

    def toggle_input(self, toggle):
        self.states[toggle] = not self.states.get(toggle, False)
        new_color = "red" if self.states[toggle] else "grey"
        self.canvas.itemconfig(self.workspace_objects[toggle]['toggle'], fill=new_color)
        self.simulate_circuit()

    def select_node(self, event):
        node_id = self.canvas.find_withtag('current')[0]
        node_tags = self.canvas.gettags(node_id)

        if 'workspace_input' in node_tags:
            node_type = 'workspace_input'
        elif 'workspace_output' in node_tags:
            node_type = 'workspace_output'
        elif 'gate_input' in node_tags:
            node_type = 'gate_input'
        elif 'gate_output' in node_tags:
            node_type = 'gate_output'

        if self.selected_node:
            selected_node_tags = self.canvas.gettags(self.selected_node)

            if (('workspace_input' in selected_node_tags and node_type == 'gate_input') or
                ('gate_output' in selected_node_tags and node_type == 'workspace_output') or
                ('gate_output' in selected_node_tags and node_type == 'gate_input')):
                self.connect_nodes(self.selected_node, node_id)

            self.canvas.itemconfig(self.selected_node, fill="black")
            self.selected_node = None
        else:
            self.selected_node = node_id
            self.canvas.itemconfig(node_id, fill="blue")

    def connect_nodes(self, start_node, end_node):
        start_coords = self.canvas.coords(start_node)
        end_coords = self.canvas.coords(end_node)
        line = self.canvas.create_line(start_coords[0]+5, start_coords[1]+5, end_coords[0]+5, end_coords[1]+5, width=6, tags="wire")
        
        # Adjust drawing order
        self.canvas.tag_lower(line, "node")

        self.connections[(start_node, end_node)] = line
        self.canvas.tag_bind(line, "<Button-3>", self.on_wire_right_click)
        self.simulate_circuit()

    def on_wire_right_click(self, event):
        line_id = self.canvas.find_withtag('current')[0]
        self.delete_wire(line_id)

    def delete_wire(self, line_id):
        for conn, line in list(self.connections.items()):
            if line == line_id:
                del self.connections[conn]
                break
        self.canvas.delete(line_id)

    def on_node_hover(self, node_id, entering):
        if entering:
            self.canvas.itemconfig(node_id, outline="yellow")
        else:
            if node_id == self.selected_node:
                self.canvas.itemconfig(node_id, fill="blue")
            else:
                self.canvas.itemconfig(node_id, fill="black")

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

    def save_circuit_as_gate(self):
        name = simpledialog.askstring("New Gate", "Enter the name for the new gate:")
        if not name:
            return
        
        input_nodes = [obj for obj, details in self.workspace_objects.items() if details.get('type') == 'workspace_input']
        output_nodes = [obj for obj, details in self.workspace_objects.items() if details.get('type') == 'workspace_output']

        num_inputs = len(input_nodes)
        num_outputs = len(output_nodes)

        truth_table = {}

        for i in range(2 ** num_inputs):
            input_state = [(i >> bit) & 1 for bit in range(num_inputs)]
            
            for idx, node in enumerate(input_nodes):
                self.states[node] = input_state[idx] == 1
                toggle_color = "red" if self.states[node] else "grey"
                self.canvas.itemconfig(self.workspace_objects[node]['toggle'], fill=toggle_color)

            self.simulate_circuit()

            # Record the entire output state
            output_state = tuple(self.states.get(node, False) for node in output_nodes)
            truth_table[tuple(input_state)] = output_state

        self.gates[name] = Gate(name, num_inputs, num_outputs, truth_table)
        self.populate_operations()
        self.clear_board()

    def simulate_circuit(self):
        change_flag = True
        while change_flag:
            change_flag = False
            for (gate_obj, details) in self.workspace_objects.items():
                if 'gate' not in details:
                    continue

                gate = details['gate']
                input_nodes = [n for n in details['nodes'] if 'gate_input' in self.canvas.gettags(n)]
                output_nodes = [n for n in details['nodes'] if 'gate_output' in self.canvas.gettags(n)]

                inputs = tuple(self.states.get(node, False) for node in input_nodes)

                if gate.truth_table:
                    result = gate.evaluate(inputs)
                elif gate.name == "AND":
                    result = (all(inputs),)
                elif gate.name == "OR":
                    result = (any(inputs),)
                elif gate.name == "NOT":
                    result = (not inputs[0],)

                for idx, output_node in enumerate(output_nodes):
                    if result and self.states.get(output_node) != result[idx]:
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

    def clear_board(self):
        self.canvas.delete("all")
        self.workspace_objects.clear()
        self.connections.clear()
        self.states.clear()

if __name__ == '__main__':
    app = LogicCircuitDesigner()
    app.mainloop()