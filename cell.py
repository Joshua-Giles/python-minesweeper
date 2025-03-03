from tkinter import Button

# Creation of the Cell class to be the blocks in the field.
class Cell:
    # Defines the constructor to set values.
    def __init__(self, is_mine=False):
        self.is_mine = is_mine
        self.cell_btn_obj = None

    # Created a function the make a button at the specific location.
    def create_btn_obj(self, location):
        btn = Button(
            location,
            text='Text'
        )
        # Creating an event for the button. "<Button-1>" = left click.
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_obj = btn

    # The function that runs when left clicked. Takes 2 parameters.
    def left_click_actions(self, event):
        print(event)
        print("I am left clicked!")

    # The function that runs when right clicked. Takes 2 parameters.
    def right_click_actions(self, event):
        print(event)
        print("I am RIGHT clicked!")