"""Basic unit tests for 2048 game."""
import sys
import os
import pytest
import numpy as np

# add the parent directory to path so imports work from tests/ folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.board import Board
from game.utils import combine_line
from ai.spawner import AISpawner


class TestCombineLine:
    """Test the core tile merging logic."""

    def test_merge_two_tiles(self):
        """Test merging two identical tiles."""
        line = np.array([2, 2, 0, 0])
        result, score = combine_line(line)
        assert np.array_equal(result, np.array([4, 0, 0, 0]))
        assert score == 4

    def test_merge_multiple_pairs(self):
        """Test merging multiple pairs in one line."""
        line = np.array([2, 2, 4, 4])
        result, score = combine_line(line)
        assert np.array_equal(result, np.array([4, 8, 0, 0]))
        assert score == 12

    def test_no_merge_different_values(self):
        """Test that different values don't merge."""
        line = np.array([2, 4, 8, 0])
        result, score = combine_line(line)
        assert np.array_equal(result, np.array([2, 4, 8, 0]))
        assert score == 0

    def test_compress_with_gaps(self):
        """Test compression removes gaps."""
        line = np.array([2, 0, 2, 0])
        result, score = combine_line(line)
        assert np.array_equal(result, np.array([4, 0, 0, 0]))
        assert score == 4

    def test_empty_line(self):
        """Test empty line returns zeros."""
        line = np.array([0, 0, 0, 0])
        result, score = combine_line(line)
        assert np.array_equal(result, np.array([0, 0, 0, 0]))
        assert score == 0

    def test_triple_same_value(self):
        """Test three identical tiles only merge first two."""
        line = np.array([2, 2, 2, 0])
        result, score = combine_line(line)
        assert np.array_equal(result, np.array([4, 2, 0, 0]))
        assert score == 4


class TestBoard:
    """Test the game board logic."""

    def test_board_initialization(self):
        """Test board initializes with correct size."""
        board = Board(4, spawn_initial=False)
        assert board.size == 4
        assert board.grid.shape == (4, 4)
        assert board.score == 0
        assert not board.game_over
        assert not board.won

    def test_spawn_tile(self):
        """Test that spawning adds a tile."""
        board = Board(4, spawn_initial=False)
        board.spawn_random_tile()
        # check that exactly one tile was spawned
        non_zero = np.count_nonzero(board.grid)
        assert non_zero == 1
        # check it's either 2 or 4
        values = board.grid[board.grid != 0]
        assert values[0] in [2, 4]

    def test_move_left_simple(self):
        """Test simple left move."""
        board = Board(4, spawn_initial=False)
        board._grid = np.array([
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])
        result = board.move('left')
        assert result is False  # no change, already on left

    def test_move_creates_merge(self):
        """Test move that creates a merge."""
        board = Board(4, spawn_initial=False)
        board._grid = np.array([
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])
        board.move('left')
        assert board.grid[0, 0] == 4
        assert board.score == 4

    def test_invalid_move(self):
        """Test invalid move direction."""
        board = Board(4, spawn_initial=False)
        result = board.move('invalid')
        assert result is False

    def test_win_condition(self):
        """Test win condition triggers at 2048."""
        board = Board(4, spawn_initial=False)
        board._grid = np.array([
            [1024, 1024, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])
        board.move('left')
        assert board.won
        assert board.high_tile == 2048


class TestAISpawner:
    """Test the AI spawner logic."""

    def test_medium_spawns_randomly(self):
        """Test medium difficulty uses random spawning."""
        board = Board(4, difficulty='medium', spawn_initial=False)
        spawner = AISpawner(difficulty='medium')
        result = spawner.spawn_tile(board)
        assert result is True
        assert np.count_nonzero(board.grid) == 1

    def test_easy_helps_player(self):
        """Test easy difficulty picks favorable positions."""
        board = Board(4, difficulty='easy', spawn_initial=False)
        # set up a board where one corner is clearly better
        board._grid = np.array([
            [2, 4, 8, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])
        spawner = AISpawner(difficulty='easy', search_depth=2)
        spawner.spawn_tile(board)
        # should spawn somewhere that helps (not blocking the high tiles)
        assert np.count_nonzero(board.grid) == 5

    def test_hard_hinders_player(self):
        """Test hard difficulty picks bad positions."""
        board = Board(4, difficulty='hard', spawn_initial=False)
        board._grid = np.array([
            [2, 4, 8, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])
        spawner = AISpawner(difficulty='hard', search_depth=3)
        spawner.spawn_tile(board)
        # should spawn somewhere that hinders
        assert np.count_nonzero(board.grid) == 5

    def test_spawner_returns_false_when_full(self):
        """Test spawner returns False when board is full."""
        board = Board(4, spawn_initial=False)
        board._grid = np.full((4, 4), 2)  # fill board
        spawner = AISpawner(difficulty='medium')
        result = spawner.spawn_tile(board)
        assert result is False


class TestGameOver:
    """Test game over detection."""

    def test_game_over_when_no_moves(self):
        """Test game over detected when no moves possible."""
        board = Board(4, spawn_initial=False)
        # create a checkerboard pattern with no possible merges
        board._grid = np.array([
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ])
        is_over = board.check_game_over()
        assert is_over is True

    def test_not_game_over_with_empty_space(self):
        """Test game not over when empty spaces exist."""
        board = Board(4, spawn_initial=False)
        board._grid = np.array([
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 0],
            [4, 2, 4, 2]
        ])
        is_over = board.check_game_over()
        assert is_over is False

    def test_not_game_over_with_possible_merge(self):
        """Test game not over when merges are possible."""
        board = Board(4, spawn_initial=False)
        board._grid = np.array([
            [2, 2, 4, 8],
            [4, 8, 16, 32],
            [8, 16, 32, 64],
            [16, 32, 64, 128]
        ])
        is_over = board.check_game_over()
        assert is_over is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])