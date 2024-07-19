import time
import sys 
import pygame
import argparse
from game import KnowledgeBase, TicTacPotatoe

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
# WIDTH, HEIGHT = 60, 60

# Main function
def main():
    win = None

    argparser = argparse.ArgumentParser(description="Simple MENACE-based Tic-Tac-Toe implementation")

    argparser.add_argument('--training', action='store_true', default=False, help='Runs 1000 of AI vs AI games in headless (no UI) mode')
    argparser.add_argument('--training-games', type=int, default=0, help='Runs passed number of AI vs AI games in headless (no UI) mode')

    args = argparser.parse_args()

    run = True
    training_games = args.training_games
    training = args.training

    player1 = 'human'
    player2 = 'ai'

    game_over_timer = 0

    scores = {
        0 : 0,
        1 : 0,
        2 : 0
    }

    scores_players = {
        'human' : 0,
        'ai' : 0,
    }

    if training_games > 0:
        training = True
    if training and not training_games > 0:
        training_games = 1000

    games_to_play = training_games
        
    knowledge = KnowledgeBase()
    knowledge.load()

    border_width = (WIDTH - HEIGHT) / 2
    
    clock = pygame.time.Clock()
    start_time = time.time()

    if training:
        game = TicTacPotatoe(None, knowledge, 'ai', 'ai', training)
    else:
        win = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption("Tic Tac Toe")
        game = TicTacPotatoe(win, knowledge, player1, player2, training)
        game.draw()

    while run:
        if not training:
            clock.tick(60)  # Limit to 60 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    game.handle_click(pos)

        if not training:
            game.draw()

        if game_over_timer == 0:
            game.update()
        else:
            game_over_timer -= 1
            if game_over_timer == 0:
                (player1, player2) = (player2, player1)
                game = TicTacPotatoe(win, knowledge, player1, player2, training)
            else:
                continue

        if game.ended():
            winner = game.get_winner()

            scores[winner] += 1

            if winner == 1:
                scores_players[player1] += 1
            elif winner == 2:
                scores_players[player2] += 1



            knowledge.learn(game.history, winner)
            knowledge.save()

            if training:
                games_to_play -= 1
                game = TicTacPotatoe(win, knowledge, 'ai', 'ai', training)
                if games_to_play == 0:
                    break
                print_training_progress(training_games - games_to_play, training_games)

            game_over_timer = 120

        if win is not None: 
            marker_width = border_width / 5
            spacer_width = marker_width / 4

            c, r = 0, 0
            for _ in range(scores_players['ai']):
                start = (c * spacer_width + (c) * marker_width, r * marker_width) 
                end = (c * spacer_width + (c+1) * marker_width, r * marker_width + marker_width) 
                pygame.draw.line(win, (255, 255, 255), start, end)

                start = (c * spacer_width + (c+1) * marker_width, r * marker_width) 
                end = (c * spacer_width + (c) * marker_width, r * marker_width + marker_width) 
                pygame.draw.line(win, (255, 255, 255), start, end)

                c += 1
                if c > 3:
                    c = 0
                    r += 1

            c, r = 0, 0

            for _ in range(scores_players['human']):
                start = (WIDTH - border_width + c * spacer_width + (c) * marker_width, r * marker_width) 
                end = (WIDTH - border_width + c * spacer_width + (c+1) * marker_width, r * marker_width + marker_width) 
                pygame.draw.line(win, (255, 255, 255), start, end)

                start = (WIDTH - border_width + c * spacer_width + (c+1) * marker_width, r * marker_width) 
                end = (WIDTH - border_width + c * spacer_width + (c) * marker_width, r * marker_width + marker_width) 
                pygame.draw.line(win, (255, 255, 255), start, end)

                c += 1
                if c > 3:
                    c = 0
                    r += 1
        

    if training:
        end_time = time.time()
        elapsed = end_time - start_time
        average = elapsed / training_games

        print(f"Played {training_games} games. X won {scores[1]}, O won {scores[2]}, drawn: {scores[0]}.")
        print(f"Took: {elapsed}s, average {average}s per game")

    pygame.quit()

def print_training_progress(game, total, bar_length= 40):
    percent = float(game) / total
    arrow = '=' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write(f"\r[{arrow}{spaces}] {int(round(percent * 100))}%")
    sys.stdout.flush()

if __name__ == "__main__":
    main()


