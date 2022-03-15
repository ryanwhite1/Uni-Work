"""
Simple GUI programming exercise to demonstrate simple graphics programming
and event handling.
"""

__copyright__ = "Copyright 2018, University of Queensland"


import tkinter as tk


class SettingsFrame(tk.Frame) :
    """A frame which allows users to change settings of the application
       Settings to change are: whether or not a line preview is shown.
    """
    def __init__(self, parent) :
        """Initialise the widget, with its subwidgets."""
        super().__init__(parent)

        self._position_label = tk.Label(self, text="Current Position:")
        self._position_label.pack(side=tk.LEFT)

        self._preview_button = tk.Button(self, text="Preview On", bg="green",
                                         command=self._toggle_preview)
        self._preview_button.pack(side=tk.RIGHT)
        self._preview = True

    def _toggle_preview(self) :
        """Toggle the line preview on/off."""
        if self._preview == True:
            self._preview_button.config(text="Preview Off", bg="grey")
            self._preview = False
        else:
            self._preview_button.config(text="Preview On", bg="green")
            self._preview = True
    def is_preview_on(self) :
        """(bool) Return True if the preview setting is on, otherwise False."""
        return self._preview
    def set_position(self, x, y) :
        """Change the 'Current Position' label to show new (x,y) coordinates."""
        self._position_label.config(text = "Current Position: " + str((x, y)))
        



class DrawingApp() :
    """An application for drawing lines."""
    def __init__(self, master) :
        """Initialise a DrawingApp object, including widget layout."""
        self._master = master
        master.title("Drawing Application")
        master.minsize(500, 375)

        self._canvas = tk.Canvas(master, bd=2, relief=tk.SUNKEN)
        self._canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self._canvas.bind('<Motion>', self.evt_motion)
        self._canvas.bind('<Button-1>', self.evt_click)
        self._firstclick = False

        self._settings = SettingsFrame(master)
        self._settings.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        menubar = tk.Menu(master)
        master.config(menu=menubar)

        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Exit", command=self.exit)

        editmenu = tk.Menu(menubar)
        menubar.add_cascade(label="Edit", menu=editmenu)
        editmenu.add_command(label="Clear All Lines", command=self.clear)

    def evt_motion(self, event) :
        """Event handler for Mouse movement on the Canvas."""
        self._settings.set_position(event.x, event.y)

    def evt_click(self, event):
        if self._firstclick == False:
            self._firstclick = True
            self._evt1 = (event.x, event.y)
        else:
            self._firstclick = False
            self._evt2 = (event.x, event.y)
            self._canvas.create_line(self._evt1, self._evt2)         

    def exit(self) :
        """Close the application."""
        self._master.destroy()

    def clear(self) :
        """Delete all lines from the application."""
        self._canvas.delete(tk.ALL)



if __name__ == '__main__' :
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
