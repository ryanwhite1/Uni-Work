"""
An interactive visualization demonstrating how Tkinter's pack method behaves
with combinations of the expand, fill, and side parameters.

Docstring comments are formatted according to the Introduction to Software
Engineering course (CSSE1001) at the University of Queensland.
See http://csse1001.uqcloud.net/notes/commenting
"""
import tkinter as tk

__author__ = "Benjamin Martin"
__copyright__ = "Copyright 2017, The University of Queensland"
__license__ = "MIT"
__date__ = "02/05/2017"
__version__ = "1.0.0"

GRASS_COLOUR = '#77DD77'
FENCE_COLOUR = '#836953'

ROOF_COLOUR = '#FF6961'
ROOF_OUTLINE_COLOUR = '#C23B22'
WALL_COLOUR = '#AEC6CF'
WALL_OUTLINE_COLOUR = '#779ECB'
DOOR_COLOUR = '#FFB347'

# Measured in pixels
ROOF_OVERHANG_SIZE = 25
FENCE_SIZE = 10
YARD_PADDING = 10


class House(tk.Canvas):
    """Static widget that displays a resizable drawing of a house."""

    def __init__(self, master, **kwargs):
        """
        Constructor

        Parameters:
            master (tk.Tk|tk.Frame): The parent widget.
            kwargs (dict<*, *>): Keyword arguments for tk.Canvas.
        """
        super().__init__(master, **kwargs)

        self.bind("<Configure>", self.draw)

    def draw(self, ev):
        """Draws the house."""
        self.delete(tk.ALL)
        width = self.winfo_width()
        height = self.winfo_height()

        building = self.create_rectangle(0 + ROOF_OVERHANG_SIZE, height * 0.33,
                                         width - ROOF_OVERHANG_SIZE, height - 1,
                                         fill=WALL_COLOUR,
                                         outline=WALL_OUTLINE_COLOUR)

        roof = self.create_polygon((0, height * 0.33), (width, height * 0.33),
                                   (width / 2, 0), fill=ROOF_COLOUR,
                                   outline=ROOF_OUTLINE_COLOUR)


class HouseYardFrame(tk.Frame):
    """Simple widget that visualizes .pack's expand/fill/side parameters."""

    def __init__(self, master, size, expand, fill, side, *args, **kwargs):
        """
        Constructor

        Parameters:
            master (tk.Tk|tk.Frame): The parent widget.
            size (tuple<int, int>): Initial size. Width, height pair in pixels.
            expand (bool): Expand setting for visualization.
            fill (constant): Fill setting for visualization. Must be a valid
                             fill argument to .pack.
            side (constant): Side setting for visualization. Must be a valid
                             side argument to .pack.
            args (tuple<*>): Positional arguments for tk.Canvas.
            kwargs (dict<*, *>): Keyword arguments for tk.Canvas.
        """
        super().__init__(master, *args, **kwargs)

        self._fence = fence = tk.Frame(self, bd=FENCE_SIZE, bg=FENCE_COLOUR)
        fence.pack(fill=tk.BOTH, expand=True)

        self._yard = yard = tk.Frame(fence, bd=YARD_PADDING, bg=GRASS_COLOUR)
        yard.pack(fill=tk.BOTH, expand=True)

        width, height = size

        self._house = house = House(yard, width=width, height=height,
                                    bd=0, highlightthickness=0, bg=GRASS_COLOUR)
        house.pack(expand=True)

        self.set_pack_options(expand, fill, side)

    def set_pack_options(self, expand, fill, side):
        """
        Sets the pack options and refreshes the visualization.

        Parameters:
            expand (bool): Expand setting for visualization.
            fill (constant): Fill setting for visualization. Must be a valid
                             fill argument to .pack.
            side (constant): Side setting for visualization. Must be a valid
                             side argument to .pack.
        """
        self._fence.pack(expand=expand, side=side)
        self._house.pack(fill=fill)


class ConfigControl(tk.Frame):
    """Convenience widget to display an option menu & label with a simple
    change handler."""

    def __init__(self, master, label_text, values, default_value, on_change,
                 **kwargs):
        """
        Constructor

        Parameters:
            master (tk.Tk|tk.Frame): The parent widget.
            label_text (str): The text for the label.
            values (iterable(*)): Values to display in the option menu. Ordered
                                  by iteration order.
            default_value (*): Default value to select in the option menu.
            on_change (function): Function to be called when the option menu's
                                  value changes. Called as on_change(new_value).
            kwargs (dict<*, *>): Keyword arguments for tk.Canvas.

        """
        super().__init__(master)

        label = tk.Label(self, text=label_text)
        label.pack()
        self._var = var = tk.StringVar(value=default_value)
        var.trace("w", lambda name, index, mode, var=var: on_change(var.get()))
        expand_select = tk.OptionMenu(self, var, *values)
        expand_select.pack()

    def get(self):
        """(*) Returns the currently selected value from the option menu."""
        return self._var.get()


class ExpandFillExampleApp:
    """
    Top-level application.

    Interactive demonstration of how Tkinter widgets behave visually based upon
    combinations of expand, fill, and side arguments to .pack method.

    User can reconfigure options dynamically.
    """
    expand_options = (
        "False",
        "True"
    )

    fill_options = (
        "tk.NONE",
        "tk.X",
        "tk.Y",
        "tk.BOTH"
    )

    side_options = (
        "tk.TOP",
        "tk.LEFT",
        "tk.BOTTOM",
        "tk.RIGHT"
    )

    def __init__(self, master):
        """
        Constructor

        Parameters:
            master (tk.Tk): The root window.
        """
        self._master = master
        master.geometry("500x500")

        self._house = HouseYardFrame(master, (100, 100), True, tk.NONE,
                                     tk.TOP, bg='blue')
        self._house.pack(expand=True, fill=tk.BOTH)

        # controls
        control_frame = tk.Frame(master)

        self._expand = ConfigControl(control_frame, "Expand",
                                     self.expand_options,
                                     self.expand_options[0], self._configure)
        self._expand.pack(side=tk.LEFT)

        self._fill = ConfigControl(control_frame, "Fill", self.fill_options,
                                   self.fill_options[0], self._configure)
        self._fill.pack(side=tk.LEFT)

        self._side = ConfigControl(control_frame, "Side", self.side_options,
                                   self.side_options[0], self._configure)
        self._side.pack(side=tk.LEFT)

        control_frame.pack()

        self._configure()

    def _configure(self, *args):
        """Reconfigures the visualization.

        Parameters:
            args (tuple<*>): Useless. Allows method to be called with any
                             number of arguments.
        """
        self._house.set_pack_options(eval(self._expand.get()),
                                     eval(self._fill.get()),
                                     eval(self._side.get()))


def main():
    """Instantiates GUI for visualization."""
    root = tk.Tk()
    ExpandFillExampleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
