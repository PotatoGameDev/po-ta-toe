import pygame
from game import TicTacPotatoe

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Main function
def main():
    run = True
    clock = pygame.time.Clock()
    game = TicTacPotatoe(WIN, 'human', 'ai')

    while run:
        clock.tick(60)  # Limit to 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                game.handle_click(pos)

        game.update()
        game.draw()

    pygame.quit()

if __name__ == "__main__":
    main()


