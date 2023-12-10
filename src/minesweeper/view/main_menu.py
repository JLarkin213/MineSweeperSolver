from tkinter import *

class MainMenu():
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("MINESWEEPER")
        self.root.geometry('400x400')

        self.current_row = 1

        self.add_title()
        self.add_instructions()
        self.add_buttons()
    
    def add_title(self):
        main_menu_label = Label(self.root, text = "Main Menu")
        main_menu_label.grid(row=self.current_row)
        self.current_row += 1

    def add_instructions(self):
        self.instructions = Label(self.root, text = "Select a level to play")
        self.instructions.grid(row=self.current_row, sticky="w")
        self.current_row += 1

    def add_buttons(self):
        self.beginner = Button(self.root, text = "Beginner", fg = "green")
        self.beginner.grid(row=self.current_row, sticky="w")
        self.current_row += 1

        self.intermediate = Button(self.root, text = "Intermediate")
        self.intermediate.grid(row=self.current_row, sticky="w")
        self.current_row += 1

        self.advanced = Button(self.root, text = "Advanced", fg = "red")
        self.advanced.grid(row=self.current_row, sticky="w")
        self.current_row += 1

        quit = Button(self.root, text = "QUIT", command=self.root.destroy)
        quit.grid(row=self.current_row, sticky="w")
        self.current_row += 1

    def update_instructions(self):
        self.instructions.configure(text = "Selecting a new level will close any current games")
