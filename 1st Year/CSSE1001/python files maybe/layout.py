"""
Example of a Tkinter GUI focusing primarily on a variety of layout options.

Look carefully at the differences between one frame and the next frame.
Resize the window and see how the layout changes.

This example is not really in an OO style - if it were, then the various
components (i.e. each frame) would have been made to inherit from Frame and
contain the relevant buttons.
"""

import tkinter as tk

# A standard message box
from tkinter import messagebox

__author__ = "Peter Robinson, Benjamin Martin"
__copyright__ = "Copyright 2012-2017, The University of Queensland"
__license__ = "MIT"
__date__ = "05/05/2017"
__version__ = "1.1.1"


class DemoApp(object):
    """More comprehensive Tkinter pack layout demonstration."""

    def __init__(self, master):
        """
        Constructor

        Parameters:
             master (tk.Tk): The parent widget.
        """
        master.title("Layout Demo")
        self._master = master

        master.protocol("WM_DELETE_WINDOW", self.quit)

        # Create a frame and put some buttons in it
        frame1 = tk.Frame(master, bg='black')
        frame1.pack()

        self.button1 = tk.Button(frame1, text="Button 01", bg='green',
                                 width=len("Button 01") + 10)
        self.button1.pack(side=tk.LEFT)

        self.button2 = tk.Button(frame1, text="Button 02", bg='green')
        self.button2.pack(side=tk.LEFT)

        self.button3 = tk.Button(frame1, text="Button 03", bg='green')
        self.button3.pack(side=tk.LEFT)

        # Create another frame and put some buttons in it
        frame2 = tk.Frame(master, bg='black')
        frame2.pack(fill=tk.X)

        self.button4 = tk.Button(frame2, text="Button 04", bg='green')
        self.button4.pack(side=tk.LEFT, expand=True)

        self.button5 = tk.Button(frame2, text="Button 05", bg='green')
        self.button5.pack(side=tk.LEFT, expand=True)

        self.button6 = tk.Button(frame2, text="Button 06", bg='green')
        self.button6.pack(side=tk.LEFT)

        # Yet another one
        frame3 = tk.Frame(master, bg='blue')
        frame3.pack(fill=tk.X, expand=True)

        self.button7 = tk.Button(frame3, text="Button 07", bg='green')
        self.button7.pack(side=tk.LEFT)

        self.button8 = tk.Button(frame3, text="Button 08", bg='green')
        self.button8.pack(side=tk.LEFT)

        self.button9 = tk.Button(frame3, text="Button 09", bg='green')
        self.button9.pack(side=tk.LEFT)

        # Yet another one
        frame4 = tk.Frame(master, bg='yellow')
        frame4.pack(fill=tk.BOTH, expand=True, padx=20)

        self.button10 = tk.Button(frame4, text="Button 10", bg='green')
        self.button10.pack(side=tk.LEFT, ipadx=30)

        self.button11 = tk.Button(frame4, text="Button 11", bg='green')
        self.button11.pack(side=tk.LEFT, padx=40)

        self.button12 = tk.Button(frame4, text="Button 12", bg='green')
        self.button12.pack(side=tk.LEFT)

        # Yet another one
        frame5 = tk.Frame(master)
        frame5.pack(fill=tk.BOTH)

        self.quitbutton = tk.Button(frame5, text="QUIT", command=self.quit)
        self.quitbutton.pack(side=tk.LEFT, expand=True)

        dont = tk.Button(frame5, text="DON'T PRESS ME", command=self.dont_do_it)
        dont.pack(side=tk.LEFT, expand=True)

        self.shout = 'I TOLD YOU NOT TO DO THAT'.split(' ')
        self.shoutbuttons = [(self.button1, 'Button 01'),
                             (self.button3, 'Button 03'),
                             (self.button4, 'Button 04'),
                             (self.button5, 'Button 05'),
                             (self.button9, 'Button 09'),
                             (self.button10, 'Button 10'),
                             (self.button11, 'Button 11')]
        self.shout_index = 0

    def quit(self):
        ans = messagebox.askokcancel('Verify exit', "Really quit?")
        if ans:
            self._master.destroy()

    # An example of refactoring.
    # def dont_do_it(self):
    #     """An example using timer events - after 500 milliseconds this
    #     function is called.
    #     """
    #
    #     i = self.shout_index
    #     if i == 7:
    #         # got to the end - reset the last button and index
    #         button, text = self.shoutbuttons[i - 1]
    #         button.configure(bg='green', fg='black', text=text)
    #         self.shout_index = 0
    #     elif i == 0:
    #         # just started - change the first button
    #         button, text = self.shoutbuttons[i]
    #         button.configure(bg='red', fg='yellow', text=self.shout[i])
    #         self.shout_index += 1
    #         # after 500ms call self.dont_do_it
    #         self._master.after(500, self.dont_do_it)
    #     else:
    #         # reset the previous button and change the next button
    #         previous_button, previous_text = self.shoutbuttons[i - 1]
    #         previous_button.configure(bg='green', fg='black',
    #                                   text=previous_text)
    #         button, text = self.shoutbuttons[i]
    #         button.configure(bg='red', fg='yellow', text=self.shout[i])
    #         self.shout_index += 1
    #         self._master.after(500, self.dont_do_it)

    def dont_do_it(self):
        """An example using timer events - after 500 milliseconds this
        function is called.
        """

        i = self.shout_index
        if i != 0:
            # reset the previous button and change the next button
            previous_button, previous_text = self.shoutbuttons[i - 1]
            previous_button.configure(bg='green', fg='black',
                                      text=previous_text, height=1, width=0)

        if i == len(self.shoutbuttons):
            self.shout_index = 0
        else:
            # change current button
            button, text = self.shoutbuttons[i]
            button.configure(bg='red', fg='yellow', text=self.shout[i],
                             width=20, height=5)
            self.shout_index += 1
            self._master.after(500, self.dont_do_it)


def main():
    root = tk.Tk()
    app = DemoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
