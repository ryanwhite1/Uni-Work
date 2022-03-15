"""
Draw random size circles with options of picking a random or specified colour.
"""

__author__ = "Benjamin Martin & Richard Thomas"
__copyright__ = "Copyright 2018, The University of Queensland"
__license__ = "MIT"
__date__ = "30/04/2018"


import tkinter as tk
import random
import week09a_colours as colours


class ColourChoice(tk.Frame):
    """Colour Choice Frame."""
    def __init__(self, master):
        super().__init__(master)
        
        self._colour_label = tk.Label(self,
                                      text='Enter drawing colour: ')
        self._colour_label.pack(side=tk.LEFT, padx = 10)

        self._colour_string = tk.StringVar()
        self._colour_string.set('red')
        self._colour_field = tk.Entry(self,
                                      textvariable=self._colour_string)
        self._colour_field.pack(side=tk.LEFT)

        random_colour_button = tk.Button(self,
                                         text='Random Colour',
                                         command=self._set_to_random)
        random_colour_button.pack(side=tk.LEFT, expand=True)

    def _set_to_random(self):
        self._colour_string.set(colours.generate_random_pastel())

    def get_colour(self):
        return self._colour_string.get()
        

class App(object) :
    def __init__(self, master) :
        master.title('Event Handling Example 2')
        master.geometry('800x600')

        # Colour Choice Frame
        self._colour_choice = ColourChoice(master)
        self._colour_choice.pack()

        # Drawing Canvas
        self._canvas = tk.Canvas(master, bg='white')
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._canvas.bind('<Button-1>', self._left_mouse_button)


    def _left_mouse_button(self, event) :
        radius = random.randint(5, 20)

        x0 = event.x - radius
        y0 = event.y - radius
        x1 = event.x + radius
        y1 = event.y + radius

        self._canvas.create_oval(x0, y0, x1, y1,
                                 fill=self._colour_choice.get_colour())
        # Could also use create_line, create_rectangle, etc.

       




def main() :
    root = tk.Tk()
    app = App(root)
    root.mainloop()



if __name__ == "__main__" :
    main()
