"""
Example of using a text widget with a file menu and file dialog.
"""


__author__ = "Peter Robinson & Richard Thomas"
__copyright__ = "Copyright 2018, The University of Queensland"
__license__ = "MIT"
__date__ = "01/05/2018"


import tkinter as tk 
from tkinter import filedialog


class App(object) :
    
    def __init__(self, master):   
        master.title("Simple Text Editor")
        self._master = master
        self._text = tk.Text(master)
        self._text.pack(expand=True, fill=tk.BOTH)
        
        # File menu
        menubar = tk.Menu(master)
        self._master.config(menu=menubar)    # Tell master what it's menu is
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.new_file)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        self._filename = None


    def new_file(self) :
        self._text.delete("1.0", tk.END)
        self._filename = None
        self._master.title("New File")


    def save_file(self) :
        if self._filename is None :
            filename = filedialog.asksaveasfilename()
            if filename :
                self.filename = filename
        if self.filename :
            self._master.title(self.filename)
            file = open(self.filename, 'w')
            file.write(self._text.get("1.0", tk.END))
            file.close()
            

    def open_file(self) :
        filename = filedialog.askopenfilename()
        if filename :
            self.filename = filename
            self._master.title(self.filename)
            file = open(filename, 'r')
            self._text.insert(tk.INSERT, file.read())
            file.close()



def main() :
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__" :
    main()
