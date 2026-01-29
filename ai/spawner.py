"""AI spawner module for 2048."""
import copy
import numpy as np
#pylint: disable=R0903
class AISpawner:
    """
    Implements expectimax algorithm to strategically spawn tiles.
    Easy = helps player, Hard = hinders player, Medium = random
    """

    def __init__(self, difficulty='medium', search_depth=2, debug=False):
        """
        Initialize AI spawner.

        Args:
            difficulty: 'easy', 'medium', or 'hard'
            search_depth: How many moves ahead to look 2-3
            debug: If True, print AI decisions to console
        """
        self.difficulty = difficulty.lower()
        # on hard mode look one step further ahead to be extra mean
        if difficulty == 'hard':
            self.search_depth = 3
        else:
            self.search_depth = search_depth
        self.debug = debug

    def spawn_tile(self, board):
        """
        Spawn a tile based on difficulty setting.

        Args:
            board: Board instance

        Returns:
            bool: True if spawn successful, False otherwise
        """
        if self.difficulty == 'medium':
            # classic mode - just pick a random spot
            return self._spawn_random(board)

        empty_cells = list(zip(*np.where(board.grid == 0)))
        if not empty_cells:
            return False

        # figure out how good each position would be for the player
        scores = []
        for row, col in empty_cells:
            # check both possible tile values
            score_2 = self._evaluate_spawn(board, row, col, 2)
            score_4 = self._evaluate_spawn(board, row, col, 4)

            # weight them by probability (90% chance of 2, 10% chance of 4)
            avg_score = 0.9 * score_2 + 0.1 * score_4
            scores.append((avg_score, row, col))

        # sort from worst to best
        scores.sort(key=lambda x: x[0])

        # pick based on difficulty
        if self.difficulty == 'easy':
            best_pos = scores[-1]  # give them the best spot
        else:  # hard
            best_pos = scores[0]  # give them the worst spot

        _, row, col = best_pos

        # spawn the tile with normal probabilities
        board._grid[row, col] = np.random.choice([2, 4], p=[0.9, 0.1])  # pylint: disable=protected-access

        # debug helper
        if self.debug:
            print(f"\n AI {self.difficulty.upper()} spawned at ({row},{col})")
            print(f"   Position score: {best_pos[0]:.1f}")
            print(f"   All scores: {sorted([s[0] for s in scores])}")
            print(f"   Best score: {max(s[0] for s in scores):.1f}")
            print(f"   Worst score: {min(s[0] for s in scores):.1f}")

        return True

    def _spawn_random(self, board):
        """Original random spawning for medium difficulty."""
        empty_cells = list(zip(*np.where(board.grid == 0)))
        if not empty_cells:
            return False

        index = int(np.random.randint(len(empty_cells)))
        row, col = empty_cells[index]
        board._grid[row, col] = np.random.choice([2, 4], p=[0.9, 0.1])  # pylint: disable=protected-access
        return True

    def _evaluate_spawn(self, board, row, col, value):
        """
        Evaluate how good a spawn position is for the player.
        Uses expectimax to look ahead.

        Args:
            board: Board instance
            row, col: Position to spawn
            value: Tile value (2 or 4)

        Returns:
            float: Expected score - higher = better for player
        """
        # make a copy so we don't mess up the real board
        temp_board = copy.deepcopy(board)
        temp_board._grid[row, col] = value  # pylint: disable=protected-access

        # simulate what might happen from here
        return self._expectimax(temp_board, self.search_depth, True)

    def _expectimax(self, board, depth, is_player_turn):
        """
        Expectimax algorithm.

        Args:
            board: Board instance
            depth: Remaining search depth
            is_player_turn: True if player's turn, False if chance node

        Returns:
            float: Expected value of this state
        """
        if depth == 0 or self._is_terminal(board):
            return self._evaluate_board(board)

        if is_player_turn:
            # player picks the best move they can
            return self._max_node(board, depth)
        # chance node - random tile appears
        return self._chance_node(board, depth)

    def _max_node(self, board, depth):
        """Player's turn - try all moves and pick best."""
        max_value = float('-inf')

        for direction in ['up', 'down', 'left', 'right']:
            temp_board = copy.deepcopy(board)

            if temp_board.move(direction):
                # this move worked, see how good the result is
                value = self._expectimax(temp_board, depth - 1, False)
                max_value = max(max_value, value)

        # if no moves worked, just evaluate where we are now
        if max_value == float('-inf'):
            return self._evaluate_board(board)

        return max_value

    def _chance_node(self, board, depth):
        """Chance node - average over possible spawns."""
        empty_cells = list(zip(*np.where(board.grid == 0)))

        if not empty_cells:
            return self._evaluate_board(board)

        total_value = 0
        num_cells = len(empty_cells)

        # if there are too many empty cells, just sample a few (optimization)
        if num_cells > 6:
            empty_cells = [empty_cells[i] for i in
                          np.random.choice(num_cells, 6, replace=False)]
            num_cells = 6

        for row, col in empty_cells:
            # try spawning a 2
            temp_board_2 = copy.deepcopy(board)
            temp_board_2._grid[row, col] = 2  # pylint: disable=protected-access
            value_2 = self._expectimax(temp_board_2, depth - 1, True)

            # try spawning a 4
            temp_board_4 = copy.deepcopy(board)
            temp_board_4._grid[row, col] = 4  # pylint: disable=protected-access
            value_4 = self._expectimax(temp_board_4, depth - 1, True)

            # combine them by probability
            cell_value = 0.9 * value_2 + 0.1 * value_4
            total_value += cell_value

        return total_value / num_cells

    def _is_terminal(self, board):
        """Check if state is terminal (game over)."""
        # if there's any empty space, game's not over
        if np.any(board.grid == 0):
            return False

        # try all moves to see if any work
        for direction in ['up', 'down', 'left', 'right']:
            temp_board = copy.deepcopy(board)
            if temp_board.move(direction):
                return False

        return True

    def _evaluate_board(self, board):
        """
        Heuristic evaluation of board state.
        Higher score = better for player.
        """
        grid = board.grid
        score = 0

        # current score matters a lot
        score += board.score * 2.0

        # having empty spaces is super important
        empty_tiles = np.sum(grid == 0)
        score += empty_tiles * 500

        # tiles should flow in one direction (monotonicity)
        score += self._monotonicity(grid) * 100

        # similar tiles should be next to each other (smoothness)
        score += self._smoothness(grid) * 30

        # big bonus if the highest tile is in a corner
        max_tile_bonus = self._max_tile_corner_bonus(grid) * 1000
        score += max_tile_bonus

        # big penalty if the max tile isn't in a corner
        max_val = np.max(grid)
        corners = [grid[0, 0], grid[0, -1], grid[-1, 0], grid[-1, -1]]
        if max_val not in corners:
            score -= 2000

        # penalize scattered high tiles
        high_tiles = grid[grid >= 64]
        if len(high_tiles) > 0:
            positions = np.argwhere(grid >= 64)
            if len(positions) > 1:
                spread = np.std(positions)
                score -= spread * 50

        # bonus for organized rows and columns
        for i in range(grid.shape[0]):
            row = grid[i, :]
            if self._is_organized(row):
                score += 200

        for j in range(grid.shape[1]):
            col = grid[:, j]
            if self._is_organized(col):
                score += 200

        return score

    def _monotonicity(self, grid):
        """Measure how monotonic the rows or columns are."""
        totals = [0, 0, 0, 0]  # up, down, left, right

        # check each row
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1] - 1):
                if grid[i, j] > grid[i, j+1]:
                    totals[0] += grid[i, j] - grid[i, j+1]
                else:
                    totals[1] += grid[i, j+1] - grid[i, j]

        # check each column
        for j in range(grid.shape[1]):
            for i in range(grid.shape[0] - 1):
                if grid[i, j] > grid[i+1, j]:
                    totals[2] += grid[i, j] - grid[i+1, j]
                else:
                    totals[3] += grid[i+1, j] - grid[i, j]

        return max(totals[0], totals[1]) + max(totals[2], totals[3])

    def _smoothness(self, grid):
        """Measure how smooth the grid is - lower differences between adjacent tiles."""
        smoothness = 0

        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if grid[i, j] != 0:
                    # check the tile to the right
                    if j < grid.shape[1] - 1 and grid[i, j+1] != 0:
                        smoothness -= abs(np.log2(grid[i, j]) - np.log2(grid[i, j+1]))
                    # check the tile below
                    if i < grid.shape[0] - 1 and grid[i+1, j] != 0:
                        smoothness -= abs(np.log2(grid[i, j]) - np.log2(grid[i+1, j]))

        return smoothness

    def _max_tile_corner_bonus(self, grid):
        """Give bonus if max tile is in a corner."""
        max_val = np.max(grid)
        corners = [grid[0, 0], grid[0, -1], grid[-1, 0], grid[-1, -1]]

        if max_val in corners:
            return 1
        return 0

    def _is_organized(self, line):
        """Check if a line is organized - monotonic or mostly monotonic."""
        non_zero = line[line != 0]
        if len(non_zero) <= 1:
            return True

        # see if tiles are mostly increasing or decreasing
        diffs = np.diff(non_zero)
        increasing = np.sum(diffs > 0)
        decreasing = np.sum(diffs < 0)

        # at least 70% should follow one direction
        total_changes = len(diffs)
        threshold = 0.7 * total_changes
        return (increasing >= threshold) or (decreasing >= threshold)
