"""
GameEngine: owns the helicopter and all obstacles.
"""

import random

import pygame

from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3
PIXELS_PER_METER = 10   # 10 scrolled pixels = 1 metre of distance


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Start (or restart) a fresh game."""
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.game_over = False
        self.distance_px = 0.0   # total distance travelled

    def _spawn_obstacle(self):
        margin = 60
        gap_y = random.randint(margin + GAP_HEIGHT // 2, HEIGHT - margin - GAP_HEIGHT // 2)
        self.obstacles.append(Obstacle(
            x=WIDTH, gap_y=gap_y, gap_height=GAP_HEIGHT,
            wall_width=WALL_WIDTH, screen_height=HEIGHT, speed=SCROLL_SPEED,
        ))

    def handle_input(self, keys_pressed):
        if self.game_over:
            return
        self.helicopter.handle_input(keys_pressed)

    def handle_keydown(self, key):
        if self.game_over and key in (pygame.K_r, pygame.K_RETURN):
            self.reset()

    @property
    def distance(self):
        return int(self.distance_px // PIXELS_PER_METER)

    def _hits_obstacle(self, obstacle):
        rect = self.helicopter.get_rect()
        return (rect.colliderect(obstacle.get_top_rect())
                or rect.colliderect(obstacle.get_bottom_rect()))

    def update(self):
        if self.game_over:
            return

        self.helicopter.update(HEIGHT)
        self.distance_px += SCROLL_SPEED

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()
            if self._hits_obstacle(obstacle):
                self.game_over = True
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.helicopter, self.obstacles)
        renderer.draw_text(surface, font, f"Distance: {self.distance} m", (10, 10))
        if self.game_over:
            renderer.draw_banner(surface, font, "GAME OVER  -  press R to restart", offset_y=-20)
            renderer.draw_banner(surface, font, f"Final distance: {self.distance} m", offset_y=20,
                                 color=renderer.COLOR_TEXT)