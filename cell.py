from tkinter import Button, Label
import settings
import random

# Creation of the Cell class to be the blocks in the field.
class Cell:
    # List of actions
    all = []
    # Global label for number of cells left.
    cell_count_label_obj = None
    # Creates the number of flags.
    num_flags = settings.MINES_COUNT
    # Defines the constructor to set values.
    def __init__(self, x, y,  is_mine=False):
        self.is_mine = is_mine
        self.is_open = False
        self.cell_btn_obj = None
        self.x = x
        self.y = y
        self.bg_color = "#8fcf4c" if (x + y) % 2 == 0 else "#7db048"

        # Append object to Cell.all list
        Cell.all.append(self)

    # Created a function the make a button at the specific location.
    def create_btn_obj(self, location):
        btn = Button(
            location,
            width=8,
            height=3,
            bg=self.bg_color
        )
        # Creating an event for the button. "<Button-1>" = left click.
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_obj = btn
    
    # Creates the label for number of cells left
    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg="#446324",
            fg="white",
            text=f"Flags Left: {Cell.num_flags}",
            font=("", 20)
        )
        Cell.cell_count_label_obj = lbl

    # The function that runs when left clicked. Takes 2 parameters.
    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            # If 0, it checks all cells around it
            if self.num_surrounding_mines == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()

    # Return a cell object based on the values of x and y.
    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    # Initializes a list for the surrounding cells.
    @property
    def surrounded_cells(self):
        # Creates a list of surrounding cells.
        surrounded_cells = [
            self.get_cell_by_axis(self.x-1, self.y-1),
            self.get_cell_by_axis(self.x-1, self.y),
            self.get_cell_by_axis(self.x-1, self.y+1),
            self.get_cell_by_axis(self.x, self.y-1),
            self.get_cell_by_axis(self.x+1, self.y-1),
            self.get_cell_by_axis(self.x+1, self.y),
            self.get_cell_by_axis(self.x+1, self.y+1),
            self.get_cell_by_axis(self.x, self.y+1)
        ]

        # Creating the same list with out 'None's
        cells = [cell for cell in surrounded_cells if cell is not None]
        return cells
    
    # Determines the number of minessurrounding the cell
    @property
    def num_surrounding_mines(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter+=1

        return counter

    # Shows the number of mines nearby the selected cell.
    def show_cell(self):
        mines_count = self.num_surrounding_mines
        # Sets the background color of the selected cells to their appropriate color.
        self.cell_btn_obj.configure(bg="#e3cfa6" if self.bg_color=="#8fcf4c" else "#c4b495")
        bnt_font = ("Arial", 9, "bold")
        if mines_count == 0:
            self.cell_btn_obj.configure(text="",font=bnt_font)
        else:
            color = {1:"green", 2:"blue", 3:"red", 4:"orange"}.get(mines_count,"black")
            self.cell_btn_obj.configure(text=mines_count, fg=color, font=bnt_font)
        # Sets the cell to be "selected"
        self.is_open = True

    # Shows the mine once it is selected.
    def show_mine(self):
        # A logic to interrupt the game and display losing message.
        self.cell_btn_obj.configure(bg='#db2121')

    # The function that runs when right clicked. Takes 2 parameters.
    def right_click_actions(self, event):
        if not self.is_open:
            Cell.num_flags -= 1
            if Cell.cell_count_label_obj:
                Cell.cell_count_label_obj.configure(text=f"Flags Left: {Cell.num_flags}")
                self.cell_btn_obj.configure(text="FLAG", fg="black", font=("Arial", 9, "bold"))
            print(event)
            print(f"I am RIGHT clicked! {Cell.num_flags}")

    # Randomly establishes cells to be mines.
    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all, settings.MINES_COUNT
        )
        # Sets selected mine to true.
        for pickeed_cell in picked_cells:
            pickeed_cell.is_mine = True
    
    # Makes the output of the attributes more friendly.
    def __repr__(self):
        return f"Cell({self.x}, {self.y})"