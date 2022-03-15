"""
Draw random size circles with options of picking a random or specified colour.
"""

__author__ = "Benjamin Martin & Richard Thomas"
__copyright__ = "Copyright 2018, The University of Queensland"
__license__ = "MIT"
__date__ = "01/05/2018"


import tkinter as tk
import random
import week09a_colours as colours


class ColourChoice(tk.Frame) :
    """Colour Choice Frame."""
    
    def __init__(self, master) :
        super().__init__(master)
        self._colour_label = tk.Label(self, text='Enter drawing colour:')
        self._colour_label.pack(side=tk.LEFT, padx=10)

        self._colour_string = tk.StringVar()
        self._colour_string.set('red')
        self._colour_field = tk.Entry(self, textvariable=self._colour_string)
        self._colour_field.pack(side=tk.LEFT)

        random_colour_button = tk.Button(self, text='Random Colour',
                                         command=self._set_to_random)
        random_colour_button.pack(side=tk.LEFT, expand=True, padx=50)

       
    def _set_to_random(self) :
        self._colour_string.set(colours.generate_random_pastel())

    def get_colour(self) :
        return self._colour_string.get()



class Controls(tk.Frame) :
    """Drawing Controls."""
    
    def __init__(self, master) :
        super().__init__(master)
        tk.Button(self, text="Add", command=self.add).pack(side=tk.LEFT, padx=30)
        tk.Button(self, text="Move", command=self.move).pack(side=tk.LEFT)
        tk.Button(self, text="Delete", command=self.delete).pack(side=tk.LEFT, padx=30)
        self._mode = "add"

    def add(self) :
        self._mode = "add"

    def move(self) :
        self._mode = "move"

    def delete(self) :
        self._mode = "delete"

    def get_mode(self) :
        return self._mode



class Menus(object) :
    def __init__(self, master, file_methods, controls_methods):   
        menubar = tk.Menu(master)
        master.config(menu=menubar)    # Tell master what it's menu is
        # File menu
        file_menu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=file_methods[0])
        # Controls menu
        controls_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Controls", menu=controls_menu)
        controls_menu.add_command(label="Add", command=controls_methods[0])
        controls_menu.add_command(label="Move", command=controls_methods[1])
        controls_menu.add_command(label="Delete", command=controls_methods[2])



class DrawingApp(object) :
    def __init__(self, master) :
        master.title('Drawing Example')
        master.geometry('800x600')
        self._master = master

        # Configuration Frames
        self._controls = Controls(master)
        self._controls.pack()
        self._colour_choice = ColourChoice(master)
        self._colour_choice.pack(pady=10)

        self._menu = Menus(master, [self.close],
                           [self._controls.add,
                            self._controls.move,
                            self._controls.delete])

        # Drawing Canvas
        self._canvas = tk.Canvas(master, bg='white')
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._canvas.bind('<Button-1>', self.left_mouse_button)
        self._canvas.bind("<B1-Motion>", self.motion)

        master.protocol("WM_DELETE_WINDOW", self.close)


    def left_mouse_button(self, event) :
        mode = self._controls.get_mode()
        if mode == "add" :
            radius = random.randint(5, 20)
            x0 = event.x - radius
            y0 = event.y - radius
            x1 = event.x + radius
            y1 = event.y + radius
            self._canvas.create_oval([(x0, y0), (x1, y1)],
                                     fill=self._colour_choice.get_colour())
        elif mode == "move" :
            self._object_id = self._canvas.find_closest(event.x, event.y)
            self._save_x = event.x
            self._save_y = event.y
        else :   # delete mode
            self._canvas.delete(self._canvas.find_closest(event.x, event.y))


    def motion(self, event) :
        mode = self._controls.get_mode()
        if mode == "move" :
            dx = event.x - self._save_x
            dy = event.y - self._save_y
            self._save_x = event.x
            self._save_y = event.y
            self._canvas.move(self._object_id, dx, dy)


    def close(self) :
        """Exit the drawing application."""
        self._master.destroy()



def main() :
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__" :
    main()
