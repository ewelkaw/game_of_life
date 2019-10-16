import pytest
from game.game_of_life import epoch, SingleBoardField


def test_board_state_change_all_off():
    on = SingleBoardField(state="on", state_image="x.png")
    off = SingleBoardField(state="off", state_image="red_dot.png")
    previous = [[off] * 16] * 16
    expected = [[off] * 16] * 16
    assert epoch(previous) == expected


def test_board_state_change_success():
    on = SingleBoardField(state="on", state_image="x.png")
    off = SingleBoardField(state="off", state_image="red_dot.png")
    previous = [[off] * 16] * 16
    previous[2][2] = on
    expected = [[off] * 16] * 16
    assert epoch(previous) == expected


def test_board_state_change_edges_on():
    on = SingleBoardField(state="on", state_image="x.png")
    off = SingleBoardField(state="off", state_image="red_dot.png")
    previous = [[on] * 16] * 16
    expected = [[off] * 16] * 16
    edges = [(0, 0), (0, 15), (15, 0), (15, 15)]
    for x, y in edges:
        expected[x][y] = on
    assert epoch(previous) == expected
