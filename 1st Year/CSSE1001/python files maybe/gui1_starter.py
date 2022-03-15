"""
Simple GUI programming exercise to demonstrate component layout
and event handling.
"""

__copyright__ = "Copyright 2018, University of Queensland"


import tkinter as tk
from tkinter import messagebox


class SampleApp(object) :
    def __init__(self, master) :
        self._master = master
        master.title("Hello!")
        master.minsize(430, 200)

        self._lbl = tk.Label(master, text="Choose a button")
        self._lbl.pack(side=tk.TOP, expand=True)

        btn_frame = tk.Frame(master)
        btn_frame.pack(side=tk.TOP, pady=10)

        bluebtn = tk.Button(btn_frame, text="Change to Blue", command=self.blue)
        bluebtn.pack(side=tk.LEFT)

        greenbtn = tk.Button(btn_frame, text="Change to Green", command=self.green)
        greenbtn.pack(side=tk.RIGHT)

        eval_frame = tk.Frame(master)
        eval_frame.pack(side=tk.BOTTOM, pady=10, padx=10)

        entry_lbl = tk.Label(eval_frame, text="Change the colour to:")
        entry_lbl.pack(side=tk.LEFT)
        self.entry = tk.Entry(eval_frame)
        self.entry.pack(side=tk.LEFT)
        entry_btn = tk.Button(eval_frame, text="Change it!", command=self.change_colour)
        entry_btn.pack(side=tk.LEFT)        

    def say_hello(self) :
        print('Hello! Thanks for clicking!')

    def blue(self):
        self._lbl.config(text="This label is blue", bg="blue")

    def green(self):
        self._lbl.config(text="This label is green", bg="green")

    def change_colour(self):
        exp = str(self.entry.get())
        string = "This label is " + exp
        try:
            self._lbl.config(text=string, bg=exp)
        except tk.TclError:
            messagebox.showerror("Invalid colour", "'" + exp + "'" + " is not a colour!")


if __name__ == "__main__" :
    root = tk.Tk()
    app = SampleApp(root)
    root.mainloop()
