from tkinter import Button, Label
import settings
import random
import ctypes

# Creation of the Cell class to be the blocks in the field.
class Cell:
    # List of actions
    all = []
    # Global label for number of cells left.
    cell_count_label_obj = None
    # Creates the number of flags.
    num_flags = settings.MINES_COUNT
    # Number of mines in the game.
    num_mines = settings.MINES_COUNT
    # Number of cells left.
    cell_count = settings.CELL_COUNT
    # Flag to check for first click
    first_click = True
    # Defines the constructor to set values.
    def __init__(self, x, y,  is_mine=False):
        self.is_mine = is_mine
        self.is_open = False
        self.cell_btn_obj = None
        self.is_mine_candidate = False
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
            font=("small fonts", 20, 'bold')
        )
        Cell.cell_count_label_obj = lbl

    # The function that runs when left clicked. Takes 2 parameters.
    def left_click_actions(self, event):
        # On the first click, randomize mines safely.
        if Cell.first_click:
            # Creates a safe zone.
            safe_zone = [self] + self.surrounded_cells
            # All cells in the safe zone are candidates for mines.
            mine_candidates = [cell for cell in Cell.all if cell not in safe_zone]
            # Randomly place mines from the candidate.
            picked_cells = random.sample(mine_candidates, settings.MINES_COUNT)
            for picked_cell in picked_cells:
                picked_cell.is_mine = True
            # Mark that the first click has been handled.
            Cell.first_click = False

        # Proceed with normal click if not first
        if self.is_mine:
            self.show_mine()
            return
        else:
            if not self.is_open:
                self.show_cell()
                # If 0, it checks all cells around it
                if self.num_surrounding_mines == 0:
                    for cell_obj in self.surrounded_cells:
                        if not cell_obj.is_open:
                            cell_obj.left_click_actions(None)
                # If 10 cells left, player won
                if Cell.cell_count == Cell.num_mines:
                    ctypes.windll.user32.MessageBoxW(0, 'Congradulations, you won!', 'Game Over', 0)

        # Cancel left and right click events if cell is already opened
        self.cell_btn_obj.unbind('<Button-1>')
        self.cell_btn_obj.unbind('<Button-3>')

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
        if not self.is_mine_candidate:
            Cell.cell_count -= 1
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
        if not self.is_mine_candidate:
            # Sets the cell to red
            self.cell_btn_obj.configure(bg='#db2121')
            for cell in Cell.all:
                cell.cell_btn_obj.unbind('<Button-1>')
                cell.cell_btn_obj.unbind('<Button-3>')
                if cell.is_mine:
                    cell.cell_btn_obj.configure(bg='#db2121')
                cell.cell_btn_obj.configure(state='disabled')
            # A logic to interrupt the game and display losing message.
            # First 0 is required. First message is body. Second message is header. Second 0 is "Ok"
            ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game Over', 0)

    # The function that runs when right clicked. Takes 2 parameters.
    def right_click_actions(self, event):
        # Sets the original background color for the flag to change back.
        color = self.bg_color
        # If the cell is not flagged...
        if not self.is_mine_candidate:
            # If there are enough flags...
            if Cell.num_flags > 0:
                # If the cell has not been selected tet
                if not self.is_open:
                    Cell.num_flags -= 1
                    if Cell.cell_count_label_obj:
                        Cell.cell_count_label_obj.configure(text=f"Flags Left: {Cell.num_flags}")
                        self.cell_btn_obj.configure(bg="orange")
                    self.is_mine_candidate = True
        else:
            Cell.num_flags += 1
            if Cell.cell_count_label_obj:
                Cell.cell_count_label_obj.configure(text=f"Flags Left: {Cell.num_flags}")
                self.cell_btn_obj.configure(bg=color)
            self.is_mine_candidate = False

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