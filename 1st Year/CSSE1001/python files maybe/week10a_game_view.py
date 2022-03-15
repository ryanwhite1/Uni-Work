"""Display components for a simple room-based game."""

__author__ = "Richard Thomas"
__date__ = "08/05/2018"
__copyright__ = "The University of Queensland, 2018"


import tkinter as tk
import week10a_game_model as model


class RoomView(tk.Canvas) :
    """Canvas to display a room."""
    
    def __init__(self, master, room) :
        """
        Parameters:
            master (Tk): Main window for application.
            room (Room): Model of the room and its contents.
        """
        super().__init__(master, bg='white',
                         width=room.get_width(),
                         height=room.get_height())
        self._room = room
        self._contents = []
        self.draw()

    def draw(self) :
        """Draw the contents of the room in the canvas."""
        self._contents = []
        self.delete(tk.ALL)
        for item in self._room.get_items() :
            self._contents.append(self.create_image(item.get_position().get_x_coord(),
                                                    item.get_position().get_y_coord(),
                                                    image=item.get_img(),
                                                    anchor=tk.NW))


class PlayerMoveent(object):
    def __init__(self, player):
        self._player = player
        self._player.set_direction(model.Player.STOP)

    def left(self):
        self._player.set_direction(model.Player.LEFT)

    def right(self):
        self._player.set_direction(model.Player.RIGHT)

    def up(self):
        self._player.set_direction(model.Player.UP)

    def right(self):
        self._player.set_direction(model.Player.RIGHT)

    def stop(self):
        self._player.set_direction(model.Player.STOP)


class ControlsFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self._controller = controller
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X)
        middle_frame = tk.Frame(self)
        middle_frame.pack(fill=tk.X)
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill=tk.X)

        tk.Button(top_frame, text="Up", command=self.controller.up).pack(side=tk.TOP,
                                                                         fill = tk.X)
        tk.Button(middle_frame, text="Left", command=self.controller.left).pack(side=tk.TOP,
                                                                         fill = tk.X)
        tk.Button(middle_frame, text="Stop", command=self.controller.stop).pack(side=tk.TOP,
                                                                         fill = tk.X)
        tk.Button(middle_frame, text="Right", command=self.controller.right).pack(side=tk.TOP,
                                                                         fill = tk.X)
        tk.Button(bottom_frame, text="Down", command=self.controller.down).pack(side=tk.TOP,
                                                                         fill = tk.X)
        
        

class GameApp(object) :
    """Main game application window."""
    def __init__(self, master) :
        master.title("Game")
        self._master = master
        self._game = model.GameModel()
        self._movement = PlayerMovement(self._game.get_player())
        self._controls = ControlsFrame(master, self._movement)
        self._controls.pack(side=tk.LEFT)
        self._room_view = RoomView(master, self._game.get_room())
        self._room_view.pack()
        self.step()

    def step(self):
        self._game.step()
        self._room_view.draw()
        self._master.after(30, self.step)



def main() :
    root = tk.Tk()
    game = GameApp(root)
    root.mainloop()


if __name__ == "__main__" :
    main()
