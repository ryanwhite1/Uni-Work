import tkinter as tk


class App:
    def __init__(self, master):
        #GUI instantiation code goes here
        master.title('GUI Example')
        #root.geometry('800x600')

        self._colour = tk.Entry(master)
        self._colour.pack()

        self._label = tk.Label(master, text='oWo whats this :3', bg='red')
        self._label.pack()

        red = tk.Button(master, text='Red', command=self._red)
        red.pack()

        blue = tk.Button(master, text='Blue', command=self._blue)
        blue.pack()

        colour_button = tk.Button(master, text='Set Colour', command=self._set_colour)
        colour_button.pack()

    def _set_colour(self):
        colour = self._colour.get()
        self._label.config(bg = colour)

    def _red(self):
        self._label.config(bg='red')

    def _blue(self):
        self._label.config(bg='blue')

##        bad_button = tk.Button(master, text='naughty naughty', command=self._bad_click)
##        bad_button.pack(side=tk.RIGHT, expand=True, ipadx=50)
##
##        good_button = tk.Button(master, text='praise jesus', command=self._good_click)
##        good_button.pack(side=tk.LEFT, expand=True, fill = tk.X, padx = 50)
##
##    def _good_click(self):
##        print('MOONPIE')
##
##    def _bad_click(self):
##        print('you have sunk my battleship')

        




root = tk.Tk()
app = App(root)
root.mainloop() # last thing to run
