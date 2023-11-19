import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)
option_font = pygame.font.Font(None, 30)

# Menu options
options = ["Option 1", "Option 2", "Option 3"]
selected_option = 0

# Function to display text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

# Main menu function
def main_menu():
    selected_option = 0
    running = True
    while running:
        screen.fill(WHITE)
        draw_text('Main Menu', font, BLACK, WIDTH // 2 - 70, HEIGHT // 4)

        # Display menu options
        for i, option in enumerate(options):
            if i == selected_option:
                text_color = RED
            else:
                text_color = BLACK
            draw_text(option, option_font, text_color, WIDTH // 2 - 50, HEIGHT // 2 + i * 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    print("Selected:", options[selected_option])
                    # Add your logic here for the selected option

        pygame.display.update()
        clock.tick(FPS)

# Run the game
main_menu()
pygame.quit()
