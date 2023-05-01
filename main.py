import random

import pygame

# Initialize pygame
pygame.init()

# Title and Icon
pygame.display.set_caption("Connect Four")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Create screen
CELL_SIZE = 100
SCREEN_ROWS = 7
SCREEN_COLS = 7
SCREEN_WIDTH = SCREEN_COLS * CELL_SIZE
SCREEN_HEIGHT = SCREEN_ROWS * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Player:
    def __init__(self, name, color):
        self.discs = []
        self.color = color
        self.name = name

    def give_new_disc(self):
        self.discs.insert(0, Disc(3, 0, self.color))

    def four_in_a_row_check(self):
        for disc in self.discs:
            if self.has_disc(disc.x + 1, disc.y) and self.has_disc(disc.x + 2, disc.y) and self.has_disc(disc.x + 3,
                                                                                                         disc.y):
                # Horizontal check
                return True
            elif self.has_disc(disc.x, disc.y + 1) and self.has_disc(disc.x, disc.y + 2) and self.has_disc(disc.x,
                                                                                                           disc.y + 3):
                # Vertical Check
                return True
            elif self.has_disc(disc.x + 1, disc.y + 1) and self.has_disc(disc.x + 2, disc.y + 2) and self.has_disc(
                    disc.x + 3, disc.y + 3):
                # Diagonal Check I
                return True
            elif self.has_disc(disc.x - 1, disc.y + 1) and self.has_disc(disc.x - 2, disc.y + 2) and self.has_disc(
                    disc.x - 3, disc.y + 3):
                # Diagonal Check II
                return True
        return False

    def has_disc(self, x, y):
        for disc in self.discs:
            if disc.x == x and disc.y == y:
                return True
        return False


class Disc:
    def __init__(self, x, y, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        x = (self.x * CELL_SIZE) + CELL_SIZE / 2
        y = (self.y * CELL_SIZE) + CELL_SIZE / 2

        pygame.draw.circle(screen, self.color, (x, y), CELL_SIZE / 2)


class Board:
    ROWS = 6
    COLS = 7

    def __init__(self):
        self.grid = [[None] * self.COLS for _ in range(self.ROWS)]

    def drop(self, disc, column_id):
        row_id = self.ROWS
        for row in reversed(self.grid):
            if row[column_id] is None:
                row[column_id] = disc
                return row_id, column_id
            else:
                row_id -= 1
        return False

    def draw(self):
        board_width = self.COLS * CELL_SIZE
        board_height = self.ROWS * CELL_SIZE
        board = pygame.Surface((board_width, board_height))
        board.fill((184, 205, 45))

        for row_id in range(self.ROWS):
            for column_id in range(self.COLS):
                x = (column_id * CELL_SIZE) + CELL_SIZE / 2
                y = (row_id * CELL_SIZE) + CELL_SIZE / 2
                disc = self.grid[row_id][column_id]
                color = disc.color if disc is not None else (0, 0, 0)

                pygame.draw.circle(board, color, (x, y), CELL_SIZE / 2)

        screen.blit(board, (0, CELL_SIZE))

    def is_full_check(self):
        for row in self.grid:
            for disc in row:
                if disc is None:
                    return False

        return True


class Game:
    def __init__(self):
        self.player1 = Player("player1", (255, 0, 0))
        self.player2 = Player("player2", (0, 0, 255))
        self.current_player = None
        self.randomize_current_player()
        self.current_player.give_new_disc()
        self.board = Board()
        self.game_state = "running"

    def play(self):
        game.board.draw()
        if self.game_state == "running":
            current_disc = self.current_player.discs[0]
            current_disc.draw()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and current_disc.x != 0:
                current_disc.x -= 1
            elif keys[pygame.K_RIGHT] and current_disc.x != SCREEN_COLS - 1:
                current_disc.x += 1
            elif keys[pygame.K_SPACE]:
                drop = self.board.drop(current_disc, current_disc.x)
                if drop is not False:
                    current_disc.x = drop[0]
                    current_disc.y = drop[1]
                    if self.current_player.four_in_a_row_check():
                        self.game_state = "win"
                    elif self.board.is_full_check():
                        self.game_state = "tie"
                    else:
                        self.set_next_player()
                        self.current_player.give_new_disc()
        elif self.game_state == "win":
            self.draw_text(f"{self.current_player.name} Wins!")
        elif self.game_state == "tie":
            self.draw_text(f"It's a tie")

    def randomize_current_player(self):
        self.current_player = random.choice([self.player1, self.player2])

    def set_next_player(self):
        self.current_player = self.player1 if self.current_player is not self.player1 else self.player2

    def draw_text(self, text):
        font = pygame.font.Font('freesansbold.ttf', 40)

        content = font.render(text, True, (255, 255, 255))
        content_rect = content.get_rect()
        content_rect.center = (SCREEN_WIDTH // 2, 40)
        screen.blit(content, content_rect)


# Game
game = Game()
running = True
while running:
    pygame.time.Clock().tick(10)
    # Background
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.play()

    pygame.display.update()
