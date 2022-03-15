
import tkinter as tk
import week10_1 as model

class RoomView(tk.Canvas):
    def __init__(self, master, room):
        super().__init__(master, bg='white',
                         width = room.get_width(),
                         height = room.get_height())
        self._room = room
        self._contents = []
        self.redraw()

    def redraw(self):
        self._contents = []
        self.delete(tk.ALL)
        for item in self._room.get_items():
            self._contents.append(self.create_image(item.get_position().get_x_coord(),
                                                    item.get_position().get_y_coord(),
                                                    image=item.get_img(),
                                                    anchor=tk.NW))


class GameApp(object):
    def __init__(self, master):
        master.title("Game")
        self._master = master
        room = model.Room((1000,800))
        position = model.RoomPosition((110,10), (45, 67))
        player = model.Player(position, "Player", "GUI4/images/player.gif")
        self._room_view = RoomView(master, room)
        self._room_view.pack()

def main():
    root = tk.Tk()
    game = GameApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    

            
