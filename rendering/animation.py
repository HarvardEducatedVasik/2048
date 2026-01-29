"""Animation handling for 2048 tiles."""
import pygame as pg
# pylint: disable=R0913
# pylint: disable=R0917

class TileAnimation:
    """Handles animations for tiles in the 2048 game."""

    def __init__(self, tile_value, start_rect, end_rect, animation_type='slide', duration=150):
        """
        Initialize a tile animation.
        
        Args:
            tile_value: The numeric value of the tile (2, 4, 8, etc.)
            start_rect: Starting pygame.Rect position
            end_rect: Ending pygame.Rect position
            animation_type: 'slide', 'spawn', or 'merge'
            duration: Animation duration in milliseconds
        """
        self.value = tile_value
        self.start_rect = start_rect.copy()
        self.end_rect = end_rect.copy()
        self.type = animation_type
        self.duration = duration
        self.start_time = pg.time.get_ticks()

    def get_progress(self):
        """
        Calculate animation progress from 0.0 to 1.0.
        
        Returns:
            float: Progress value clamped between 0.0 and 1.0
        """
        elapsed = pg.time.get_ticks() - self.start_time
        return min(elapsed / self.duration, 1.0)

    def ease_out_cubic(self, t):
        """
        Easing function for smooth animation.
        
        Args:
            t: Progress value from 0.0 to 1.0
            
        Returns:
            float: Eased value
        """
        return 1 - pow(1 - t, 3)

    def get_current_rect(self):
        """
        Get the current position rect based on animation progress.
        
        Returns:
            pygame.Rect: Current position with easing applied
        """
        progress = self.ease_out_cubic(self.get_progress())

        # smoothly move from start to end position
        x = self.start_rect.x + (self.end_rect.x - self.start_rect.x) * progress
        y = self.start_rect.y + (self.end_rect.y - self.start_rect.y) * progress

        return pg.Rect(x, y, self.start_rect.width, self.start_rect.height)

    def get_scale(self):
        """
        Get the current scale factor for spawn/merge animations.
        
        Returns:
            float: Scale factor (1.0 = normal size)
        """
        progress = self.get_progress()

        if self.type == 'spawn':
            # grow from nothing with a little bounce
            if progress < 0.8:
                return progress / 0.8 * 1.1

            return 1.1 - (progress - 0.8) / 0.2 * 0.1

        if self.type == 'merge':
            # quick bounce when tiles combine
            return 1.0 + 0.15 * (1 - abs(2 * progress - 1))

        return 1.0

    def is_finished(self):
        """
        Check if animation is complete.
        
        Returns:
            bool: True if animation has finished
        """
        return self.get_progress() >= 1.0
