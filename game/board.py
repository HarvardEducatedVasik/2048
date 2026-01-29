"""Game board logic for 2048."""
import copy
import numpy as np
#pylint: disable=E0401
from game.utils import combine_line
from ai.spawner import AISpawner

class Board:
    """Manages the game board state and logic."""
    # pylint: disable=R0902
    def __init__(self, size, difficulty='medium', ai_depth=2, spawn_initial=True):
        """
        Initialize game board.

        Args:
            size: Board size (usually 4)
            difficulty: 'easy', 'medium', or 'hard'
            ai_depth: Search depth for AI (2-3 recommended)
            spawn_initial: Whether to spawn initial tiles (set False for menu before spawning)
        """
        self.size = size
        self._grid = np.zeros((size, size), dtype=int)
        self._score = 0
        self._high_tile = 0
        self._game_over = False
        self._won = False
        self._highscore = 0
        self.difficulty = difficulty

        # set up the AI that decides where to spawn new tiles
        self.ai_spawner = AISpawner(difficulty, ai_depth)

        # start with two tiles if requested
        if spawn_initial:
            self.spawn_random_tile()
            self.spawn_random_tile()

        # load the saved high score from file
        with open(r"./game/highscore.txt", "r", encoding="utf-8") as f:
            highscore = f.read()
            if highscore:
                self._highscore = int(highscore)

    # properties so we can't accidentally access the privates
    @property
    def grid(self):
        """Get the current game grid."""
        return self._grid

    @property
    def score(self):
        """Get the current score."""
        return self._score

    @property
    def high_tile(self):
        """Get the highest tile value."""
        return self._high_tile

    @property
    def game_over(self):
        """Check if the game is over."""
        return self._game_over

    @property
    def won(self):
        """Check if the player has won."""
        return self._won

    def set_difficulty(self, difficulty):
        """Change difficulty mid-game."""
        self.difficulty = difficulty
        self.ai_spawner = AISpawner(difficulty, self.ai_spawner.search_depth)

    def spawn_random_tile(self):
        """Spawn a new tile using AI or random based on difficulty."""
        return self.ai_spawner.spawn_tile(self)

    def print_board(self):
        """Print the current board state to console."""
        print(self._grid)
        print(f"Score: {self._score}")
        print(f"Difficulty: {self.difficulty}")

    def end_game(self):
        """Mark the game as over."""
        self._game_over = True
        print("Game Over!")

    def move(self, direction):
        """
        Execute a move in the specified direction.

        Args:
            direction: One of 'up', 'down', 'left', 'right'

        Returns:
            bool: True if move was successful, False if impossible
        """
        if direction not in ['up', 'down', 'left', 'right']:
            print("Invalid move direction!")
            return False

        total_score_gained = 0
        original_grid = self._grid.copy()

        # for vertical moves, we flip the grid so we can treat everything as rows
        if direction in ['up', 'down']:
            grid_to_process = self._grid.T
        else:
            grid_to_process = self._grid

        new_grid = np.zeros_like(grid_to_process, dtype=int)

        for i in range(self.size):
            line_to_process = grid_to_process[i, :]

            # flip the line for moves going right or down
            if direction in ['right', 'down']:
                line_to_process = line_to_process[::-1]

            new_line, score_gained = combine_line(line_to_process)
            total_score_gained += score_gained

            # flip it back
            if direction in ['right', 'down']:
                new_line = new_line[::-1]

            new_grid[i, :] = new_line

        # flip the whole grid back if we moved vertically
        if direction in ['up', 'down']:
            new_grid = new_grid.T

        # do nothing if the grid didn't change
        if np.array_equal(new_grid, original_grid):
            return False

        self._grid = new_grid
        self._score += total_score_gained
        self._highscore = max(self._score,self._highscore)
        self._high_tile = self._grid.max()

        # check if they just hit 2048 for the first time
        if self._high_tile >= 2048 and not self._won:
            self._won = True
            print("Congratulations! You reached 2048!")

        return True

    def update_highscore(self):
        """Save the current high score to file."""
        with open(r"./game/highscore.txt", "w", encoding="utf-8") as f:
            f.write(str(self._highscore))
    def check_game_over(self):
        """
        Check if any valid moves remain.

        Returns:
            bool: True if no moves possible, False otherwise
        """
        # try every direction to see if any move works
        temp_board = copy.deepcopy(self)
        directions = ["up", "down", "right", "left"]

        for direction in directions:
            if temp_board.move(direction):
                return False  # found a valid move - game's not over

        # no moves left, save the high score
        self.update_highscore()
        return True

if __name__ == "__main__":
    b = Board(4, difficulty='hard')
    b.print_board()
