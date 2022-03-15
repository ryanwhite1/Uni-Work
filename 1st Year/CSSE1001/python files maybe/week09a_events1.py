"""
Example of handling mouse and keyboard events.
"""

__author__ = "Peter Robinson & Richard Thomas"
__copyright__ = "Copyright 2018, The University of Queensland"
__license__ = "MIT"
__date__ = "30/04/2018"


import tkinter as tk 


class App(object) :
    
    def __init__(self, master) :   
        master.title("Event Handling Example")
        master.geometry("400x200")
        self._canvas = tk.Canvas(master, bg='white')
        # self._canvas.pack()
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._canvas.bind("<Button-1>", self.press1)
        self._canvas.bind("<B1-Motion>", self.motion1)
        self._canvas.bind("<ButtonRelease-1>", self.release1)
        self._canvas.bind_all("<Key>", self.key_press)

    def press1(self, event) :
        print("press", event.x, event.y)

    def motion1(self, event) :
        print("motion", event.x, event.y)

    def release1(self, event) :
        print("release", event.x, event.y)

    def key_press(self, event) :
        print(event.char, event.keysym, event.keycode)



def main() :
    root = tk.Tk()
    app = App(root)
    root.mainloop()



if __name__ == "__main__" :
    main()
