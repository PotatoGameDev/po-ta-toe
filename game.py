import os
import random
from re import search
import pygame
import time
import json
MAGIC_NUMBER = 19683

class Position:
    # move = (col, row)
    def __init__(self, move = (), prev = 0):
        self._values = [0 for _ in range(9)]

        if prev > 0:
            self.fill_values(prev)

        if not move:
            return

        index = move[1] * 3 + move[0]

        move_value = self.whose_move()

        if self._values[index] != 0:
            raise ValueError(f"Move {move} already taken")

        self._values[index] = move_value

    def __iter__(self):
        self.current = 0
        return self

    def __next__(self):
        if self.current < 9:
            val = self._values[self.current]
            result = ''
            if val == 1:
                result = 'X'
            elif val == 2:
                result = 'O'
            else:
                result = ''
            self.current += 1
            return result
        else:
            raise StopIteration

    def __hash__(self):
        p = 0
        h = 0
        for v in self._values:
            h += v * (3 ** (8 - p))
            p += 1
        return h

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        for i in range(9):
            if self._values[i] != other._values[i]:
                return False
        return True

    def __str__(self):
        return str(hash(self))

    @classmethod
    def from_str(cls, hash):
        return cls(prev = int(hash))

    def fill_values(self, hash):
        current = hash + MAGIC_NUMBER
        ind = 8

        while current > 1:
            quot, rem = divmod(current, 3)
            if current == MAGIC_NUMBER:
                current = quot
                continue
            current = quot
            self._values[ind] = rem
            ind -= 1

    def whose_move(self):
        moves = 0
        for i in self._values:
            if i > 0:
                moves += 1
        if moves % 2 == 0:
            return 1
        else:
            return 2

    # list of available moves (col, row):
    def available_moves(self):
        available = []
        for i in range(9):
            if self._values[i] == 0:
                col = i % 3
                row = int(i // 3)

                available.append((col, row))
        return available

    def is_move_valid(self, move):
        return move in self.available_moves()

    def get_winner(self):
        if self._values[4] != 0 and self._values[0] == self._values[4] and self._values[4] == self._values[8]:
            return self._values[4]
        if self._values[4] != 0 and self._values[2] == self._values[4] and self._values[4] == self._values[6]:
            return self._values[4]

        for i in range(3):
            if self._values[i] != 0 and self._values[i] == self._values[i + 3] and self._values[i + 3] == self._values[i + 6]:
                return self._values[i]

            if self._values[i*3] != 0 and self._values[i*3] == self._values[i*3 + 1] and self._values[i*3 + 1] == self._values[i*3 + 2]:
                return self._values[i*3]

        return 0

class KnowledgeBase:
    def __init__(self):
        self._positions = {}

    def get_available_moves(self, pos):
        if pos not in self._positions:
            self._positions[pos] = pos.available_moves()

        if len(self._positions[pos]) == 0:
            self._positions[pos] = pos.available_moves()

        return self._positions[pos]

    def learn(self, history, winner):
        for data in history:
            (pos, player, move) = data

            knowledge = self.get_available_moves(pos)

            if winner == 0: # drawing move
                knowledge.append(move)
            elif winner == player: # winning move
                knowledge.extend([move] * 3)
            else: # losing move
                if move in knowledge:
                    knowledge.remove(move)

    def load(self):
        if os.path.exists('knowledge.json'):
            with open('knowledge.json', 'r') as file:
                loaded = json.load(file)

            self._positions = {Position.from_str(key): value for key, value in loaded.items()}


    def save(self):
        serializable_positions = {str(key): value for key, value in self._positions.items()}
        with open('knowledge.json', 'w') as file:
            json.dump(serializable_positions, file)


class TicTacPotatoe:
    def __init__(self, win, knowledge, p1, p2, training):
        self.mouse_click_pos = None
        self.pos = Position()
        self.players = {}
        self.history = []
        self.knowledge = knowledge

        if not training:
            self.win = win
            self.win_height = self.win.get_height()
            self.win_width = self.win.get_width() 
            self.board_width = self.win_width
            self.border_width = (self.win_width - self.board_width) / 2
            self.lane_width = self.board_width / 3

        if p1 == 'human':
            self.players[1] = handle_human_move 
        else:
            self.players[1] = get_ai(training)

        if p2 == 'human':
            self.players[2] = handle_human_move 
        else:
            self.players[2] = get_ai(training)


    def draw(self):
        pygame.display.update()
        self.win.fill((0, 0, 0)) 
        self.draw_board()
        self.draw_position()

    def handle_click(self, pos):
        if pos[0] < self.border_width:
            return
        if pos[0] > self.border_width + self.board_width:
            return

        mouseX = pos[0] - self.border_width
        mouseY = pos[1]

        indX = int(mouseX // self.lane_width)
        indY = int(mouseY // self.lane_width)

        self.mouse_click_pos = (indX, indY)

    def get_winner(self):
        return self.pos.get_winner()

    def ended(self):
        return len(self.pos.available_moves()) == 0 or self.get_winner() != 0 


    def draw_position(self):
        halfLane = self.lane_width / 2
        startPos = halfLane
        row = 0
        col = 0
        for s in self.pos:
            offX = col * self.lane_width
            offY = row * self.lane_width
            centerX = startPos + offX
            centerY = startPos + offY

            if s == 'X':
                pygame.draw.line(self.win, (255, 255, 255) , (centerX - halfLane, centerY - halfLane), (centerX + halfLane, centerY + halfLane), 2)
                pygame.draw.line(self.win, (255, 255, 255) , (centerX - halfLane, centerY + halfLane), (centerX + halfLane, centerY - halfLane), 2)
            elif s == 'O':
                pygame.draw.circle(self.win, (255, 255, 255), (centerX, centerY), halfLane, 2) 
            else:
                pass

            if col == 2:
                col = 0
                row += 1
            else:
                col += 1

    def draw_board(self):
        pygame.draw.line(self.win, (255, 255, 255), (self.border_width + self.lane_width, 0), (self.border_width + self.lane_width, self.win_height), 5)
        pygame.draw.line(self.win, (255, 255, 255), (self.border_width + 2 * self.lane_width, 0), (self.border_width + 2 * self.lane_width, self.win_height), 5)

        pygame.draw.line(self.win, (255, 255, 255), (0, self.border_width + self.lane_width), (self.win_width, self.border_width + self.lane_width), 5)
        pygame.draw.line(self.win, (255, 255, 255), (0, self.border_width + 2 * self.lane_width), (self.win_width, self.border_width + 2 * self.lane_width), 5)

    def update(self):
        current_player = self.pos.whose_move()

        move = self.players[current_player](self.pos, self.mouse_click_pos, self.knowledge)

        if move is None:
            return

        self.history.append((self.pos, current_player, move))
        self.pos = Position(move, hash(self.pos))
        self.mouse_click_pos = None

def get_ai(training):
    def handle_ai_move(pos, _, knowledge):
        move = random.choice(knowledge.get_available_moves(pos))
        if not training:
            time.sleep(0.5)
        return move

    return handle_ai_move

def handle_human_move(pos, move, _):
    if pos.is_move_valid(move):
        return move 
    return None

