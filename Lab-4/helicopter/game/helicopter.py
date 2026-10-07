"""
Helicopter: the player-controlled vehicle. Moves vertically based on
held Up/Down keys.
"""

import pygame

THRUST = 0.4        # acceleration added per frame while a key is held
MAX_SPEED = 6.0     # vertical speed can never exceed this
DRAG = 0.85         # vy is multiplied by this each frame when no key is held


class Helicopter:
    def __init__(self, x, y, width=40, height=24):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vy = 0.0

    def handle_input(self, keys_pressed):
        up = keys_pressed[pygame.K_UP]
        down = keys_pressed[pygame.K_DOWN]

        if up and not down:
            if self.vy > 0:
                self.vy = 0.0          # cancel leftover downward speed
            self.vy -= THRUST
        elif down and not up:
            if self.vy < 0:
                self.vy = 0.0          # cancel leftover upward speed
            self.vy += THRUST
        else:
            self.vy *= DRAG            # slow down smoothly
            if abs(self.vy) < 0.05:
                self.vy = 0.0

        self.vy = max(-MAX_SPEED, min(MAX_SPEED, self.vy))

    def update(self, height_bound):
        self.y += self.vy

        half = self.height / 2
        if self.y < half:                   # top edge
            self.y = half
            self.vy = 0
        elif self.y > height_bound - half:  # bottom edge
            self.y = height_bound - half
            self.vy = 0

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )