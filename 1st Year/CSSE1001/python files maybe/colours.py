from colorsys import hls_to_rgb
import random

__author__ = "Benjamin Martin"
__copyright__ = "Copyright 2018, The University of Queensland"
__license__ = "MIT"
__date__ = "11/04/2018"
__version__ = "1.0.0"

def generate_random_rgb(h_min=0., h_max=1., s_min=.5, s_max=.7, l_min=.65, l_max=.85):
    """Generates a random RGB colour within a subset of the HSL spectrum

    Parameters:
        h_min (float): The minimum value for the hue
        h_max (float): The maximum value for the hue
        s_min (float): The minimum value for the saturation
        s_max (float): The maximum value for the saturation
        l_min (float): The minimum value for the lightness
        l_max (float): The maximum value for the lightness

    Return:
        tuple<float, float, float>: (red, green, blue)
    """
    hue = random.random() * (h_max - h_min) + h_min
    saturation = random.random() * (s_max - s_min) + s_min
    lightness = random.random() * (l_max - l_min) + l_min
    return hls_to_rgb(hue, lightness, saturation)

def rgb_to_hex(r, g, b, normalise=True):
    """Converts an ('r', 'g', 'b') triple to hex code

    Return:
        str: Hex colour code of the form #rrggbb
    """
    
    if normalise:
        r, g, b = list(int(i * 256) for i in (r, g, b))
    return f'#{r:02X}{g:02X}{b:02X}'

def generate_random_pastel():
    """(str) Returns the hex code for a randomly generated pastel colour"""
    return rgb_to_hex(*generate_random_rgb())

def main():
    import tkinter as tk

    ROWS = 10
    COLUMNS = 20
    PADDING = 20
    
    root = tk.Tk()

    for row in range(ROWS):
        for column in range(COLUMNS):
            colour = generate_random_pastel()
            text = colour
            label = tk.Label(root, text=text, bg=colour, font=('Helvetica', 16))
            label.grid(row=row, column=column, ipadx=PADDING, ipady=PADDING, sticky=tk.NSEW)
            root.columnconfigure(column, weight=1, uniform='colour')

    root.mainloop()

if __name__ == "__main__":
    main()
