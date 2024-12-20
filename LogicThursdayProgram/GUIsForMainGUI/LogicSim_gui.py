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
                if type(expr) == bool:
                    results.append(expr)
                else:
                    output = GTT_Thinker.calculateFunctionOutput(expr.replace(" ", ""), input_state)
                    #print(self.name, expr.replace(" ", ""), output, input_state)
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
        self.dontdocanvasclick = False

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
        self.preview_tag = "preview_item"
        if self.preview_item:
            self.canvas.delete(self.preview_tag)
        x, y = event.x, event.y

        lenrectang = 25+4*(len(self.dragged_gate.name))
        #determine if the box needs to be scaled about the inputs or the ouputs
        if self.dragged_gate.inputs > self.dragged_gate.outputs:
            heirectang = 20+10*(self.dragged_gate.inputs)
            offset = (self.dragged_gate.inputs / self.dragged_gate.outputs)
        elif self.dragged_gate.inputs < self.dragged_gate.outputs:
           heirectang = 20+10*(self.dragged_gate.outputs) 
           offset = (self.dragged_gate.outputs / self.dragged_gate.inputs)
        else:
            heirectang = 20+10*(self.dragged_gate.inputs)
            offset = 1

        # Create the main rectangle for the preview item
        self.preview_item = self.canvas.create_rectangle(x, y, x+lenrectang, y+heirectang, fill="lightblue", tags=self.preview_tag)

        # Add the text to the canvas and assign the same tag
        text_obj = self.canvas.create_text(x+(lenrectang/2), y+(heirectang/2), text=self.dragged_gate.name, tags=self.preview_tag)

        # Add input nodes to the canvas and assign the same tag
        for i in range(self.dragged_gate.inputs):
            if self.dragged_gate.inputs > self.dragged_gate.outputs:
                input_node = self.canvas.create_oval(x-5, y+10*i+10, x+5, y+10*i+20, fill="black", tags=self.preview_tag)
            else:
                nodeoffset = 10 * (i * offset) + 10
                input_node = self.canvas.create_oval(x-5, y+nodeoffset, x+5, y+nodeoffset+10, fill="black", tags=self.preview_tag)

        # Add output nodes to the canvas and assign the same tag
        for i in range(self.dragged_gate.outputs):
            if self.dragged_gate.inputs > self.dragged_gate.outputs:
                nodeoffset = 10*(i*offset)+10
                output_node = self.canvas.create_oval(x+lenrectang-5, y+nodeoffset, x+lenrectang+5, y+nodeoffset+10, fill="black", tags=self.preview_tag)
            else:
                output_node = self.canvas.create_oval(x+lenrectang-5, y+10*i+10, x+lenrectang+5, y+10*i+20, fill="black", tags=self.preview_tag)

    def on_canvas_click(self, event):
        """
        Trigger the place gate function when the user clicks on the canvas while dragging is active.
        else if dragging is not active try and select whatever the user clicked on.
        """
        #if i dont want it to click, then i disable it for a single click
        if self.dontdocanvasclick == False:

            item = self.canvas.find_withtag('current')

            if self.dragged_gate:
                #place the gate
                self.place_gate(event.x, event.y)
            elif item:
                if 'gate' in self.canvas.gettags(item):
                    #select thing on canvas
                    self.select_gate(item[0])
            #if there is a node selected
            elif self.selected_node:
                node_tags = self.canvas.gettags(self.selected_node)

                if len(item) == 0:
                    #if nothing was clicked and if a node was selected make a wire that goes to that point
                    if node_tags[1] == 'workspace_input' or node_tags[1] == 'gate_input' or node_tags[1] == 'wire_node_input':
                        self.place_part_of_wire(event.x, event.y, "wire_node_input")
                    else:
                        self.place_part_of_wire(event.x, event.y, "wire_node_output")
        else:
            #re enable the on canvas click
            self.dontdocanvasclick = False

    def place_part_of_wire(self, x, y, type_node):
        #This huge if statement is a copy of the one below in the select node function, if you change one change both
        #all it does is define what types of connections are allowed between nodes
        selected_node_tags = self.canvas.gettags(self.selected_node)
        if (('workspace_input' in selected_node_tags and 'gate_input' in type_node) or
            ('gate_output' in selected_node_tags and 'workspace_output' in type_node) or
            ('gate_output' in selected_node_tags and 'gate_input' in type_node) or
            ('wire_node_input' in selected_node_tags and 'wire_node_input' in type_node) or
            ('wire_node_output' in selected_node_tags and 'wire_node_output' in type_node) or
            ('wire_node_input' in selected_node_tags and 'workspace_output' in type_node) or
            ('wire_node_input' in selected_node_tags and 'gate_input' in type_node) or
            ('gate_output' in selected_node_tags and 'wire_node_output' in type_node) or
            ('wire_node_output' in selected_node_tags and 'gate_input' in type_node) or
            ('workspace_input' in selected_node_tags and 'workspace_output' in type_node) or
            ('workspace_input' in selected_node_tags and 'wire_node_input' in type_node) or
            ('wire_node_output' in selected_node_tags and 'workspace_output' in type_node)):

            #create a rectangle behind the node to have the same format as a normal gate
            wire_obj = self.canvas.create_rectangle(x, y, x, y, fill="lightblue", tag="gate")
            self.workspace_objects[wire_obj] = {'wire': self.dragged_gate, 'nodes': []}

            #make and attach the node to the rectangle
            wire_node = self.canvas.create_oval(x-5, y, x+5, y+10, fill="black", tags=("node", type_node))
            self.workspace_objects[wire_obj]['nodes'].append(wire_node)
            self.workspace_objects[wire_node] = {'parent': wire_obj, 'type': type_node}

            #bind the button to the new node
            self.canvas.tag_bind(wire_node, "<Button-1>", self.select_node)
            #select the node thus making a connection and making life good
            self.select_node(wire_node)


    def place_gate(self, x, y):
        """This function takes an x and y cordinate and makes a chip in that space using the gate currently in self.dragged_gate"""
        #if you make y+40 dynamic you could fix the issue with your inputs overflowing out of the box's bounds
        #just clamp it to a minimum value then depending on the gate selected's number of inputs and outputs make it bigger by the 
        #height of a single I/O node

        lenrectang = 25+4*(len(self.dragged_gate.name))
        #determine if the box needs to be scaled about the inputs or the ouputs
        if self.dragged_gate.inputs > self.dragged_gate.outputs:
            heirectang = 20+10*(self.dragged_gate.inputs)
            offset = (self.dragged_gate.inputs / self.dragged_gate.outputs)
        elif self.dragged_gate.inputs < self.dragged_gate.outputs:
           heirectang = 20+10*(self.dragged_gate.outputs) 
           offset = (self.dragged_gate.outputs / self.dragged_gate.inputs)
        else:
            heirectang = 20+10*(self.dragged_gate.inputs)
            offset = 1
           

        gate_obj = self.canvas.create_rectangle(x, y, x+lenrectang, y+heirectang, fill="lightblue", tag="gate")
        #y+20 should actually be half of y+40 if you implement dynamic chip sizes
        text_obj = self.canvas.create_text(x+(lenrectang/2), y+(heirectang/2), text=self.dragged_gate.name, tags=("text",))
        #add the gate's information to the workspace's object list
        self.workspace_objects[gate_obj] = {'gate': self.dragged_gate, 'nodes': [], 'text': text_obj}

        #for each input the chip has, make an input node 
        for i in range(self.dragged_gate.inputs):
            if self.dragged_gate.inputs > self.dragged_gate.outputs:
                input_node = self.canvas.create_oval(x-5, y+10*i+10, x+5, y+10*i+20, fill="black", tags=("node", "gate_input"))
            else:
                nodeoffset = 10*(i*offset)+10
                input_node = self.canvas.create_oval(x-5, y+nodeoffset, x+5, y+nodeoffset+10, fill="black", tags=("node", "gate_input"))
            self.workspace_objects[gate_obj]['nodes'].append(input_node)
            self.workspace_objects[input_node] = {'parent': gate_obj, 'type': 'gate_input'}
            self.canvas.tag_bind(input_node, "<Button-1>", self.select_node)

        #for each output the chip has, make an output node.
        for i in range(self.dragged_gate.outputs):
            if self.dragged_gate.inputs > self.dragged_gate.outputs:
                nodeoffset = 10*(i*offset)+10
                output_node = self.canvas.create_oval(x+lenrectang-5, y+nodeoffset, x+lenrectang+5, y+nodeoffset+10, fill="black", tags=("node", "gate_output"))
            else:
                output_node = self.canvas.create_oval(x+lenrectang-5, y+10*i+10, x+lenrectang+5, y+10*i+20, fill="black", tags=("node", "gate_output"))
            self.workspace_objects[gate_obj]['nodes'].append(output_node)
            self.workspace_objects[output_node] = {'parent': gate_obj, 'type': 'gate_output'}
            self.canvas.tag_bind(output_node, "<Button-1>", self.select_node)

        #reset the dragged_gate to None as the drag has ended.
        self.dragged_gate = None
        self.canvas.delete(self.preview_tag)
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
            self.delete_wire(self.connections[conn])

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
        #if event is equal to None then we need to connect the wire to a new node that will allow for complicated wires
        if type(event) != int:
            node_id = self.canvas.find_withtag('current')[0]
        else:
            node_id = event

        node_tags = self.canvas.gettags(node_id)

        #if we have already selected a node and the node just clicked is a valid canidate to be connected with... form a connection
        if self.selected_node:
            selected_node_tags = self.canvas.gettags(self.selected_node)
            #if you mess with this if statement i would recomend also changing the identical one above
            if (('workspace_input' in selected_node_tags and 'gate_input' in node_tags) or
                ('gate_output' in selected_node_tags and 'workspace_output' in node_tags) or
                ('gate_output' in selected_node_tags and 'gate_input' in node_tags) or
                ('wire_node_input' in selected_node_tags and 'wire_node_input' in node_tags) or
                ('wire_node_output' in selected_node_tags and 'wire_node_output' in node_tags) or
                ('wire_node_input' in selected_node_tags and 'gate_input' in node_tags) or
                ('wire_node_input' in selected_node_tags and 'workspace_output' in node_tags) or
                ('gate_output' in selected_node_tags and 'wire_node_output' in node_tags) or
                ('workspace_input' in selected_node_tags and 'workspace_output' in node_tags) or
                ('wire_node_output' in selected_node_tags and 'gate_input' in node_tags) or
                ('workspace_input' in selected_node_tags and 'wire_node_input' in node_tags) or
                ('wire_node_output' in selected_node_tags and 'workspace_output' in node_tags)):
                self.connect_nodes(self.selected_node, node_id)

            self.canvas.itemconfig(self.selected_node, fill="black")
            self.selected_node = None
            
            #auto select the 2nd node because it was just created by the user, so it should be selected
            if type(event) == int:
                self.select_node(event)
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
        #render the nodes above the wires!
        try:
            self.canvas.tag_lower("wire", "node")
        except:
            pass
        self.connections[(start_node, end_node)] = line
        #if the line is rightclicked delete the the connection, and the wire
        self.canvas.tag_bind(line, "<Button-3>", self.delete_wire)
        self.canvas.tag_bind(line, "<Button-1>", self.split_wire)

        #simulate circuit needs to be ran to update the results of all the gates
        self.simulate_circuit()

    def delete_wire(self, wire):
        """
        This function is called by a right click on a wire, when that happens it takes a reference from that wire 
        then deletes all information about that connection.
        """
        if type(wire) == int:
            line_id = wire
        else:
            line_id = self.canvas.find_withtag('current')[0]
            
        findmore = []       
        connectionss = []

        for conn, line in list(self.connections.items()):
            if line == line_id:
                findmore.append(conn[0])
                findmore.append(conn[1])
                del self.connections[conn]
            else:
                connectionss.append(conn[0])
                connectionss.append(conn[1])
                
        #if for each id in the connection (conn) check if there is any connections to the nodes
        #if not delete the node because it is allalone.... there can be more than one alone node per deleteion..
        for i in findmore:
            if (i not in connectionss) and (i in self.workspace_objects):
                element = self.workspace_objects[i]
                if 'type' in element and element['type'] in ["wire_node_input", "wire_node_output"] :
                    parent = element.get('parent')
                    #delete the node's parent
                    self.canvas.delete(parent)
                    #delete the reference in the array of all objects
                    del self.workspace_objects[i]
                    #delete the node
                    self.canvas.delete(i)
                    
        self.canvas.delete(line_id)

    def split_wire(self, event):
        """
        This function should make a new node where the wire was right clicked and delete the wire,
        then the nodes should both be selected and connected to the new node splitting the wire
        """

        line_id = self.canvas.find_withtag('current')[0]
        findmore = []       

        #delete the old wire from the innerworkings
        for conn, line in list(self.connections.items()):
            if line == line_id:
                findmore.append(conn[0])
                findmore.append(conn[1])
                del self.connections[conn]

        #delete the old wire from the canvas
        self.canvas.delete(line_id)  


        #create a new node at cursor position
        #create a rectangle behind the node to have the same format as a normal gate
        wire_obj = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, fill="lightblue", tag="gate")
        self.workspace_objects[wire_obj] = {'wire': self.dragged_gate, 'nodes': []}


        node_tags = self.canvas.gettags(findmore[0])
        node_tagss = self.canvas.gettags(findmore[1])

        if node_tags[1] == 'workspace_input' or node_tags[1] == 'gate_input' or node_tags[1] == 'wire_node_input' or node_tagss[1] == 'workspace_input' or node_tagss[1] == 'gate_input' or node_tagss[1] == 'wire_node_input':
            node_tag = "wire_node_input"
        else:
            node_tag = "wire_node_output"

        #make and attach the node to the rectangle
        wire_node = self.canvas.create_oval(event.x-5, event.y, event.x+5, event.y+10, fill="black", tags=("node", node_tag))
        self.workspace_objects[wire_obj]['nodes'].append(wire_node)
        self.workspace_objects[wire_node] = {'parent': wire_obj, 'type': node_tag}

        
        #bind the button to the new node
        self.canvas.tag_bind(wire_node, "<Button-1>", self.select_node)


        #form the new connections
        #im resetting these because i think it will help with a bug im getting, when splitting wires random things connect to other random things!
        if self.selected_node != None:
            self.canvas.itemconfig(self.selected_node, fill="black")
            self.selected_node = None

        #select all nodes that had a connection broken
        self.select_node(findmore[0])
        #select new node
        self.select_node(wire_node)

        #im resetting these because i think it will help with a bug im getting, when splitting wires random things connect to other random things!
        if self.selected_node != None:
            self.canvas.itemconfig(self.selected_node, fill="black")
            self.selected_node = None
            
        #select new node
        self.select_node(wire_node)
        #select all nodes that had a connection broken
        self.select_node(findmore[1])
                
        #im resetting these because i think it will help with a bug im getting, when splitting wires random things connect to other random things!
        if self.selected_node != None:
            self.canvas.itemconfig(self.selected_node, fill="black")
            self.selected_node = None        

        #finally select the node because obiously you wanted it!
        self.select_node(wire_node)
        self.dontdocanvasclick = True

     
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

        #this will allows us to pass reference to the number of inputs to the thinkers, this is VERRY important for correct results
        ValidInputChars = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')

        #Get all input and outputs nodes so that we can count the ammount of them we have.
        input_nodes = [obj for obj, details in self.workspace_objects.items() if details.get('type') == 'workspace_input']
        output_nodes = [obj for obj, details in self.workspace_objects.items() if details.get('type') == 'workspace_output']

        num_inputs = len(input_nodes)
        num_outputs = len(output_nodes)

        tempinputchars = ""

        for input in range(0, num_inputs):
            if input == 0:
              tempinputchars += f"{ValidInputChars[input]}"  
            else:
                tempinputchars += f",{ValidInputChars[input]}"

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
                somelist = []

                # Reverse the assignment to count in the desired order.
                for idx, node in enumerate(input_nodes):
                    # This will reverse the order of indexing because it is backwards by default
                    reversed_idx = len(input_nodes) - 1 - idx  
                    
                    self.states[node] = input_state[reversed_idx] == 1
                    somelist.append(input_state[reversed_idx] == 1)

                #This function calculates what is on the workspace for the given states
                self.simulate_circuit()

                #if the output of the circuit was 1 append it to the minterms
                output_state = self.states.get(output_nodes[out_idx], False)
                if output_state == True:
                    minterms.append(counterr)

                counterr += 1

            #calculate the function expression
            stuff2 = f"F({tempinputchars}) = Z'm("
            for minterm in minterms:
                stuff2 += (f"{minterm},")

            #if the answer function is empty:
            if stuff2[-1] != '(':
                #remove the last comma
                stuff2 = stuff2[:-1]
                stuff2 += ")"

                #Calculate the minimized Function utilizing my TTG.
                ttg_thinker = TTG_Thinker.TruthTableToGates(stuff2, f"importpt{out_idx}")
                ttg_thinker.calculateanswer()
                #append result to the answer list
                returnedanswer = ttg_thinker.get_Answer().replace("F = ", "")
                if returnedanswer != '':
                    functions.append(returnedanswer)
                else:
                    #if it is empty and the minterms are not empty, it should return true
                    functions.append(True)
                
                del ttg_thinker
                os.remove(f"importpt{out_idx}")
            else:
                #if it is empty and the minterms are empty the "function" should return false
                functions.append(False)
                

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
        #my bandaid fix is to stop the simulation after so many iterations, the other way this could be done is though using a death timer
        counter = 0

        change_flag = True
        while change_flag:

            if counter >= 10000:
                messagebox.showerror("Error", "You have either a infinite loop or logic error in your ciruit!", parent=self.canvas)
                return

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

            counter += 1

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
            self.canvas.delete(self.preview_tag)
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