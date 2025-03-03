import settings

# Function to set the size of the height dynamically.
def height_prct(percentage):
    return (settings.HEIGHT / 100) * percentage

# Function to set the size of the width dynamically.
def width_prct(percentage):
    return (settings.WIDTH / 100) * percentage
