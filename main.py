import pgzrun
import time
from game import KnowledgeBase, TicTacPotatoe

# Set up display
WIDTH = 600
HEIGHT = 600

knowledge = KnowledgeBase()
knowledge.load()
player1 = 'human'
player2 = 'ai'
game = TicTacPotatoe(knowledge, player1, player2)

def draw():
    game.draw(screen)

def update():
    global player1, player2, game

    if game.ended():
        (player1, player2) = (player2, player1)
        game = TicTacPotatoe(knowledge, player1, player2)
        time.sleep(1)
    else:
        game.update()

def on_mouse_up(pos, button):
    if button == mouse.LEFT:
        game.handle_click(pos)

scores = {
    0 : 0,
    1 : 0,
    2 : 0
}


pgzrun.go()

