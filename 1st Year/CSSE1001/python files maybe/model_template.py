import random
CLOSE = 40
STEP_DELTA = 10

def close_to(p1, p2):
    """(bool) Returns True iff 'p1' is sufficiently
    close to 'p2'.

    Both 'p1' & 'p2' are coordinate pairs.
    """
    
    x1, y1 = p1
    x2, y2 = p2
    return (x2 - x1) ** 2 + (y2 - y1) ** 2 < CLOSE ** 2

class GameObject:
    def __init__(self, name, x, y):
        self._x = x
        self._y = y
        self._name = name

    def get_position(self):
        return self._x, self._y

    def get_name(self):
        return self._name

class Character(GameObject):        
    def update_health(self, change):
        self._health += change

    def update_armour(self, change):
        self._armour += change

    def move(self, dx, dy):
        """Move player by (dx, dy) in the x, y direction"""
        self._x += dx
        self._y += dy

class Player(Character):
    """A player in the game"""
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        
        #TODO: remove magic values
        self._health = 100
        self._armour = 100

        self._inventory = []

    def get_inventory(self):
        return self._inventory

class Monster(Character):
    """A monster in the game"""
    def __init__(self, name, x, y):
        super().__init__(name, x, y)

        self._health = 100
        self._armour = 0

    def step(self):
        #TODO: move monster accordion
        pass

class Weapon(GameObject):
    """A weapon to attack monsters in the game"""
    def __init__(self, name, x, y):
        super().__init__(name, x, y)

        self._damage = 20
        self._taken = False

    def is_taken(self):
        self._taken = True

    def drop(self):
        self._taken = False

def main():
    pass

if __name__ == "__main__":
    main()



