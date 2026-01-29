"""Menu module for 2048 game."""
import os
import pygame as pg
#pylint: disable=E0401
import game.utils as ut
# pylint: disable=E1101

def show_difficulty_menu():
    """
    Display difficulty selection menu.
    
    Returns:
        str or None: Selected difficulty ('easy', 'medium', 'hard') or None if closed
    """
    # make sure the window appears centered on screen
    if 'SDL_VIDEO_CENTERED' not in os.environ:
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    pg.init()
    screen = pg.display.set_mode((ut.SCREEN_HEIGHT, ut.SCREEN_WIDTH))
    pg.display.set_caption("2048 - Select Difficulty")

    fonts = _initialize_fonts()

    # set up the difficulty options
    options = _get_menu_options()

    # figure out where the buttons should go
    button_rects = _create_button_layout(options)

    # run the menu until they pick something
    selected = _menu_loop(screen, fonts, options, button_rects)

    return selected


def _initialize_fonts():
    """
    Initialize all fonts used in the menu.
    
    Returns:
        dict: Dictionary of font objects
    """
    return {
        'title': pg.font.SysFont("Comic Sans MS", 60, bold=True),
        'subtitle': pg.font.SysFont("Arial", 20),
        'option': pg.font.SysFont("Arial", 32, bold=True),
        'desc': pg.font.SysFont("Arial", 16),
        'detail': pg.font.SysFont("Arial", 14),
        'footer': pg.font.SysFont("Arial", 14, italic=True)
    }


def _get_menu_options():
    """
    Get difficulty options with descriptions and colors.
    
    Returns:
        list: List of tuples (name, description, detail, color)
    """
    return [
        ("Easy", "AI helps you with favorable spawns",
         "Good for learning!", (46, 204, 113)),
        ("Medium", "Random spawns (classic mode)",
         "The original experience", (52, 152, 219)),
        ("Hard", "AI hinders you with bad spawns",
         "For experienced players", (231, 76, 60))
    ]


def _create_button_layout(options):
    """
    Create button rectangles for menu options.
    
    Args:
        options: List of menu options
        
    Returns:
        list: List of tuples (rect, difficulty_name, color)
    """
    button_width = 450
    button_height = 75
    button_spacing = 100
    start_y = 250
    center_x = ut.SCREEN_HEIGHT // 2

    button_rects = []
    for i, (name, _, _, color) in enumerate(options):
        rect = pg.Rect(
            center_x - button_width // 2,
            start_y + i * button_spacing,
            button_width,
            button_height
        )
        button_rects.append((rect, name.lower(), color))

    return button_rects


def _menu_loop(screen, fonts, options, button_rects):
    """
    Main menu loop for difficulty selection.
    
    Args:
        screen: Pygame display surface
        fonts: Dictionary of font objects
        options: List of menu options
        button_rects: List of button rectangles
        
    Returns:
        str or None: Selected difficulty or None
    """
    selected = None
    clock = pg.time.Clock()

    while selected is None:
        screen.fill(ut.BACKGROUND_COLOR)

        # draw everything on screen
        _draw_title(screen, fonts)
        _draw_buttons(screen, fonts, options, button_rects)
        _draw_footer(screen, fonts)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return None

            if event.type == pg.MOUSEBUTTONDOWN:
                selected = _check_button_click(event.pos, button_rects)

        pg.display.update()
        clock.tick(60)

    return selected


def _draw_title(screen, fonts):
    """Draw menu title and subtitle."""
    title = fonts['title'].render("2048", True, (119, 110, 101))
    title_rect = title.get_rect(center=(ut.SCREEN_HEIGHT // 2, 100))
    screen.blit(title, title_rect)

    subtitle = fonts['subtitle'].render("Choose Your Challenge", True, (119, 110, 101))
    subtitle_rect = subtitle.get_rect(center=(ut.SCREEN_HEIGHT // 2, 160))
    screen.blit(subtitle, subtitle_rect)


def _draw_buttons(screen, fonts, options, button_rects):
    """
    Draw all difficulty selection buttons.
    
    Args:
        screen: Pygame display surface
        fonts: Dictionary of font objects
        options: List of menu options
        button_rects: List of button rectangles
    """
    mouse_pos = pg.mouse.get_pos()

    for (rect, _, color), (name, desc, detail, _) in zip(button_rects, options):
        is_hover = rect.collidepoint(mouse_pos)

        # draw the button with a hover effect if theyre pointing at it
        _draw_button(screen, rect, color, is_hover)

        # add the text on the button
        _draw_button_text(screen, fonts, rect, name, desc)

        # put the detail text below
        _draw_button_detail(screen, fonts, rect, detail)


def _draw_button(screen, rect, color, is_hover):
    """
    Draw a single button with optional hover effect.
    
    Args:
        screen: Pygame display surface
        rect: Button rectangle
        color: Button color
        is_hover: Whether mouse is hovering over button
    """
    # brighten the color a bit if they're hovering
    btn_color = tuple(min(c + 30, 255) for c in color) if is_hover else color

    # add a subtle shadow when hovering to make it pop
    if is_hover:
        shadow_rect = rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pg.draw.rect(screen, (150, 150, 150), shadow_rect, border_radius=10)

    pg.draw.rect(screen, btn_color, rect, border_radius=10)


def _draw_button_text(screen, fonts, rect, name, description):
    """
    Draw text on a button.
    
    Args:
        screen: Pygame display surface
        fonts: Dictionary of font objects
        rect: Button rectangle
        name: Button name text
        description: Button description text
    """
    # draw the difficulty name
    text = fonts['option'].render(name, True, (255, 255, 255))
    text_rect = text.get_rect(center=(rect.centerx, rect.centery - 15))
    screen.blit(text, text_rect)

    # add the description below it
    desc_text = fonts['desc'].render(description, True, (255, 255, 255))
    desc_rect = desc_text.get_rect(center=(rect.centerx, rect.centery + 15))
    screen.blit(desc_text, desc_rect)


def _draw_button_detail(screen, fonts, rect, detail):
    """
    Draw detail text below a button.
    
    Args:
        screen: Pygame display surface
        fonts: Dictionary of font objects
        rect: Button rectangle
        detail: Detail text to display
    """
    detail_text = fonts['detail'].render(detail, True, (119, 110, 101))
    detail_rect = detail_text.get_rect(
        center=(ut.SCREEN_HEIGHT // 2, rect.bottom + 12)
    )
    screen.blit(detail_text, detail_rect)


def _draw_footer(screen, fonts):
    """Draw footer instruction text."""
    footer = fonts['footer'].render(
        "Click a difficulty to start playing",
        True,
        (150, 150, 150)
    )
    footer_rect = footer.get_rect(
        center=(ut.SCREEN_HEIGHT // 2, ut.SCREEN_WIDTH - 40)
    )
    screen.blit(footer, footer_rect)


def _check_button_click(mouse_pos, button_rects):
    """
    Check if a button was clicked.
    
    Args:
        mouse_pos: Mouse position tuple (x, y)
        button_rects: List of button rectangles
        
    Returns:
        str or None: Difficulty name if clicked, None otherwise
    """
    for rect, difficulty, _ in button_rects:
        if rect.collidepoint(mouse_pos):
            return difficulty
    return None
