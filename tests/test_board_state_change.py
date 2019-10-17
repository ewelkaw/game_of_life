import pytest

from game.game_of_life import BOARD_SIZE, OFF, ON, SingleBoardField, epoch


def prepare_board(mode) -> list:
    board = []
    for _ in range(BOARD_SIZE[0]):
        row = []
        for _ in range(BOARD_SIZE[1]):
            row.append(mode)
        board.append(row)
    return board


def test_board_state_change_all_off():
    on = SingleBoardField(state="on", state_image="x.png")
    off = SingleBoardField(state="off", state_image="red_dot.png")
    previous = prepare_board(OFF)
    expected = prepare_board(OFF)
    assert epoch(previous) == expected


def test_board_state_change_success():
    on = SingleBoardField(state="on", state_image="x.png")
    off = SingleBoardField(state="off", state_image="red_dot.png")
    previous = prepare_board(OFF)
    previous[2][2] = on
    expected = prepare_board(OFF)
    assert epoch(previous) == expected


def test_board_state_change_edges_on():
    on = SingleBoardField(state="on", state_image="x.png")
    off = SingleBoardField(state="off", state_image="red_dot.png")
    previous = prepare_board(ON)
    expected = prepare_board(OFF)
    edges = [(0, 0), (0, 15), (15, 0), (15, 15)]
    for x, y in edges:
        expected[x][y] = on
    assert epoch(previous) == expected
