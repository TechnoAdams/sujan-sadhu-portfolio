import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("White Page with Button")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Button parameters
BUTTON_COLOR = (100, 100, 255)
BUTTON_HOVER_COLOR = (150, 150, 255)
BUTTON_RECT = pygame.Rect(350, 250, 100, 50)
FONT = pygame.font.Font(None, 36)

# Main loop
running = True
while running:
    screen.fill(WHITE)  # Fill the screen with white
    
    # Draw button
    if BUTTON_RECT.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, BUTTON_RECT)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, BUTTON_RECT)
    
    # Button text
    text = FONT.render("File", True, BLACK)
    screen.blit(text, (BUTTON_RECT.x + 20, BUTTON_RECT.y + 10))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if BUTTON_RECT.collidepoint(event.pos):
                print("File button clicked")

    pygame.display.flip()  # Update the screen

pygame.quit()
sys.exit()

