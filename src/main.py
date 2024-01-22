from tkinter import *

from minesweeper.controller.controller import Controller

minesweeper = Controller()
minesweeper.config.set_to_intermediate()
minesweeper.close_windows()
minesweeper.start()

minesweeper.new_game()
