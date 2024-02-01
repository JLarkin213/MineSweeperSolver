from tkinter import *

from game.controller.controller import Controller

minesweeper = Controller()
minesweeper.config.set_to_beginner()
minesweeper.config.mines = 4
minesweeper.start_for_normal_user()
