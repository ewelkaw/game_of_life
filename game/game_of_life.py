#!/usr/bin/env python

"""A well known game of life"""

import random
import sys
from collections import defaultdict, namedtuple
from itertools import product
from pathlib import Path

import pygame
from pygame.locals import *

BOARD_SIZE = [16, 16]
GAME_WINDOW_SIZE = (256, 256)
FIELDS_VALUES = {"on": ("on", "x.png"), "off": ("off", "red_dot.png")}
START_GAME_IMG = "start.png"
IMAGES_PATH = Path(__file__).absolute().parent.parent.joinpath("images")

# on/off
SingleBoardField = namedtuple("SingleBoardField", ["state", "state_image"])

IMAGES = {
    "on": pygame.image.load(str(IMAGES_PATH.joinpath(FIELDS_VALUES["on"][1]))),
    "off": pygame.image.load(str(IMAGES_PATH.joinpath(FIELDS_VALUES["off"][1]))),
}

ON = SingleBoardField(state=FIELDS_VALUES["on"][0], state_image=FIELDS_VALUES["on"][1])
OFF = SingleBoardField(
    state=FIELDS_VALUES["off"][0], state_image=FIELDS_VALUES["off"][1]
)


def prepare_empty_board() -> list:
    board = []
    for _ in range(BOARD_SIZE[0]):
        row = []
        for _ in range(BOARD_SIZE[1]):
            row.append(OFF)
        board.append(row)
    return board


def prepare_random_board() -> list:
    board = []
    for _ in range(BOARD_SIZE[0]):
        row = []
        for _ in range(BOARD_SIZE[1]):
            row.append(random.choice([ON, OFF]))
        board.append(row)
    return board


def prepare_neighbours(i: int, j: int) -> list:
    neighbours_x = [i]
    neighbours_y = [j]
    if i - 1 >= 0:
        neighbours_x.append(i - 1)
    if j - 1 >= 0:
        neighbours_y.append(j - 1)
    if i + 1 < 16:
        neighbours_x.append(i + 1)
    if j + 1 < 16:
        neighbours_y.append(j + 1)

    return [x for x in product(neighbours_x, neighbours_y) if x != (i, j)]


def check_new_field_values(
    field: SingleBoardField, board: list, neighbours: list
) -> tuple:
    field_state = field.state
    neighbours_states = defaultdict(int)
    for i, j in neighbours:
        neighbours_states[board[i][j].state] += 1

    if neighbours_states["on"] < 2:
        return FIELDS_VALUES["off"]
    if neighbours_states["on"] == 3:
        return FIELDS_VALUES["on"]
    if neighbours_states["on"] > 3:
        return FIELDS_VALUES["off"]
    if field_state is "on" and neighbours_states["on"] == 2:
        return FIELDS_VALUES["on"]
    else:
        return FIELDS_VALUES["off"]


def epoch(board: list) -> list:
    new_board = []

    for i in range(BOARD_SIZE[0]):
        new_row = []
        for j in range(BOARD_SIZE[1]):
            neighbours = prepare_neighbours(i, j)
            new_field_state, new_field_img = check_new_field_values(
                board[i][j], board, neighbours
            )
            new_row.append(
                SingleBoardField(state=new_field_state, state_image=new_field_img)
            )
        new_board.append(new_row)
    return new_board


def draw_board(board: list):
    background = pygame.Surface(GAME_WINDOW_SIZE)
    WINDOW.blit(background, (0, 0))
    for i, element in enumerate(board):
        for j, field in enumerate(element):
            img = IMAGES[field.state]
            WINDOW.blit(img, (i * 16, j * 16))
    pygame.display.flip()


def play(board: list):
    done = False
    while not done:
        board = epoch(board)
        draw_board(board)

        for e in pygame.event.get():
            if e.type == pygame.QUIT or (
                e.type == KEYUP
                and (e.key == K_RETURN or e.key == K_SPACE or e.key == K_ESCAPE)
            ):
                done = True
                break
        CLOCK.tick(2)


def main(board_start_mode="random"):
    if board_start_mode == "user":
        board = prepare_empty_board()
        pygame.display.set_caption("Press Enter to start the game")
        draw_board(board)

        done = False
        while not done:
            draw_board(board)

            for e in pygame.event.get():
                if e.type == QUIT or (
                    e.type == KEYUP and (e.key == K_RETURN or e.key == K_SPACE)
                ):
                    done = 1
                    break
                elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                    x = e.pos[0] // 16
                    y = e.pos[1] // 16
                    if board[x][y].state == "on":
                        board[x][y] = OFF
                    else:
                        board[x][y] = ON
            CLOCK.tick(10)

    elif board_start_mode == "random":
        board = prepare_random_board()

    pygame.display.set_caption("Game of Life")
    draw_board(board)
    play(board)


if __name__ == "__main__":
    pygame.init()
    WINDOW = pygame.display.set_mode(GAME_WINDOW_SIZE)
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("How you want to start game")
    img = pygame.image.load(str(IMAGES_PATH.joinpath(START_GAME_IMG)))
    WINDOW.blit(img, (0, 0))
    pygame.display.flip()

    done = False
    while not done:
        for e in pygame.event.get():
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                if e.pos[1] in range(51, 102):
                    board_start_mode = "user"
                    done = True
                if e.pos[1] in range(148, 199):
                    board_start_mode = "random"
                    done = True

    main(board_start_mode)
