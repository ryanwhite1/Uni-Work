import tkinter as tk
import math

from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import Toplevel
from tkinter import *

from model import TowerGame
from tower import AbstractTower, SimpleTower, MissileTower, PulseTower
from enemy import SimpleEnemy
from utilities import Stepper, rotate_toward, angle_between
from view import GameView
from level import AbstractLevel
from range_ import CircularRange
from high_score_manager import HighScoreManager
from advanced_view import TowerView

BACKGROUND_COLOUR = "#4a2f48"

__author__ = "Ryan White, 44990392"
__copyright__ = ""


# Could be moved to a separate file, perhaps levels/simple.py, and imported
class MyLevel(AbstractLevel):
    """A simple game level containing examples of how to generate a wave"""
    waves = 30

    def get_wave(self, wave):
        """Returns enemies in the 'wave_n'th wave

        Parameters:
            wave_n (int): The nth wave

        Return:
            list[tuple[int, AbstractEnemy]]: A list of (step, enemy) pairs in the
                                             wave, sorted by step in ascending order 
        """
        enemies = []

        if wave == 1:
            # A hardcoded singleton list of (step, enemy) pairs

            enemies = [(10, SimpleEnemy())]
        elif wave == 2:
            # A hardcoded list of multiple (step, enemy) pairs

            enemies = [(10, SimpleEnemy()), (15, SimpleEnemy()), (30, SimpleEnemy())]
        elif 3 <= wave < 10:
            # List of (step, enemy) pairs spread across an interval of time (steps)

            steps = int(40 * (wave ** .5))  # The number of steps to spread the enemies across
            count = wave * 2  # The number of enemies to spread across the (time) steps

            for step in self.generate_intervals(steps, count):
                enemies.append((step, SimpleEnemy()))

        elif wave == 10:
            # Generate sub waves
            sub_waves = [
                # (steps, number of enemies, enemy constructor, args, kwargs)
                (50, 10, SimpleEnemy, (), {}),  # 10 enemies over 50 steps
                (100, None, None, None, None),  # then nothing for 100 steps
                (50, 10, SimpleEnemy, (), {})  # then another 10 enemies over 50 steps
            ]

            enemies = self.generate_sub_waves(sub_waves)

        elif 11 <= wave <= 20:
            # Now it's going to get hectic

            sub_waves = [
                (
                    int(13 * wave),  # total steps
                    int(25 * wave ** (wave / 50)),  # number of enemies
                    SimpleEnemy,  # enemy constructor
                    (),  # positional arguments to provide to enemy constructor
                    {},  # keyword arguments to provide to enemy constructor
                ),
                (
                    int(15 * wave),
                    int(2 ** (wave / 5)),
                    SteelEnemy,
                    (),
                    {},
                )
            ]
            enemies = self.generate_sub_waves(sub_waves)

        else:
            sub_waves = [
                (
                    int(13 * wave),  
                    int(25 * wave ** (wave / 65)),  
                    SimpleEnemy,  
                    (),  
                    {},  
                ),
                (
                    int(10 * wave),  
                    int(2 * wave ** (wave / 50)),  
                    SteelEnemy,  
                    (), 
                    {},  
                ),
                (
                    int(15 * wave), 
                    int(10 * wave ** (wave / 30)),  
                    SimpleEnemy,  
                    (),  
                    {},  
                )
            ]
            enemies = self.generate_sub_waves(sub_waves) 

        return enemies

class EnergyTower(SimpleTower):
    """
    An intermediate tower with medium range that rotates toward enemies, dealing energy damage.
    """
    name = 'Energy Tower'
    colour = '#FFD700'  # Gold standard 

    range = CircularRange(3)
    cool_down_steps = 1

    base_cost = 40
    level_cost = 30

    rotation_threshold = (1 / 12) * math.pi

    def __init__(self, cell_size: int, grid_size=(.8, .8), rotation=math.pi * .25,
                 base_damage=4, level: int = 1):
        """
        Creates the tower with values specified
        """
        super().__init__(cell_size, grid_size, rotation, base_damage, level)

    def step(self, data):
        """Rotates toward 'target' and attacks if possible"""
        self.cool_down.step()

        target = self.get_unit_in_range(data.enemies)

        if target is None:
            return

        angle = angle_between(self.position, target.position)
        partial_angle = rotate_toward(self.rotation, angle, self.rotation_threshold)
        self.rotation = partial_angle

        if partial_angle == angle:
            target.damage(self.get_damage(), 'energy')
    

