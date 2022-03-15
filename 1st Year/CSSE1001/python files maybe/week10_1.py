
import tkinter as tk


class RoomPosition(object):
    """A location in a room, plus size of item."""

    def __init__(self, position, size):
        self._x_coord = position[0]
        self._y_coord = position[1]
        self._width = size[0]
        self._height = size[1]

    def move_left(self):
        self._x_coord -= 1

    def move_right(self):
        self._x_coord += 1

    def move_up(self):
        self._y_coord += 1

    def move_down(self):
        self._y_coord -= 1

    def get_x_coord(self):
        return self._x_coord

    def get_y_coord(self):
        return self._y_coord
        

class GameObject(object):
    """An object in a room in the game."""

    def __init__(self, room_position, description, img_file):
        """
        Parameters:
            room_position : Where I am in the room.
            description (str): What I am.
            img_file (str): Name of the file containing the representation.
        """
        self._position = position
        self._decription = description
        self._img = tk.PhotoImage(file = img_file)

    def get_img(self):
        return self._img

    def get_position(self):
        return self._position


class Player(GameObject):
    
    STOP = "Stop"
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"
    
    def __init__(self, room_position, description, img_file):
        super().__init__(room_position, description, img_file)
        self._score = 0
        self._direction = Player.STOP

    def set_direction(self, direction):
        self._direction = direction

    def step(self):
        if self._direction == Player.LEFT:
            self._position.move_left()
        elif self._direction == Player.RIGHT:
            self._position.move_right()
        elif self._direction == Player.UP:
            self._position.move_up()
        elif self._direction == Player.DOWN:
            self._position.move_down()
    


class Room(object):
    """A room items can be placed in."""

    def __init__(self, size):
        """
        Parameters:
            size (tuple): Width and height of the room.
        """
        self._size = size
        self._contents = []

    def add_item(self, item):
        self._contents.append(item)

    def get_items(self):
        return self._contents

    def get_width(self):
        return self._size[0]

    def get_height(self):
        return self._size[1]
