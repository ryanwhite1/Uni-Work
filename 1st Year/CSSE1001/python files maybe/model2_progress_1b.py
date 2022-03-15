"""CSSE1001, Semester 1, 2018

Modelling code from object-oriented programming example in week 7

Progress after first lecture, plus following changes:
    - Docstring comments added to all constants, classes, and methods
    - Comment added to highlight Character.__init__'s redundancy
    - Weapon.take renamed to Weapon.set_taken
    - Added get_delta_1/2d helper functions
    - Renamed close_to parameter p1 to point1; similarly for p2
    - 

"""

import random
CLOSE = 40  # The threshold
STEP_DELTA = 10  # The step size

def close_to(point1, point2):
    """(bool) Returns True iff 'point1' is sufficiently
    close to 'point2'.

    Both 'point1' & 'point2' are coordinate pairs.
    """
    
    x1, y1 = point1
    x2, y2 = point2
    return (x2 - x1) ** 2 + (y2 - y1) ** 2 < CLOSE ** 2

def get_delta_1d(point1, point2):
    """
    (int) Returns the amount to step toward point2 from point1 if they are
    not sufficiently close, else 0

    Parameters:
        point1 (int): The 1-dimensional coordinate to move from
        point2 (int): The 1-dimensional coordinate to move toward
    """
    if point1 > point2 + STEP_DELTA:
        return STEP_DELTA
    elif point1 < point2 - STEP_DELTA:
        return -STEP_DELTA
    else:
        return 0

def get_delta_2d(point1, point2):
    """
    (tuple<int, int>) Returns the amount to step toward point2 from point1 if
    they are not sufficiently close, else (0, 0)

    Parameters:
        point1 (tuple<int, int>): The 2-dimensional coordinate to move from
        point2 (tuple<int, int>): The 2-dimensional coordinate to move toward
    """
    close = close_to(point1, point2)

    if close:
        return (0, 0)

    dx = x2 - x1
    dy = y2 - y1
    magnitude = (dx ** 2 + dy ** 2) ** 0.5

    return (int(dx / magnitude * STEP_DELTA), int(dy / magnitude * STEP_DELTA))

class GameObject:
    """An object in the game"""
    def __init__(self, name, x, y):
        """Constructor

        Parameters:
            name (str): The name of this game object
            x (int): The game object's x position
            y (int): The game object's y position
        """
        self._x = x
        self._y = y
        self._name = name

    def get_position(self):
        """(int, int) Returns the (x, y) position of the game object"""
        return self._x, self._y

    def get_name(self):
        """(str) Returns the name of the game object"""
        return self._name

class Character(GameObject):
    """A character in the game with health and armour"""
    # # Note that __init__ does not need to be overridden, because it does
    # # nothing other than call the super method with the exact same arguments,
    # # which is the same as not defining it at all

    # def __init__(self, name, x, y):
    #     super().__init__(name, x, y)

    def move(self, dx, dy):
        """Move character by (dx, dy) in the (x, y) direction

        Parameters:
            dx (int): The amount to move in the positive x direction
            dy (int): The amount to move in the positive y direction
        """
        self._x += dx
        self._y += dy

    def get_health(self):
        """Returns the character's health"""
        return self._health

    def increase_health(self, change):
        """Increases the character's health by 'change'"""
        self._health += change

    def get_armour(self):
        """Returns the character's armour"""
        return self._armour

    def increase_armour(self, change):
        """Increases the character's armour by 'change'"""
        self._armour += change

    # TODO: health & armour getters
    
class Item(GameObject):
    """An item in the game"""
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self._taken = False

    def is_taken(self):
        """(bool) Returns True iff this weapon has been taken"""
        return self._taken

    # def take(self):
    #     """Take the weapon"""
    #     self._taken = True

    # def drop(self):
    #     """Drop the weapon"""
    #     self._taken = False

    def set_taken(self, taken=True):
        """Takes or drops the weapon

        Parameters:
            taken (bool): True iff the weapon should be taken, else False
        """
        self._taken = taken

    def set_postition(self, x, y):
        self._x = x
        self._y = y

    def use(self, character):
        """Use this item on the given character"""
        raise NotImplementedError("The use method must be implemented by a subclass")

    def __str__(self):
        return self._name
        

