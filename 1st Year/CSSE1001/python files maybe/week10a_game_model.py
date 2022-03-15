"""Logical model for a simple room-based game."""

__author__ = "Richard Thomas"
__date__ = "08/05/2018"
__copyright__ = "The University of Queensland, 2018"


import tkinter as tk


X_COORD = 0
Y_COORD = 1
WIDTH = 0
HEIGHT = 1


class RoomPosition(object) :
    """Positoin and size of an item in a room."""

    def __init__(self, position, size) :
        """
        Parameters:
            position (tuple): X & Y coordinates of the position.
            size (tuple): Width & height of the item.
        """
        self._x_coord = position[X_COORD]
        self._y_coord = position[Y_COORD]
        self._width = size[WIDTH]
        self._height = size[HEIGHT]

    def move_left(self) :
        self._x_coord -= 1

    def move_right(self) :
        self._x_coord += 1

    def move_up(self) :
        self._y_coord -= 1

    def move_down(self) :
        self._y_coord += 1

    def get_x_coord(self) :
        return self._x_coord

    def get_y_coord(self) :
        return self._y_coord


class GameObject(object) :
    """An object that can be placed in a room."""

    def __init__(self, room_position, description, img_file) :
        """
        Parameters:
            room_position (RoomPosition): Object's position and size.
            description (str): Description of the object.
            img_file (str): Name of file containing graphical representation.
        """
        self._position = room_position
        self._description = description
        self._img = tk.PhotoImage(file=img_file)  # Load image.

    def get_img(self) :
        return self._img

    def get_position(self) :
        return self._position


class Player(GameObject) :
    """A player character that can interact with the game."""

    # Player movement constants.
    STOP = "Stop"
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"
    
    def __init__(self, room_position, description, img_file) :
        """
        Parameters:
            room_position (RoomPosition): Object's position and size.
            description (str): Description of the object.
            img_file (str): Name of file containing graphical representation.
        """
        super().__init__(room_position, description, img_file)
        self._score = 0
        self._direction = Player.STOP

    def set_direction(self, direction) :
        """Change the direction in which the player is moving.
        Parameters:
            direction (str): One of the Player movement constants.
        """
        self._direction = direction

    def step(self) :
        """Single time-based movement in the game."""
        if self._direction == Player.LEFT :
            self.get_position().move_left()
        elif self._direction == Player.RIGHT :
             self.get_position().move_right()
        elif self._direction == Player.UP :
            self.get_position().move_up()
        elif self._direction == Player.DOWN :
            self._position.move_down()
        # else direction is stop so don't move.
           
        
    

class Room(object) :
    """A room in which items can be placed."""

    def __init__(self, size) :
        """
        Parameters:
            size (tuple): Width and height of the room.
        """
        self._size = size
        self._contents = []

    def add_item(self, item) :
        """Add an item to the room.
        Parameters:
            item (GameObject): Item placed into the room.
        """
        self._contents.append(item)

    def get_items(self) :
        return self._contents

    def get_width(self) :
        return self._size[WIDTH]

    def get_height(self) :
        return self._size[HEIGHT]

    def step():
        pass


class GameModel(object):
    def __init__(self):
        self._current_room = Room((1000, 800))
        position = RoomPosition((10, 10), (45, 67))
        self._player = Player(position, "Player", "week10_images/player.gif")
        self._current_room.add_item(self._player)

    def step(self):
        self._player.step()
        self._current_room.step()
