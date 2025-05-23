# settings.py

# Screen settings
WIDTH = 400
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (34, 139, 34)

# Bird settings
BIRD_START_X = 50
BIRD_START_Y = HEIGHT // 2
GRAVITY = 0.5
JUMP_STRENGTH = -10

# Pipe settings
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_VELOCITY = 3
PIPE_FREQUENCY_MS = 1500  # milliseconds between pipes
MIN_PIPE_GAP = 100 # Added this line for the minimum gap