class SteelEnemy(SimpleEnemy):
    """
    Enemy resistant to projectile and explosive damage.
    """
    name = "Steel Enemy"
    colour = "#000000"      # as black as my coffee

    points = 30
    
    def __init__(self, grid_size=(.6, .6), grid_speed=2/60, health=400):
        """
        Imports necessary parameters for enemy construction. 
        """
        super().__init__(grid_size, grid_speed, health)

    def damage(self, damage, type_):
        """
        Inflicts damage on the enemy

        Parameters:
            damage (int): the amount of damage to be inflicted
            type_ (str): the type of damage to inflict
        """
        # damage only inflicted unless not explosive or projectile
        if type_ == "explosive":
            return
        elif type_ == "projectile":
            return
        else:
            self.health -= 0.5 * damage
            if self.health < 0:
                self.health = 0

class StatusBar(tk.Frame):
    """
    Creates a frame showing all relevant game variables to the user. 
    """
    def __init__(self, master):
        """
        Creates all labels, displays, etc.
        
        Parameter:
            master (tk.Frame): The frame to create the Status Bar in. 
        """
        self._master = master

        status_bar = tk.Frame(self._master, bg="white")     # frame containing all statusbar widgets
        status_bar.pack(side=tk.TOP, fill=tk.X)

        # displays waves, updates based on set_wave function
        self._wave_display = tk.Label(status_bar, bg="white")
        self._wave_display.pack(side=tk.TOP)

        # displays score, updates by set_score
        self._score_display = tk.Label(status_bar, bg="white")
        self._score_display.pack(side=tk.TOP)

        # handles the coin display, including image
        self.coins = tk.PhotoImage(file="images/coins.gif")
        coin_image = tk.Label(status_bar, image=self.coins, bg="white")
        coin_image.pack(side=tk.LEFT)
        self._coin_display = tk.Label(status_bar, bg="white")
        self._coin_display.pack(side=tk.LEFT, fill=tk.Y)

        # handles lives display, including image
        self.heart = tk.PhotoImage(file="images/heart.gif")
        heart_image = tk.Label(status_bar, image=self.heart, bg="white")
        heart_image.pack(side=tk.LEFT)
        self._lives_display = tk.Label(status_bar, bg="white")
        self._lives_display.pack(side=tk.LEFT)

    # following functions update respective widgets by configuring the labels
    def set_wave(self, wave, level):
        """
        Sets the current wave in the wave status widget.

        Parameters:
            wave (int): The current wave.
            level (int): The maximum wave number.
        """
        self._wave_display.config(text = "Wave: " + str(wave) + "/" + str(level))

    def set_score(self, score):
        """
        Sets the score widget to the current score.

        Parameter:
            score (int): The score to set the widget to.
        """
        self._score_display.config(text = "Score: " + str(score))

    def set_coins(self, coins):
        """
        Sets the coins widget to the current coins.

        Parameter:
            coins (int): The coin value to set the widget to.
        """
        self._coin_display.config(text = str(coins) + " Coins")

    def set_lives(self, lives):
        """
        Sets the lives widget to the current lives.

        Parameter:
            lives (int): The number of lives to set the widget to.
        """
        self._lives_display.config(text = str(lives) + " Lives")

