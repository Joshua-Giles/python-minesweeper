from tkinter import *
from cell import Cell
import settings
import util

# Initialization of the GUI window.
root = Tk()
# Sets the background color to be light green.
root.configure(bg="#8fcf4c")

# Changes the aspect ratio of the GUI.
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
# Changes the title of the window that is created (initial name is 'tk').
root.title('Minesweeper')
# Sets the width and height resizability to false respectively.
root.resizable(False, False)

# Creation of the header frame.
top_frame = Frame(
    root,
    bg = '#446324',
    width = util.width_prct(100),
    height = util.height_prct(20)
)
# Places the frame in the adequate location.
top_frame.place(x = 0, y = 0)

# Creating a frame to save best times.
left_frame = Frame(
    root,
    bg = '#293d14',
    width = util.width_prct(20),
    height = util.height_prct(80)
)
# Places it on the left side of the page.
left_frame.place(x = 0, y = util.height_prct(20))

# Creation of the frame that will hold the game.
center_frame = Frame(
    root,
    bg='#8fcf4c',
    width=util.width_prct(80),
    height=util.height_prct(80)
)
# Places it accordingly
center_frame.place(
    x=util.width_prct(20),
    y=util.height_prct(20)
)

for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell()
        c.create_btn_obj(center_frame)
        c.cell_btn_obj.grid(
            column=x,
            row=y
        )

# Ends the loop of the GUI.
mainloop()
