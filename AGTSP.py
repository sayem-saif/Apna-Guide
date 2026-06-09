import matplotlib.pyplot as plt
import tkinter as tk
from PIL import ImageTk, Image

from tsp_core import (
    VALID_CITIES,
    DEFAULT_START,
    build_city_graph,
    nearest_neighbor_path,
    trim_path_to_destination,
    calculate_path_distance,
    validate_city,
)
import networkx as nx

class WelcomeWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.config(background='black')
        self.master.title("Apna Guide Using TSP")
        

        # Load the background image
        self.bg_image = ImageTk.PhotoImage(Image.open("fl.jpg"))
        self.bg_label = tk.Label(self.master, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create the widgets
        self.create_widgets()

    def create_widgets(self):
        # Create the label, entry widget, and buttons
        self.label = tk.Label(self.master, text="Welcome to Apna Guide !", font=("Inter", 20))
        self.label.pack(side="bottom", pady=25)

        self.name_label = tk.Label(self.master, text="Please Enter Your Destination :", font=("Inter Bold", 14))
        self.name_label.pack(side="top", pady=15)

        self.name_entry = tk.Entry(self.master, width=30, font=("Arial", 14))
        self.name_entry.pack(side="top", pady=10)

        self.greet_button = tk.Button(self.master, text="Guide", command=self.greet_user, font=("Algerian", 14))
        self.greet_button.pack(side="top", pady=10)

        # Connected to show_path method instead of destroying the window
        self.close_button = tk.Button(self.master, text="Show Path", command=self.show_path, font=("Algerian", 14))
        self.close_button.pack(side="top", padx=10, pady=10)

    # Handles Show Path button click - will display TSP path on graph
    def show_path(self):
        name = self.name_entry.get()
        if validate_city(name):
            G = build_city_graph()

            # Draw the graph
            pos = nx.get_node_attributes(G, 'pos')
            nx.draw(G, pos, with_labels=True, node_size=5000, font_size=15, font_color='white')

            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=15)

            # Find approximate solution using nearest neighbor heuristic
            path = nearest_neighbor_path(G, DEFAULT_START)
            trimmed_path = trim_path_to_destination(path, name)
            total_distance = calculate_path_distance(G, trimmed_path)

            # Show the plot
            path_edges = list(zip(trimmed_path[:-1], trimmed_path[1:]))

            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
            plt.suptitle(f"Path: {' \u2192 '.join(trimmed_path)} | Distance: {total_distance} km", fontsize=10, y=0.98, x=0.02, ha='left')
            plt.subplots_adjust(top=0.75)
            plt.tight_layout()
            plt.show()
        else:
            error = "Invalid City name!"
            self.label.config(text=error)

    def greet_user(self):
        name = self.name_entry.get()
        if name:
            greeting = f'''Hello From Mumbai To {name} This is The Shortest and Minimum cost path.
*Click On Show Path To View Shortest Path or Enter Another Destination*'''
        else:
            greeting = "Hello! Welcome to my app."
        self.label.config(text=greeting)

# Create a new instance of Tkinter
root = tk.Tk()

# Set the size of the main window and center it on the screen
root.geometry("600x400+400+200")

# Create the welcome window
app = WelcomeWindow(master=root)

# Run the main loop
app.mainloop()

