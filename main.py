"""Main module to run the 2048 game."""
import pygame as pg
from game.board import Board
from rendering.ui import GameUI
from rendering.menu import show_difficulty_menu
import game.audio_manager as audio
# pylint: disable=E1101, E0401


def main():
    """Main game function with restart capability."""
    pg.init()

    # Initialize audio system
    audio.initialize()


    play_again = True
    while play_again:
        play_again = run_game()


def run_game():
    """
    Run a single game session.
    
    Returns:
        bool: True if player wants to play again, False to exit.
    """
    # let the player pick difficulty
    difficulty = show_difficulty_menu()

    if difficulty is None:
        return False  # they closed the window

    size = 4
    # create the board but don't spawn tiles yet
    board = Board(size, difficulty=difficulty, ai_depth=2, spawn_initial=False)
    ui = GameUI(size, board)

    clock = pg.time.Clock()
    run = True

    # now spawn the initial tiles with animations
    board.spawn_random_tile()
    ui.old_grid = board.grid.copy()
    board.spawn_random_tile()
    ui.animate_spawn()

    print(f"Starting game with difficulty: {difficulty}")

    win_continue = False

    while run:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                board.update_highscore()
                pg.quit()
                return False

            if event.type == pg.KEYDOWN:
                result = handle_key_event(event, board, ui, win_continue)
                if result is not None:
                    return result

        ui.draw()

    board.update_highscore()
    return False


def handle_key_event(event, board, ui, win_continue):
    """Handle keyboard events during gameplay."""
    # if the game is over, any key restarts
    if board.game_over:
        board.update_highscore()
        return True

    # they won, they have the choice to continue or restart
    if board.won and not win_continue:
        if event.key == pg.K_SPACE:
            board._won = False  # pylint: disable=protected-access
            print("Continuing after win...")
            return None
        board.update_highscore()
        return True

    # normal gameplay - but wait for animations to finish first
    if not ui.has_active_animations():
        ui.prepare_move()
        moved = process_move(event, board)

        if moved:
            handle_successful_move(board, ui, win_continue)

    return None


def process_move(event, board):
    """Process a movement key and execute the move."""
    direction_map = {
        pg.K_UP: 'up',
        pg.K_DOWN: 'down',
        pg.K_LEFT: 'left',
        pg.K_RIGHT: 'right'
    }

    direction = direction_map.get(event.key)
    if direction:
        old_score = board.score
        moved = board.move(direction)
        if moved:
            audio.play_sound('move')
            # play merge sound if score increased
            if board.score > old_score:
                audio.play_sound('merge')
        return moved

    return False


def handle_successful_move(board, ui, win_continue):
    """Handle animations and game state after a successful move."""
    ui.animate_move()

    # wait for the slide to finish before spawning a new tile
    pg.time.wait(ui.animation_duration)
    board.spawn_random_tile()
    ui.animate_spawn()

    # check if they just hit 2048 for the first time
    if board.high_tile >= 2048 and not board.won and not win_continue:
        board._won = True  # pylint: disable=protected-access
        audio.play_sound('win')

    # see if there are any moves left
    if board.check_game_over():
        board.end_game()
        audio.play_sound('lose')


if __name__ == "__main__":
    main()
