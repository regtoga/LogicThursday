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
    """
    Constructor for a new gate, Gates have:
    1. name
    2. number inputs
    3. number outputs
    4. functions to calculate output
    """
    def __init__(self, name:str, inputs:int, outputs:int, boolean_exprs:list):
        "Initialize a gate with a name, inputs, outputs and a list of functions"
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.boolean_exprs = boolean_exprs

    def evaluate(self, input_state):
        """Will evaluate the outputs for a gate when executed"""
        results = []
        for expr in self.boolean_exprs:
            try:
                #gates outputs are calculated using my GTT's calculate Function output method.
                output = GTT_Thinker.calculateFunctionOutput(expr.replace(" ", ""), input_state)
                results.append(output)
            except Exception as e:
                print(f"Error evaluating function: {e}")
                results.append(False)
        #return the results as a tuple even if there is only one
        return tuple(results)

class LogicSim_gui(tk.Toplevel):
    def __init__(self, main_menu_ref, position="+100+100"):
        super().__init__(main_menu_ref)
        self.main_menu_ref = main_menu_ref
        self.title("Logic Circuit Designer")
        self.geometry(position)
        self.geometry("1055x600")
        
        #This dictionary holds the built in gates, These are AND, OR, and NOT, though OR isn't strictly fundemential
        self.gate_definitions = {
            "AND": (2, 1, ["AB"]),
            "OR": (2, 1, ["A+B"]),
            "NOT": (1, 1, ["A'"])
        }
        
        #create a iteratable object that will hold every gate that we can interact with.
        self.gates = {name: Gate(name, *details) for name, details in self.gate_definitions.items()}
        #Create lists that will store items and object that user will be interacting with.
        self.workspace_objects = {}
        self.connections = {}
        self.states = {}
        
        #Create status flags
        self.preview_item = None
        self.dragged_gate = None
        self.selected_node = None
        self.moving_gate = None
        self.move_start = None

        self.create_frames()
        self.load_custom_gates()

    def create_frames(self):
        """Creates a frame on the left for the buttons and a nother frame on the left for the workspace"""
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
        """Creates all the initial buttons"""
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
        """This function creates the buttons for the gates.
        This is done by iterating though the self.gates variable and making a button called the name of each gate."""
        #I believe this clears the frame of all buttons so that we dont endup with any duplicates
        for widget in self.operations_frame.winfo_children():
            if isinstance(widget, tk.Button) and widget not in self.buttons_frame.winfo_children():
                widget.destroy()
        
        #populate the operations frame with the gate buttons
        for gate_name in self.gates:
            button = tk.Button(self.operations_frame, text=gate_name)
            button.bind("<Button-1>", self.start_drag)
            if gate_name not in self.gate_definitions:  # Custom gates
                button.bind("<Button-3>", self.delete_gate_file)
            button.pack(pady=2)

    def start_drag(self, event):
        """
        this is used with the gate buttons, when the user wants a gate, a drag event happens
        This means that when the cursor is above the canvas a dotted outline of the gate will appear,
        finally the user will click and the selected gate will appear.
        """
        widget = event.widget
        gate = widget.cget("text")
        self.dragged_gate = self.gates[gate]
        self.canvas.bind("<Motion>", self.update_preview)

    def update_preview(self, event):
        """Functions creats the preview (dotted rectangle) around where the gate would go if the user clicked"""
        if self.preview_item:
            self.canvas.delete(self.preview_item)
        x, y = event.x, event.y
        #if you make y+40 dynamic you could fix the issue with your inputs overflowing out of the box's bounds
        #just clamp it to a minimum value then depending on the gate selected's number of inputs and outputs make it bigger by the 
        #height of a single I/O node
        self.preview_item = self.canvas.create_rectangle(x, y, x+80, y+40, dash=(5, 2), outline="gray")

    def on_canvas_click(self, event):
        """
        Trigger the place gate function when the user clicks on the canvas while dragging is active.
        else if dragging is not active try and select whatever the user clicked on.
        """
        item = self.canvas.find_withtag('current')
        if self.dragged_gate:
            #place the gate
            self.place_gate(event.x, event.y)
        elif item:
            if 'gate' in self.canvas.gettags(item):
                #select thing on canvas
                self.select_gate(item[0])

    def place_gate(self, x, y):
        """This function takes an x and y cordinate and makes a chip in that space using the gate currently in self.dragged_gate"""
        #if you make y+40 dynamic you could fix the issue with your inputs overflowing out of the box's bounds
        #just clamp it to a minimum value then depending on the gate selected's number of inputs and outputs make it bigger by the 
        #height of a single I/O node
        gate_obj = self.canvas.create_rectangle(x, y, x+80, y+40, fill="lightblue", tag="gate")
        #y+20 should actually be half of y+40 if you implement dynamic chip sizes
        text_obj = self.canvas.create_text(x+40, y+20, text=self.dragged_gate.name, tags=("text",))
        #add the gate's information to the workspace's object list
        self.workspace_objects[gate_obj] = {'gate': self.dragged_gate, 'nodes': [], 'text': text_obj}

        #for each input the chip has, make an input node 
        for i in range(self.dragged_gate.inputs):
            input_node = self.canvas.create_oval(x-5, y+10*i+10, x+5, y+10*i+20, fill="black", tags=("node", "gate_input"))
            self.workspace_objects[gate_obj]['nodes'].append(input_node)
            self.workspace_objects[input_node] = {'parent': gate_obj, 'type': 'gate_input'}
            self.canvas.tag_bind(input_node, "<Button-1>", self.select_node)

        #for each output the chip has, make an output node.
        for i in range(self.dragged_gate.outputs):
            output_node = self.canvas.create_oval(x+75, y+10*i+10, x+85, y+10*i+20, fill="black", tags=("node", "gate_output"))
            self.workspace_objects[gate_obj]['nodes'].append(output_node)
            self.workspace_objects[output_node] = {'parent': gate_obj, 'type': 'gate_output'}
            self.canvas.tag_bind(output_node, "<Button-1>", self.select_node)

        #reset the dragged_gate to None as the drag has ended.
        self.dragged_gate = None
        self.canvas.delete(self.preview_item)
        self.canvas.unbind("<Motion>")
        #give the chip a right click handler that will prompt for the deletion of a chip.
        self.canvas.tag_bind(gate_obj, "<Button-3>", self.prompt_delete_gate)

    def select_gate(self, gate_id):
        """if the thing clicked is a gate this will handle the starting and ending movements of that gate"""
        #if i wanted to move the Input and outputs, i bet i could implement that here pretty easily
        if gate_id in self.workspace_objects and 'gate' in self.workspace_objects[gate_id]:
            self.moving_gate = gate_id
            #visually change the gates colors to give visual feedback something is happening
            self.invert_gate_colors(gate_id)
            self.move_start = self.canvas.coords(gate_id)[:2]
            #start movement
            self.canvas.bind("<B1-Motion>", self.move_gate)
            #end movment
            self.canvas.bind("<ButtonRelease-1>", self.end_move_gate)

    def prompt_delete_gate(self, event):
        """Calling this will trigger a messagebox to ask if the user actually wants to delete the selected chip."""
        gate_id = self.canvas.find_withtag('current')[0]
        result = messagebox.askyesno("Delete Confirmation", "Do you want to delete this gate?", parent=self.canvas)
        if result:
            self.delete_gate(gate_id)

    def delete_gate(self, gate_id):
        """
        Takes a input "gate_id" and will handle the deletion of that chip
            a. Needs to delete the connections to other chips
            b. Needs to delete the I/O nodes related to the chip
            c. Needs to delete the chip's body on the canvas
            d. Needs to remove the chip's id from the list of chips
        """
        #get the connections to delete
        connections_to_delete = [(start, end) for start, end in self.connections if start in self.workspace_objects[gate_id]['nodes'] or end in self.workspace_objects[gate_id]['nodes']]

        #delete the connections and the line on the canvas
        for conn in connections_to_delete:
            line = self.connections[conn]
            self.canvas.delete(line)
            del self.connections[conn]

        #delete the nodes related to this chip
        for node in self.workspace_objects[gate_id]['nodes']:
            self.canvas.delete(node)
            del self.workspace_objects[node]

        #Delete the text box on the chip
        text = self.workspace_objects[gate_id]['text']
        self.canvas.delete(text)
        #Finally delete the chip's body
        self.canvas.delete(gate_id)
        del self.workspace_objects[gate_id]

    def move_gate(self, event):
        """
        This function will move the chip thats inside the: self.moving_gate variable
        Things that need to move about the location of the cursor:
        1. the gates body
        2. the gate's I/O nodes
        3. all the lines from this chip to other chips
        4. the text on the chip describing it
        """
        if self.moving_gate and self.move_start:
            #get the chagne in x and y by subtracting where it was from where the mouse is now.
            dx = event.x - self.move_start[0]
            dy = event.y - self.move_start[1]
            #move the body of the chip
            self.canvas.move(self.moving_gate, dx, dy)
            
            #update the positions of all the nodes and all the connections between them
            for node in self.workspace_objects[self.moving_gate]['nodes']:
                self.canvas.move(node, dx, dy)
                for connection, line in self.connections.items():
                    if node in connection:
                        self.update_line(connection, line)

            #move the text on the chip
            text = self.workspace_objects[self.moving_gate]['text']
            self.canvas.move(text, dx, dy)
            self.move_start = (event.x, event.y)

    def update_line(self, nodes, line):
        """
        This function takes two nodes in a list formarly known as a connection and calculates
        how the line should be updated baised on those cordinates.
        """
        start_node, end_node = nodes
        start_coords = self.canvas.coords(start_node)
        end_coords = self.canvas.coords(end_node)
        color = "red" if self.states.get(start_node, False) else "grey"
        self.canvas.itemconfig(line, fill=color)
        self.canvas.coords(line, start_coords[0]+5, start_coords[1]+5, end_coords[0]+5, end_coords[1]+5)

    def end_move_gate(self, event):
        """
        This function Ends the movement of a gate by fixing its colors, and resetting the "self.moving_gate" and "self.move_start" flags.
        """
        if self.moving_gate:
            self.invert_gate_colors(self.moving_gate)
        self.moving_gate = None
        self.move_start = None
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def select_node(self, event):
        """
        This functions will visually change a node when clicked to show that is selected.
        If there is allready a node selected form a connections and unchange the other node.
        """
        node_id = self.canvas.find_withtag('current')[0]
        node_tags = self.canvas.gettags(node_id)

        #if we have already selected a node and the node just clicked is a valid canidate to be connected with... form a connection
        if self.selected_node:
            selected_node_tags = self.canvas.gettags(self.selected_node)
            if (('workspace_input' in selected_node_tags and 'gate_input' in node_tags) or
                ('gate_output' in selected_node_tags and 'workspace_output' in node_tags) or
                ('gate_output' in selected_node_tags and 'gate_input' in node_tags)):
                self.connect_nodes(self.selected_node, node_id)

            self.canvas.itemconfig(self.selected_node, fill="black")
            self.selected_node = None
        #else the node just selected is the new self.selected_node so that next time we might be able to form a connection. 
        else:
            self.selected_node = node_id
            self.canvas.itemconfig(node_id, fill="blue")

    def connect_nodes(self, start_node, end_node):
        """This functions takes two nodes and forms a connection between them, then creates a line using the cordinates"""
        #if there is allready a connection between these two nodes or it the nodes are somehow the same then dont make a connection
        if (start_node, end_node) in self.connections or start_node == end_node:
            return

        #get the cordinates of the two nodes
        start_coords = self.canvas.coords(start_node)
        end_coords = self.canvas.coords(end_node)
        #form a line between the two cords, update the connections list with the line reference
        line = self.canvas.create_line(start_coords[0]+5, start_coords[1]+5, end_coords[0]+5, end_coords[1]+5, width=6, tags="wire")
        self.connections[(start_node, end_node)] = line
        #if the line is rightclicked delete the the connection, and the wire
        self.canvas.tag_bind(line, "<Button-3>", self.delete_wire)

        #simulate circuit needs to be ran to update the results of all the gates
        self.simulate_circuit()

    def delete_wire(self, event):
        """
        This function is called by a right click on a wire, when that happens it takes a reference from that wire 
        then deletes all information about that connection.
        """
        line_id = self.canvas.find_withtag('current')[0]
        for conn, line in list(self.connections.items()):
            if line == line_id:
                del self.connections[conn]
                break
        self.canvas.delete(line_id)

    def delete_workspace_element(self, element_id):
        """
        This function is used to delete workspace inputs and workspace outputs.
        """
        if element_id in self.workspace_objects:
            element = self.workspace_objects[element_id]
            #if either workspace input or output delete it
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
        """function inverts the colors of the gate passed"""
        current_fill = self.canvas.itemcget(gate_id, "fill")
        inverted_fill = "blue" if current_fill == "lightblue" else "lightblue"
        self.canvas.itemconfig(gate_id, fill=inverted_fill)

    def save_circuit_as_gate(self):
        """This function's job is to take all of the gates and connections and simulate a minimized function-
        to describe the chip as a whole. The chip will be saved to a file to be loaded later."""
        #Ask user for name of chip, this is limited to 14 chars just because i dont want the filenames getting too long.
        name = simpledialog.askstring("New Gate", "Enter the name for the new gate (max 14 characters):")
        if not name or len(name) > 14:
            messagebox.showerror("Error", "Invalid gate name. Must be 1-14 characters.")
            return

        #Get all input and outputs nodes so that we can count the ammount of them we have.
        input_nodes = [obj for obj, details in self.workspace_objects.items() if details.get('type') == 'workspace_input']
        output_nodes = [obj for obj, details in self.workspace_objects.items() if details.get('type') == 'workspace_output']

        num_inputs = len(input_nodes)
        num_outputs = len(output_nodes)

        truth_table = {}
        functions = []

        for out_idx in range(num_outputs):
            minterms = []
            counterr = 0
            #For each output calculate every combination 
            #so essentially what this does is count in binary until and for each number we plug into the
            #circuit curently on the workspace and append its result to a function which we can use to find the minimized functions
            for i in range(2 ** num_inputs):
                input_state = [(i >> bit) & 1 for bit in range(num_inputs)]
                for idx, node in enumerate(input_nodes):
                    self.states[node] = input_state[idx] == 1

                #This function calculates what is on the workspace for a any given states
                self.simulate_circuit()

                #if the output of the circuit was 1 append it to the minterms
                output_state = self.states.get(output_nodes[out_idx], False)
                if output_state == True:
                    minterms.append(counterr)

                counterr += 1

            #calculate the function expression
            stuff2 = "Z'm("
            for minterm in minterms:
                stuff2 += (f"{minterm},")

            #remove the last comma
            stuff2 = stuff2[:-1]
            stuff2 += ")"

            #Calculate the minimized Function utilizing my TTG.
            ttg_thinker = TTG_Thinker.TruthTableToGates(stuff2, f"importpt{out_idx}")
            ttg_thinker.calculateanswer()
            #append result to the answer list
            functions.append(ttg_thinker.get_Answer().replace("F = ", ""))
            del ttg_thinker
            os.remove(f"importpt{out_idx}")

        #add the newly formed gate the programs bank of gates
        self.gates[name] = Gate(name, num_inputs, num_outputs, boolean_exprs=functions)
        #add the new gate to the path of all the chips so that we can load it from memory next time
        with open(os.path.join(CHIP_DIR, f"{name}.pkl"), 'wb') as f:
            pickle.dump((num_inputs, num_outputs, functions), f)

        #clean the board, then refresh the operations pane.
        self.clear_board()
        self.populate_operations()

    def simulate_circuit(self):
        """
        This function simulates the values of every gate, input, wire, and output in the workspace.
        """
        #function knows to stop once there is no longer any changes hapening in the circuit.
        #think about how we might not know how many changes may need to be calculated, so once it settles down...
        #or colapses on a steady state
        change_flag = True
        while change_flag:
            change_flag = False
            #Iterates though every object on the workspace 
            for gate_obj, details in self.workspace_objects.items():
                #if the object is not a gate then ignore.
                if 'gate' not in details:
                    continue
                #Get relevent I/O locations
                gate = details['gate']
                input_nodes = [n for n in details['nodes'] if 'gate_input' in self.canvas.gettags(n)]
                output_nodes = [n for n in details['nodes'] if 'gate_output' in self.canvas.gettags(n)]
                #Get inputs values
                inputs = tuple(self.states.get(node, False) for node in input_nodes)
                #Calculate result
                result = gate.evaluate(inputs)

                #update the outupts on the gate
                for idx, output_node in enumerate(output_nodes):
                    if idx < len(result) and self.states.get(output_node) != result[idx]:
                        self.states[output_node] = result[idx]
                        change_flag = True

            #based on the new states update the wire colors
            for (start_node, end_node), line in self.connections.items():
                state = self.states.get(start_node, False)
                self.canvas.itemconfig(line, fill="red" if state else "grey")
                if self.states.get(end_node) != state:
                    self.states[end_node] = state
                    change_flag = True

            #finally update the output indicators
            for obj, details in self.workspace_objects.items():
                if details.get('type') == 'workspace_output':
                    connected_nodes = [start for (start, end) in self.connections if end == obj]
                    indicator_color = "red" if any(self.states.get(node, False) for node in connected_nodes) else "grey"
                    self.canvas.itemconfig(details['indicator'], fill=indicator_color)

    def add_input(self):
        """This adds an toggle button input to the left side of the workspace"""
        coords = (5, 10 + len([w for w in self.workspace_objects.values() if w.get('type') == 'workspace_input']) * 30)
        toggle_button = self.canvas.create_oval(*coords, coords[0]+20, coords[1]+20, fill="grey", tag="toggle_button")
        connect_node = self.canvas.create_oval(coords[0]+25, coords[1]+5, coords[0]+35, coords[1]+15, fill="black", tags=("node", "workspace_input"))

        self.workspace_objects[connect_node] = {'type': 'workspace_input', 'toggle': toggle_button}
        self.states[connect_node] = False

        self.canvas.tag_bind(toggle_button, "<Button-1>", lambda event, toggle=connect_node: self.toggle_input(toggle))
        self.canvas.tag_bind(connect_node, "<Button-1>", self.select_node)
        self.canvas.tag_bind(connect_node, "<Button-3>", lambda event, element=connect_node: self.delete_workspace_element(element))

    def add_output(self):
        """This adds an indicator output to the right side of the workspace"""
        coords = (self.canvas.winfo_width() - 50, 10 + len([w for w in self.workspace_objects.values() if w.get('type') == 'workspace_output']) * 30)
        connect_node = self.canvas.create_oval(coords[0], coords[1]+5, coords[0]+10, coords[1]+15, fill="black", tags=("node", "workspace_output"))
        indicator = self.canvas.create_oval(coords[0]+15, coords[1], coords[0]+35, coords[1]+20, fill="grey", tag="output_indicator")

        self.workspace_objects[connect_node] = {'type': 'workspace_output', 'indicator': indicator}

        self.canvas.tag_bind(connect_node, "<Button-1>", self.select_node)
        self.canvas.tag_bind(connect_node, "<Button-3>", lambda event, element=connect_node: self.delete_workspace_element(element))

    def toggle_input(self, toggle):
        """Function for workspace input's toggle button"""
        self.states[toggle] = not self.states.get(toggle, False)
        self.canvas.itemconfig(self.workspace_objects[toggle]['toggle'], fill="red" if self.states[toggle] else "grey")
        self.simulate_circuit()

    def clear_board(self):
        """This function simply clears the workspace"""
        self.canvas.delete("all")
        self.workspace_objects.clear()
        self.connections.clear()
        self.states.clear()

    def cancel_action(self, event):
        """This function is simple enough, it just cancels the action happening"""
        #Deselects a node if called while a node is active
        if self.selected_node:
            self.canvas.itemconfig(self.selected_node, fill="black")
            self.selected_node = None

        #this cancels the pending placement of a gate
        if self.preview_item:
            #reset the dragged_gate to None as the drag has been canceled.
            self.dragged_gate = None
            self.canvas.delete(self.preview_item)
            self.canvas.unbind("<Motion>")

        #this handles when a gate is not being moved anymore
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
        """This function is how we import TTG tables as a chip and also other chips as chips"""
        def calc():
            root = tk.Tk()
            root.withdraw()

            #open a file manager box 
            file_path = filedialog.askopenfilename(
                initialdir=CHIP_DIR,
                title="Select a File",
                filetypes=(("Pickle Files", "*.pkl*"), ("all files", "*.*"))
            )

            #if filepath is not empty
            if file_path:
                try:
                    #try and open the file
                    with open(file_path, "rb") as file:
                        TableFromStorage = pickle.load(file)

                    # Load and unpack all expressions for the custom gate
                    name_without_ext = os.path.basename(file_path).replace(".pkl", "")

                    #because how truth tables work they are always len powers of 2
                    #so this case only works for Dedicated chips
                    if len(TableFromStorage) == 3:
                        num_inputs = TableFromStorage[0]
                        num_outputs = TableFromStorage[1]
                        function_exprs = TableFromStorage[2]
                        
                    #chip must be in the format of a truthtable   
                    else:
                        name_without_ext = os.path.basename(file_path).replace(".pkl", "")
                        num_inputs = int(math.log(len(TableFromStorage), 2))
                        num_outputs = len(TableFromStorage[0])
                        function_exprs = []
                        #for each column in the truthtable (each output) calculate the minimized function
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

                            ttg_thinker = TTG_Thinker.TruthTableToGates(stuff2, f"importpt{depth}")
                            ttg_thinker.calculateanswer()
                            #append result to the answer bit
                            function_exprs.append(ttg_thinker.get_Answer().replace("F = ", ""))
                            del ttg_thinker
                            os.remove(f"importpt{depth}")
                            
                    #append the new gate to the table of gates        
                    self.gates[name_without_ext] = Gate(name_without_ext, num_inputs, num_outputs, boolean_exprs=function_exprs)

                    #save the imported file into the chips directory, so that we can load them later
                    with open(os.path.join(CHIP_DIR, f"{name_without_ext}.pkl"), 'wb') as f:
                        pickle.dump((num_inputs, num_outputs, function_exprs), f)

                    #refresh the operations pane
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
            #if you want to comment this, that is fine i just do like a little extra workspace if i am allowed to have more.
            #self.resizable(False, False)

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