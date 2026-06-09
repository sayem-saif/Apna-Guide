import tkinter as tk
from PIL import ImageTk, Image

from config.cities import VALID_CITIES, START_CITY
from utils import (
    build_city_graph,
    nearest_neighbor_path,
    trim_path_to_destination,
    calculate_path_distance,
    draw_graph,
    highlight_path,
)


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
        self.label = tk.Label(self.master, text="Welcome to Apna Guide !", font=("Inter", 20))
        self.label.pack(side="bottom", pady=25)

        self.name_label = tk.Label(self.master, text="Please Enter Your Destination :", font=("Inter Bold", 14))
        self.name_label.pack(side="top", pady=15)

        self.name_entry = tk.Entry(self.master, width=30, font=("Arial", 14))
        self.name_entry.pack(side="top", pady=10)

        self.greet_button = tk.Button(self.master, text="Guide", command=self.greet_user, font=("Algerian", 14))
        self.greet_button.pack(side="top", pady=10)

        self.close_button = tk.Button(self.master, text="Show Path", command=self.show_path, font=("Algerian", 14))
        self.close_button.pack(side="top", padx=10, pady=10)

    def show_path(self):
        name = self.name_entry.get()
        if name not in VALID_CITIES:
            self.label.config(text="Invalid City name!")
            return

        G = build_city_graph()
        full_path = nearest_neighbor_path(G, START_CITY)
        trimmed_path = trim_path_to_destination(full_path, name)
        total_distance = calculate_path_distance(G, trimmed_path)

        pos = draw_graph(G)
        highlight_path(G, pos, trimmed_path, total_distance)

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