class ShopTowerView(tk.Frame):
    """
    Shop GUI for purchasing different Tower types. 
    """
    def __init__(self, master, tower, tower_list, bg, highlight, click_command):
        """
        Construct a shop view to the right of the game.

        Parameters:
            master (tk.Tk): Window to place the shop into.
            tower (AbstractTower): The tower type.
            tower_list (list): A list of the tower types being used with their respective ShopTowerView classes, and a boolean parameter if they're highlighted. 
            bg (str): The desired background colour.
            highlight (str): The desired highlight colour.
            click_command (lambda): The command when Button 1 is activated.
        """
        super().__init__(master)
        self._master = master
        self._bg = bg
        self._highlight = highlight
        self._click_command = click_command
        self._tower = tower
        self._tower_list = tower_list

        # creates the shop item, complete with tower icon
        self._shop_item = tk.Frame(self._master, bg=self._bg)
        self._shop_item.pack(fill=tk.X)
        
        self._canvas = tk.Canvas(self._shop_item, width=self._tower.cell_size, height=self._tower.cell_size, bg=self._bg)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH)

        # draws tower on a canvas
        tower.position = (self._tower.cell_size / 2, self._tower.cell_size / 2)  # Position in centre
        tower.rotation = 3 * math.pi / 2  # Point up
        TowerView.draw(self._canvas, self._tower)

        # creates labels for tower name and tower cost
        self._tower_name = tk.Label(self._shop_item, text=self._tower.name, bg=self._bg, fg="red")
        self._tower_name.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._tower_cost = tk.Label(self._shop_item, text=str(self._tower.get_value()) + " coins",
                                    bg=self._bg, fg="red")
        self._tower_cost.pack(side=tk.BOTTOM)

        # binds left click to all relevant shop GUI
        self._shop_item.bind("<Button-1>", self._select_tower)
        self._canvas.bind("<Button-1>", self._select_tower)
        self._tower_name.bind("<Button-1>", self._select_tower)
        self._tower_cost.bind("<Button-1>", self._select_tower)
        
    def _set_available(self):
        """
        Sets the tower type as available (to place).
        """
        self._tower_name.config(fg="black")
        self._tower_cost.config(fg="black")

    def _set_unavailable(self):
        """
        Sets the tower type as unavailable (to place).
        """
        self._tower_name.config(fg="red")
        self._tower_cost.config(fg="red")

    def _select_tower(self, event):
        """
        Runs the left click command (specified in __init__ initialisation). Selects the clicked on tower. 

        Parameter:
            event (tk.Event): A dummy variable that is not used. 
        """
        self._click_command()
        self._toggle_highlight()

    def _toggle_highlight(self):
        """
        Updates all of the shop items to highlight only the selected tower item.
        """
        for tower_instance in self._tower_list:
            if tower_instance[0].name == self._tower.name:      # if the tower matches the shop item, will highlight
                if not tower_instance[2]:       # if the item is not highlighted.
                    self.set_shop_colour(self, self._highlight)
                    tower_instance[2] = True
            else:       # sets all other tower shop colours to the background colour
                self.set_shop_colour(tower_instance[1], self._bg)
                tower_instance[2] = False

    def set_shop_colour(self, shop_instance, colour):
        """
        Sets the background colours of a shop instance to the specified colour.

        Parameters:
            shop_instance (ShopTowerView): The location of the shop widgets. Use 'self' if using in own class.
            colour (str): The colour to set the widgets.
        """
        shop_instance._shop_item.config(bg=colour)
        shop_instance._canvas.config(bg=colour)
        shop_instance._tower_name.config(bg=colour)
        shop_instance._tower_cost.config(bg=colour)

