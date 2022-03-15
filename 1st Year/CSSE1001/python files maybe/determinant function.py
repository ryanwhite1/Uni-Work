import tkinter
from tkinter import *

def determinant(a,b):
    a1 = (a[1]*b[2])-(a[2]*b[1])
    b1 = (a[0]*b[2])-(a[2]*b[0])
    c1 = (a[0]*b[1])-(a[1]*b[0])

    return (a1,-b1,c1)




top = tkinter.Tk()
label_a = Label(top, text = 'vector a')
label_a.pack(side = LEFT)
a = Entry(top)
a.pack(side = LEFT)
label_b = Label(top, text = 'vector b')
label_b.pack(side = RIGHT)
b = Entry(top)
b.pack(side = RIGHT)
butt = Button(top, command= determinant(a.get(), b.get()))
butt.pack(side = BOTTOM)



    
root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
