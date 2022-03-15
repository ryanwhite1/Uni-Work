"""
Example of using multiple frames as a containers.
Bind a StringVar to the Entry to allow easier setting of Entry's value.
"""

__author__ = "Benjamin Martin & Richard Thomas"
__copyright__ = "Copyright 2018, The University of Queensland"
__license__ = "MIT"
__date__ = "30/04/2018"


import tkinter as tk


class App(object) :
    def __init__(self, master):
        master.title('Frames Example 4')
        master.geometry('800x600')

        self._top_frame = tk.Frame(master, bg = 'yellow')
        self._top_frame.pack(fill=tk.BOTH, expand=True)
        self._middle_frame = tk.Frame(master, bg = 'orange')
        self._middle_frame.pack(fill=tk.BOTH, expand=True)
        self._bottom_frame = tk.Frame(master, bg = 'goldenrod')
        self._bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        self._label = tk.Label(self._top_frame, text='Hello World!', bg='red')
        self._label.pack(side=tk.RIGHT, expand=True)

        self._colour_string = tk.StringVar()
        self._colour_field = tk.Entry(self._middle_frame,
                                      textvariable=self._colour_string)
        self._colour_field.pack()

        reset_button = tk.Button(self._bottom_frame, text='Reset',
                                 command=self._reset)
        reset_button.pack(side=tk.LEFT, expand=True)

        colour_button = tk.Button(self._bottom_frame, text='Set Colour',
                                  command=self._set_to_colour)
        colour_button.pack(side=tk.LEFT, expand=True)

       
    def _reset(self) :
        self._colour_string.set('yellow')
        self._set_to_colour()
       
       
    def _set_to_colour(self) :
        colour = self._colour_string.get()
        self._label.config(bg=colour)



def main() :
    root = tk.Tk()
    app = App(root)
    root.mainloop()



if __name__ == "__main__" :
    main()