class TowerGameApp(Stepper):
    """Top-level GUI application for a simple tower defence game"""

    # All private attributes for ease of reading
    _current_tower = None
    _paused = False
    _won = None

    _level = None
    _wave = None
    _score = None
    _coins = None
    _lives = None

    _master = None
    _game = None
    _view = None

    def __init__(self, master: tk.Tk, delay: int = 20):
        """Construct a tower defence game in a root window

        Parameters:
            master (tk.Tk): Window to place the game into
        """

        self._master = master
        super().__init__(master, delay=delay)

        self._game = game = TowerGame()

        self.high_scores = HighScoreManager()

        self.setup_menu()

        master.title("Tower Defence Game")

        # create a game view and draw grid borders
        self._view = view = GameView(master, size=game.grid.cells,
                                     cell_size=game.grid.cell_size,
                                     bg='antique white')
        view.pack(side=tk.LEFT, expand=True)

        # Instantiates status bar
        self._info_bar = tk.Frame(self._master, bg="white")
        self._info_bar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self._statusbar = StatusBar(self._info_bar)
    
        # Instantiates control widgets
        self._control_frame = tk.Frame(self._info_bar)
        self._control_frame.pack(side = tk.BOTTOM)

        self._btn_nextwave = tk.Button(self._control_frame, text="Next Wave",
                                       command = self.next_wave)
        self._btn_nextwave.pack(side=tk.LEFT)

        self._btn_play = tk.Button(self._control_frame, text="Play",
                                   command = self._toggle_paused)
        self._btn_play.pack(side=tk.LEFT)

        # All playable towers:
        self._game_towers = [SimpleTower,
                             EnergyTower,
                             PulseTower,
                             MissileTower
                             ]

        self._shop = tk.Frame(self._info_bar, bg="white")
        self._shop.pack(fill=tk.X)

        # Create views for each tower & store to update if availability changes
        self._tower_views = []
        for tower_class in self._game_towers:
            self._highlighted = False
            self._tower = tower_class(self._game.grid.cell_size // 2)

            self._shop_instance = ShopTowerView(self._shop, self._tower, self._tower_views, bg="white", highlight="#FFFF99",
                                 click_command=lambda class_=tower_class: self.select_tower(class_))
            self._shop_instance.pack(fill=tk.BOTH)
            self._tower_views.append([self._tower, self._shop_instance,
                                      self._highlighted]) # Can use to check if tower is affordable when refreshing view
            
        # bind game events
        game.on("enemy_death", self._handle_death)
        game.on("enemy_escape", self._handle_escape)
        game.on("cleared", self._handle_wave_clear)

        # Task 1.2 (Tower Placement): bind mouse events to canvas here
        self._view.bind("<Button-1>", self._left_click)
        self._view.bind("<Motion>", self._move)
        self._view.bind("<Leave>", self._mouse_leave)
        self._view.bind("<Button-3>", self._right_click)

        # Level
        self._level = MyLevel()

        view.draw_borders(game.grid.get_border_coordinates())

        # Get ready for the game
        self._setup_game()
        self._towers = {}     

    def setup_menu(self):
        """Sets up the application menu"""
        # Constructs file menu with menu options
        dropdown = tk.Menu(self._master)
        self._master.config(menu=dropdown)

        filemenu = tk.Menu(dropdown)
        dropdown.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Game", command = self._new_game)
        filemenu.add_command(label="High Scores", command = self._high_score_display)
        filemenu.add_command(label="Exit", command = self._exit)

        # if the window is closed, runs exit command
        self._master.protocol("WM_DELETE_WINDOW", self._exit)
        

    def _toggle_paused(self, paused=None):
        """Toggles or sets the paused state

        Parameters:
            paused (bool): Toggles/pauses/unpauses if None/True/False, respectively
        """
        if paused is None:
            paused = not self._paused

        # Reconfigures the pause button
        if paused:
            self._btn_play.config(text="Play")
            self.pause()
        else:
            self._btn_play.config(text="Pause")
            self.start()

        self._paused = paused

    def _setup_game(self):
        """Sets up the game"""
        self._wave = 0
        self._score = 0
        self._coins = 75
        self._lives = 20

        self._won = False

        # Updates status bar
        self._statusbar.set_wave(self._wave, self._level.get_max_wave())
        self._statusbar.set_score(self._score)
        self._statusbar.set_coins(self._coins)
        self._update_availability()
        self._statusbar.set_lives(self._lives)

        # Re-enables the play controls 
        self._btn_nextwave.config(state = "normal")
        self._btn_play.config(state = "normal")

        self._game.reset()

        # Auto-start the first wave
        self.next_wave()
        self._toggle_paused(paused=True)

    # Task 1.4 (File Menu): Complete menu item handlers here (including docstrings!)
    def _new_game(self):
        """
        Resets the game to a blank canvas with initial widget values.
        """
        self._setup_game()
        self.refresh_view()
    
    def _exit(self):
        """
        Asks the user whether they actually want to quit. Quits if answer is yes.
        """
        leave = messagebox.askquestion("Exit", "Are you sure that you want to quit?", icon = "warning")
        if leave == "yes":
            self._master.destroy()

    def refresh_view(self):
        """Refreshes the game view"""
        if self._step_number % 2 == 0:
            self._view.draw_enemies(self._game.enemies)
        self._view.draw_towers(self._game.towers)
        self._view.draw_obstacles(self._game.obstacles)
        self._update_availability()

    def _step(self):
        """
        Perform a step every interval

        Triggers a game step and updates the view

        Returns:
            (bool) True if the game is still running
        """
        self._game.step()
        self.refresh_view()

        return not self._won

    def _update_availability(self):
        """
        Updates the shop to show which towers are available or otherwise. 
        """
        for tower_instance in self._tower_views:
            if self._coins >= tower_instance[0].get_value():
                tower_instance[1]._set_available()
            else:
                tower_instance[1]._set_unavailable()

    # Task 1.2 (Tower Placement): Complete event handlers here (including docstrings!)
    def _move(self, event):
        """
        Handles the mouse moving over the game view canvas

        Parameter:
            event (tk.Event): Tkinter mouse event
        """
        if self._current_tower == None:
            return

        # move the shadow tower to mouse position
        position = event.x, event.y
        self._current_tower.position = position

        legal, grid_path = self._game.attempt_placement(position)

        # find the best path and covert positions to pixel positions
        path = [self._game.grid.cell_to_pixel_centre(position)
                for position in grid_path.get_shortest()]

        # if tower is unavailable, displays a cross and no enemy path
        if self._current_tower.get_value() > self._coins:
            legal = False
        else:
            self._view.draw_path(path)

        self._view.draw_preview(self._current_tower, legal)

    def _mouse_leave(self, event):
        """
        Handles the cursor moving outside of the GameView canvas.

        Parameter:
            event (tk.Event): Tkinter mouse event
        """
        # Deletes the preview on the game canvas
        self._view.delete('path', 'range', 'shadow')

    def _left_click(self, event):
        """
        Handles the user pressing the left mouse button inside the GameView canvas.

        Parameter:
            event(tk.Event): Tkinter mouse event
        """
        if self._current_tower is None:
            return
        elif self._current_tower.get_value() > self._coins:
            return

        position = event.x, event.y
        cell_position = self._game.grid.pixel_to_cell(position)

        # places tower if possible, updating widgets and drawing the tower
        if self._game.place(cell_position, tower_type=self._current_tower.__class__):
            self._coins -= self._current_tower.get_value()
            self._statusbar.set_coins(self._coins)
            self._update_availability()
            self._view.draw_towers(self._game.towers) 

    def _right_click(self, event):
        """
        Handles the user right clicking on a cell inside GameView.
        If a tower is at the event location, tower will be sold.

        Parameter:
            event(tk.Event): Tkinter mouse event
        """
        position = event.x, event.y
        cell_position = self._game.grid.pixel_to_cell(position)

        # tries to remove a tower at click location. If no tower, nothing happens
        try:
            self._coins += int(0.8 * self._game.towers[cell_position].get_value())
            self._update_availability()
            self._statusbar.set_coins(self._coins)
            self._game.remove(cell_position)
            self._view.draw_towers(self._game.towers)
        except:
            return

    def next_wave(self):
        """Sends the next wave of enemies against the player"""
        if self._wave == self._level.get_max_wave():
            return

        self._wave += 1

        # Updates the current wave display
        self._statusbar.set_wave(self._wave, self._level.get_max_wave())

        # Disables the add wave button (if this is the last wave)
        if self._wave == self._level.get_max_wave():
            self._btn_nextwave.config(state = "disabled")

        # Generates wave and enqueue
        wave = self._level.get_wave(self._wave)
        for step, enemy in wave:
            enemy.set_cell_size(self._game.grid.cell_size)

        self._game.queue_wave(wave)

    def select_tower(self, tower):
        """
        Set 'tower' as the current tower

        Parameters:
            tower (AbstractTower): The new tower type
        """
        self._current_tower = tower(self._game.grid.cell_size)

    def _high_score_display(self):
        """
        Displays the high score list as a popup window.
        """
        # loads high score data and organises it according to layout
        row = ''
        self.counter = 1
        entries = self.high_scores.get_entries()
        for entry in entries:
            row += "#" + str(self.counter) + ": \n"     # first line is position on scoreboard
            self.counter += 1
            for classifier in entry:
                if classifier == "name":
                    row += "Name: " + str(entry[classifier]) + "\n"     # second line is name associated with score
                if classifier == "score":
                    row += "Score: " + str(entry[classifier]) + "\n\n"      # third line is score

        # creates the high score popup
        self._high_score_window = tk.Toplevel(self._master)
        self._display = tk.Label(self._high_score_window, text = row)
        self._display.pack()
        
    def _high_score_entry(self):
        """
        Prompts user input of name with a popup window. This is added to the respective high score.
        """
        # creates a popup box
        self._popup = tk.Toplevel(self._master)
        
        self._dialogue = tk.Label(self._popup, text = "Congratulations! You've made a high score. Please enter your name:")
        self._dialogue.pack(side=tk.TOP)

        # asks user to input their name
        self._input = tk.Entry(self._popup)
        self._input.pack(side=tk.TOP)

        self._enter = tk.Button(self._popup, text = "Add it!", command = self._clear_popup)
        self._enter.pack(side=tk.BOTTOM)

    def _clear_popup(self):
        """
        Destroys the popup window, first adding the user's high score to the dictionary.
        """
        user_id = self._input.get()

        # adds score and associated name to high_scores list
        self.high_scores.add_entry(user_id, self._score)
        self.high_scores.save()
        
        self._popup.destroy()
        
    def _handle_death(self, enemies):
        """
        Handles enemies dying

        Parameters:
            enemies (list<AbstractEnemy>): The enemies which died in a step
        """
        bonus = len(enemies) ** .5
        for enemy in enemies:
            self._coins += enemy.points
            self._score += int(enemy.points * bonus)

        # Updates coins & score displays
        self._statusbar.set_coins(self._coins)
        self._statusbar.set_score(self._score)

    def _handle_escape(self, enemies):
        """
        Handles enemies escaping (not being killed before moving through the grid

        Parameters:
            enemies (list<AbstractEnemy>): The enemies which escaped in a step
        """
        self._lives -= len(enemies)
        if self._lives < 0:
            self._lives = 0

        # Updates lives display
        self._statusbar.set_lives(self._lives)

        # Handle game over
        if self._lives == 0:
            self._handle_game_over(won=False)

    def _handle_wave_clear(self):
        """Handles an entire wave being cleared (all enemies killed)"""
        if self._wave == self._level.get_max_wave():
            self._handle_game_over(won=True)

    def _handle_game_over(self, won=False):
        """
        Handles game over, displaying a popup window with game outcome. 
        
        Parameter:
            won (bool): If True, signals the game was won (otherwise lost)
        """
        self._won = won
        self.stop()

        # disables control buttons
        self._btn_nextwave.config(state = "disabled")
        self._btn_play.config(state = "disabled")

        if self.high_scores.does_score_qualify(self._score):
            self._high_score_entry()
            
        # Shows game over dialog
        if self._won:
            messagebox.showinfo("Congratulations!", "You've won the game.")
        else:
            messagebox.showinfo("Ah poop.", "You've lost the game. I would say better luck next time, but it's not looking good.")

def main():
    """
    Runs the program in a new window. 
    """
    root = tk.Tk()
    game = TowerGameApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
