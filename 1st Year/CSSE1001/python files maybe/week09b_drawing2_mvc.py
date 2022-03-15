""" Model View Controller pattern (MVC) example."""

__author__ = "Benjamin Martin & Richard Thomas"
__copyright__ = "Copyright 2018, The University of Queensland"
__license__ = "MIT"
__date__ = "01/05/2018"


import random
import week09a_colours as colours
import tkinter as tk 
from tkinter import filedialog


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

class Circle(object) :
    def __init__(self, x, y, r, c) :
        self._x = int(x)
        self._y = int(y)
        self._radius = int(r)
        self._colour = c

    def move(self, dx, dy) :
        self._x += dx
        self._y += dy

    def get_bounds(self) :
        return [(self._x - self._radius, self._y - self._radius), 
                (self._x + self._radius, self._y + self._radius)]

    def get_colour(self) :
        return self._colour

    def __repr__(self) :
        return "Circle({0}, {1}, {2}, {3})".format(self._x, self._y, 
                                                   self._radius, self._colour)



class Model(object) :
    def __init__(self) :
        self._circles = []

    def load_circles(self, filename) :
        fd = open(filename, "r")
        self._circles = []
        for line in fd :
            line = line.strip()
            if line :
                self._circles.append(Circle(*line.split()))
    
    def get_circles(self) :
        return self._circles

    def move(self, circle, dx, dy) :
        circle.move(dx, dy)

        

class Controls(tk.Frame) :
    def __init__(self, master, parent) :
        super().__init__(master)
        tk.Button(self, text="Add", command=self.add).pack(side=tk.LEFT)
        tk.Button(self, text="Open", command=parent.open).pack(side=tk.LEFT)
        tk.Button(self, text="Move", command=self.move).pack(side=tk.LEFT)
        tk.Button(self, text="Delete", command=self.delete).pack(side=tk.LEFT)
        self._mode = "add"

    def add(self):
        self._mode = "add"

    def move(self) :
        self._mode = "move"

    def delete(self) :
        self._mode = "delete"

    def get_mode(self) :
        return self._mode


        
class View(tk.Canvas) :
    def __init__(self, master, model, controls, colour_choice) :
        super().__init__(master, bg='white')
        self.bind("<Button-1>", self.press1)
        self.bind("<B1-Motion>", self.motion1)
        self.save_x = None
        self.save_y = None
        self.id = None
        self._model = model
        self._controls = controls
        self._colour_choice = colour_choice
        self.redraw()
        self.ids = []


    def redraw(self) :
        self.ids = []
        self.delete(tk.ALL)
        for circle in self._model.get_circles() :
            self.ids.append(self.create_oval(circle.get_bounds(), 
                                             fill=circle.get_colour()))


    def press1(self, event) :
        mode = self._controls.get_mode()
        if mode == "move" :
            self.index = self.ids.index(self.find_closest(event.x, event.y)[0])
            self.save_x = event.x
            self.save_y = event.y
        elif mode == "add":
            radius = random.randint(5, 20)
            colour = self._colour_choice.get_colour()
            circle = Circle(event.x, event.y, radius, colour)
            self._model.get_circles().append(circle)
            self.redraw()
        else :
            cid = self.find_closest(event.x, event.y)[0]
            index = self.ids.index(cid)
            self._model.get_circles().pop(index)
            self.redraw()

       
    def motion1(self, event) :
        mode = self._controls.get_mode()
        if mode == "move":
            dx = event.x - self.save_x
            dy = event.y - self.save_y
            self.save_x = event.x
            self.save_y = event.y
            self._model.move(self._model.get_circles()[self.index], dx, dy)
            self.redraw()



class DrawingApp(object) :
    
    def __init__(self, master) :   
        master.title("Example 3")
        master.geometry("600x400")
        self._model = Model()
        self._controls = Controls(master, self)
        self._controls.pack()
        self._colour_choice = ColourChoice(master)
        self._colour_choice.pack(pady=10)
        self._view = View(master, self._model, self._controls, self._colour_choice)
        self._view.pack(expand=1, fill=tk.BOTH)

    def open(self) :
        filename = filedialog.askopenfilename()
        if filename :
            self._model.load_circles(filename)
            self._view.redraw()



def main() :
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__" :
    main()