class Weapon(Item):
    """A weapon to attack monsters in the game"""
    def __init__(self, name, x, y, model):
        """Constructor

        Parameters:
            name (str): The name of this weapon
            x (int): The weapon's x position
            y (int): The weapon's y position
        """
        super().__init__(name, x, y)

        self._damage = 20



    # weapon = Weapon('sword1', 50, 100)
    # weapon.take() # -> taken = True
    # weapon.take(taken=False) # -> taken = False

    def use(self, character):
        for monster in self._model.get_monsters():
            if close_to(monster.get_position(), character.get_position()):
                monster.increase_healthy(-self._damage)


class Potion(Item):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self._strength = 40

    def use(self, character):
        character.increase_health(self._strength)
        self._strength = 0

class Player(Character):
    """A player in the game"""
    def __init__(self, name, x, y):
        """Constructor

        Parameters:
            name (str): The name of this player
            x (int): The player's x position
            y (int): The player's y position
        """
        super().__init__(name, x, y)

        # TODO: remove magic values
        self._health = 100
        self._armour = 100

        self._inventory = []
        self._holding = None

    def get_inventory(self):
        return self._inventory

    def take(self, item):
        """Adds an item to the player's inventory

        Parameter:
            item(Item): The item to add
        """
        self._inventory.append(item)

    def drop(self, index):
        """Removes the item at given index from the player;s inventory
        Does nothing if index is out of range"""
        if 0 <= index < len(self._inventory):
            item = self._inventory[index]
            if item == self._holding:
                self._holding = None
            return self._inventory.pop(index)

    def hold(self, index):
        """Makes the player hold the item at given index from their inventory
        Does nothing if index is out of range"""
        if 0 <= index < len(self._inventory):
            item = self._inventory[index]
            self._holding = item

    def get_holding(self):
        """(Item) Returns the item that the player is holding"""
        return self._holding

    def use(self):
        """Uses the item that the player is holding"""
        if self._holding is not None:
            self._holding.use(self)
            

class Monster(Character):
    """A monster in the game"""
    def __init__(self, name, x, y, model):
        """Constructor

        Parameters:
            name (str): The name of this monster
            x (int): The monster's x position
            y (int): The monster's y position
        """
        super().__init__(name, x, y)

        self._health = 100
        self._armour = 0

    def step(self):
        # TODO: move monster accordingly
        pass

    # TODO: attack method?

class Model:
    """A model of the game world"""
    def __init__(self):
        self._player = Player('Player', 50, 50)

        self._monsters = [
            Monster('balloon', 600, 50),
            #TrackingMonster(50, 400, 'purple'),
            #TipsyMonster(200, 300, 'triangle)
        ]

        self._items = [
            Weapon("sword", 400, 50)
            Potion("potion", 50, 400)
            Weapon("dagger", 600, 400)
        ]

    def get_player(self):
        return self._player

    def get_items(self):
        return self._items

    def get_monsters(self):
        """[Monster] Returns all living monsters in the game"""
        alive = []

        for monster in self._monsters:
            if monster.get_healthy() > 0:
                alive.append(monster)

        return alive

    def player_take_item(self):
        """Makes the player take the item that theya re close to, else nothing"""
        for item in self._items:
            if close_to(self._player.get_position(), item.get_position()) and not item.is_taken():
                self._player.take(item)
                item.set_taken()
                return
        



def main():
    player1 = Player('link', 50, 250)
    player2 = Player('fry', 10, 100)

    print(player1.get_name())
 

    #player1 = Player('link', 50, 250)
    #player2 = Player('fry', 10, 100)
    #
    #player1.get_position()


if __name__ == "__main__":
    main()

