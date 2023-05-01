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

# Hide mouse cursor
pygame.mouse.set_visible(False)


class Player:
    def __init__(self, name, color):
        self.discs = []
        self.color = color
        self.name = name

    def give_new_disc(self, col_id=3):
        self.discs.insert(0, Disc(col_id, 0, self.color))

    def four_in_a_row_check(self):
        for disc in self.discs:
            if self.has_disc(disc.row_id, disc.col_id + 1) \
                    and self.has_disc(disc.row_id, disc.col_id + 2) \
                    and self.has_disc(disc.row_id, disc.col_id + 3):
                # Horizontal check
                return True
            elif self.has_disc(disc.row_id + 1, disc.col_id) \
                    and self.has_disc(disc.row_id + 2, disc.col_id) \
                    and self.has_disc(disc.row_id + 3, disc.col_id):
                # Vertical Check
                return True
            elif self.has_disc(disc.row_id + 1, disc.col_id + 1) \
                    and self.has_disc(disc.row_id + 2, disc.col_id + 2) \
                    and self.has_disc(disc.row_id + 3, disc.col_id + 3):
                # Diagonal Check I
                return True
            elif self.has_disc(disc.row_id + 1, disc.col_id - 1) \
                    and self.has_disc(disc.row_id + 2, disc.col_id - 2) \
                    and self.has_disc(disc.row_id + 3, disc.col_id - 3):
                # Diagonal Check II
                return True
        return False

    def has_disc(self, row_id, col_id):
        for disc in self.discs:
            if disc.row_id == row_id and disc.col_id == col_id:
                return True
        return False


class Disc:
    def __init__(self, col_id, row_id, color=(255, 255, 255)):
        self.col_id = col_id
        self.row_id = row_id
        self.color = color

    def draw(self):
        x = (self.col_id * CELL_SIZE) + CELL_SIZE / 2
        y = (self.row_id * CELL_SIZE) + CELL_SIZE / 2

        pygame.draw.circle(screen, self.color, (x, y), CELL_SIZE / 2)

    def move_left(self):
        # Make sure the disc snaps back in the correct column before being able to move
        if isinstance(self.col_id, float):
            self.col_id = int(self.col_id)
        else:
            self.col_id -= 1

    def move_right(self):
        # Make sure the disc snaps back in the correct column before moving
        self.col_id = int(self.col_id)
        self.col_id += 1


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

    def update_game_state(self):
        if self.current_player.four_in_a_row_check():
            self.game_state = "win"
        elif self.board.is_full_check():
            self.game_state = "tie"
        else:
            self.initiate_next_turn()

    def drop_current_disc(self):
        current_disc = self.current_disc()

        drop = self.board.drop(current_disc, round(current_disc.col_id))
        if drop is not False:
            current_disc.col_id = drop[0]
            current_disc.row_id = drop[1]
            self.update_game_state()

    def initiate_next_turn(self):
        col_id = game.current_disc().col_id
        self.set_next_player()
        self.current_player.give_new_disc(col_id)

    def current_disc(self):
        return self.current_player.discs[0]

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
    # Background
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game.game_state == "running":
            if event.type == pygame.MOUSEMOTION \
                    and event.pos[0] < (SCREEN_COLS - 1) * CELL_SIZE:  # Make sure disc doesn't go off-screen
                game.current_disc().col_id = event.pos[0] / CELL_SIZE

            if event.type == pygame.MOUSEBUTTONDOWN:
                game.drop_current_disc()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and game.current_disc().col_id != 0:
                    game.current_disc().move_left()
                elif event.key == pygame.K_RIGHT and game.current_disc().col_id != SCREEN_COLS - 1:
                    game.current_disc().move_right()
                elif event.key == pygame.K_SPACE:
                    game.drop_current_disc()

    if game.game_state == "running":
        game.current_disc().draw()
    elif game.game_state == "win":
        game.draw_text(f"{game.current_player.name} Wins!")
    elif game.game_state == "tie":
        game.draw_text(f"It's a tie")

    game.board.draw()
    pygame.display.update()
