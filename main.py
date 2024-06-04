import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fighting Game Input Buffer")

# Set up fonts
font = pygame.font.Font(None, 36)

# Load Input Images
button_images = {
    'up': pygame.image.load("up.png"),
    'down': pygame.image.load("down.png"),
    'left': pygame.image.load("left.png"),
    'right': pygame.image.load("right.png"),
    'light': pygame.image.load("L.png"),
    'medium': pygame.image.load("M.png"),
    'heavy': pygame.image.load("H.png"),
    'special': pygame.image.load("S.png"),
}

# Input buffer parameters
buffer = []
buffer_store_time = 0.4  # in seconds
max_buffer_size = 10
last_input_time = pygame.time.get_ticks()

# List of special moves
special_moves = [
    {"name": "Flame Punch", "sequence": ['down', 'right', 'light']},
    {"name": "Tornado Kick", "sequence": ['down', 'left', 'light']},
    {"name": "Rising Uppercut", "sequence": ['right', 'down', 'right', 'special']},
    {"name": "Surging Heat", "sequence": ['down', 'down', 'special']},
    {"name": "Inferno Overdrive", "sequence": ['down', 'down', 'left', 'heavy','special']},
    {"name": "Volcanic Vortex", "sequence": ['left', "down", 'right', 'left', 'down', 'right', 'heavy', 'special']},
    {"name": "Quick Rise", "sequence": ['up', 'up']}
    # Add more special moves here
]

# Flags to track if special moves are executed
special_move_executed = {move["name"]: False for move in special_moves}

# Define virtual buttons
VIRTUAL_BUTTONS = {
    'up': 'w',
    'down': 's',
    'left': 'a',
    'right': 'd',
    'light': 'u',
    'medium': 'i',
    'heavy': 'j',
    'special': 'k',
}

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Add the key to the buffer
            key = pygame.key.name(event.key)
            for button, physical_key in VIRTUAL_BUTTONS.items():
                if key == physical_key:
                    buffer.append(button)
                    break

            # Check if the buffer is full and replace the oldest input
            if len(buffer) > max_buffer_size:
                buffer.pop(0)

            # Check for special moves
            for move in special_moves:
                if buffer[-len(move["sequence"]):] == move["sequence"]:
                    special_move_executed[move["name"]] = True

            # Update the last input time
            last_input_time = pygame.time.get_ticks()

    # Check if it's time to clear the buffer
    current_time = pygame.time.get_ticks()
    if current_time - last_input_time >= buffer_store_time * 1000:
        buffer.clear()
        special_move_executed = {move["name"]: False for move in special_moves}

    # Draw the buffer and special move messages on the screen
    screen.fill((255, 255, 255))

    # Render the images for each key in the buffer
    x_position = 20
    for button in buffer:
        if button in button_images:
            button_image = button_images[button]
            screen.blit(button_image, (x_position, 20))
            x_position += button_image.get_width() + 10  # Adjust the spacing

    y_position = 60
    for move in special_moves:
        if special_move_executed[move["name"]]:
            special_move_text = font.render(move["name"] + " Executed!", True, (255, 0, 0))
            screen.blit(special_move_text, (20, y_position))
            y_position += 40

    pygame.display.flip()
