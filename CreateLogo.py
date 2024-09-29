import tkinter as tk
from tkinter import colorchooser, simpledialog, messagebox, filedialog
import math

class LogoCreator:
    def __init__(self, master):
        self.master = master
        master.title("Simple Logo Creator")

        # Create canvas
        self.canvas = tk.Canvas(master, width=400, height=300, bg="white")
        self.canvas.pack()

        # Shape selection
        self.shape_options = ["Rectangle", "Oval", "Line", "Diamond", "Star"]
        self.shape_var = tk.StringVar(value=self.shape_options[0])  # Default shape

        # Dropdown menu for shape selection
        self.shape_menu = tk.OptionMenu(master, self.shape_var, *self.shape_options)
        self.shape_menu.pack()

        # Buttons
        self.color_button = tk.Button(master, text="Choose Color", command=self.choose_color)
        self.color_button.pack()

        self.text_button = tk.Button(master, text="Add Text", command=self.add_text)
        self.text_button.pack()

        self.toggle_button = tk.Button(master, text="Switch to Move Mode", command=self.toggle_mode)
        self.toggle_button.pack()

        self.save_button = tk.Button(master, text="Save Logo", command=self.save_logo)
        self.save_button.pack()

        self.clear_button = tk.Button(master, text="Clear", command=self.clear_canvas)
        self.clear_button.pack()

        self.color = "black"
        self.is_moving_mode = False

        # Variables for dragging
        self.start_x = None
        self.start_y = None
        self.current_shape = None
        self.current_text = None

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_shape)
        self.canvas.bind("<ButtonRelease-1>", self.release_draw)
        self.canvas.bind("<Button-3>", self.select_shape)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code[1]:
            self.color = color_code[1]

    def toggle_mode(self):
        self.is_moving_mode = not self.is_moving_mode
        if self.is_moving_mode:
            self.toggle_button.config(text="Switch to Add Mode")
            self.canvas.bind("<Button-1>", self.select_shape)
            self.canvas.bind("<B1-Motion>", self.move_shape)
        else:
            self.toggle_button.config(text="Switch to Move Mode")
            self.canvas.bind("<Button-1>", self.start_draw)
            self.canvas.bind("<B1-Motion>", self.draw_shape)

    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.current_shape = None  # Reset current shape

    def draw_shape(self, event):
        if self.current_shape:
            self.canvas.delete(self.current_shape)  # Remove previous shape
        x1, y1 = self.start_x, self.start_y
        x2, y2 = event.x, event.y
        shape_type = self.shape_var.get()

        if shape_type == "Rectangle":
            self.current_shape = self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.color)
        elif shape_type == "Oval":
            self.current_shape = self.canvas.create_oval(x1, y1, x2, y2, outline=self.color)
        elif shape_type == "Line":
            self.current_shape = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.color, width=2)
        elif shape_type == "Diamond":
            self.current_shape = self.create_diamond(x1, y1, x2, y2)
        elif shape_type == "Star":
            self.current_shape = self.create_star(x1, y1, x2, y2)

    def release_draw(self, event):
        # Finalize the shape when mouse is released
        if self.current_shape:
            self.canvas.itemconfig(self.current_shape, fill=self.color)

    def add_text(self):
        text = simpledialog.askstring("Input", "Enter your logo text:")
        if text:
            x = self.canvas.winfo_width() // 2
            y = self.canvas.winfo_height() // 2
            self.current_text = self.canvas.create_text(x, y, text=text, fill=self.color, font=("Arial", 16))

    def create_diamond(self, x1, y1, x2, y2):
        return self.canvas.create_polygon(
            (x1 + x2) / 2, y1,  # Top
            x2, (y1 + y2) / 2,  # Right
            (x1 + x2) / 2, y2,  # Bottom
            x1, (y1 + y2) / 2,  # Left
            outline=self.color, fill=self.color
        )

    def create_star(self, x1, y1, x2, y2):
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        size = min(abs(x2 - x1), abs(y2 - y1)) / 2

        points = []
        for i in range(5):
            angle = math.radians(i * 144)  # Star angles
            x = center_x + size * math.cos(angle)
            y = center_y - size * math.sin(angle)
            points.extend((x, y))

        return self.canvas.create_polygon(points, outline=self.color, fill=self.color)

    def select_shape(self, event):
        if self.is_moving_mode:
            item = self.canvas.find_closest(event.x, event.y)
            if item:
                self.canvas.itemconfig(item, fill="yellow")  # Highlight the selected shape
                self.canvas.bind("<B1-Motion>", lambda e, i=item: self.move_shape(e, i))

    def move_shape(self, event, item):
        dx = event.x - self.canvas.coords(item)[0]
        dy = event.y - self.canvas.coords(item)[1]
        self.canvas.move(item, dx, dy)

    def save_logo(self):
        # Save the canvas as a bitmap
        file_path = filedialog.asksaveasfilename(defaultextension=".bmp",
                                                   filetypes=[("Bitmap files", "*.bmp"),
                                                              ("All files", "*.*")])
        if file_path:
            self.canvas.update()  # Update the canvas
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()

            # Create a new bitmap image
            bitmap = tk.PhotoImage(width=width, height=height)
            bitmap.blank()  # Clear the image

            # Draw all items in the canvas
            for item in self.canvas.find_all():
                coords = self.canvas.coords(item)
                if self.canvas.type(item) == "rectangle":
                    bitmap.tk.create_rectangle(*coords, outline=self.canvas.itemcget(item, "outline"), 
                                                fill=self.canvas.itemcget(item, "fill"))
                elif self.canvas.type(item) == "oval":
                    bitmap.tk.create_oval(*coords, outline=self.canvas.itemcget(item, "outline"), 
                                           fill=self.canvas.itemcget(item, "fill"))
                elif self.canvas.type(item) == "line":
                    bitmap.tk.create_line(*coords, fill=self.canvas.itemcget(item, "fill"), 
                                          width=int(self.canvas.itemcget(item, "width")))
                elif self.canvas.type(item) == "text":
                    bitmap.tk.create_text((coords[0], coords[1]), text=self.canvas.itemcget(item, "text"),
                                           fill=self.canvas.itemcget(item, "fill"))

            # Save the bitmap image
            bitmap.write(file_path, format='bmp')
            messagebox.showinfo("Success", "Logo saved successfully!")

    def clear_canvas(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    logo_creator = LogoCreator(root)
    root.mainloop()
