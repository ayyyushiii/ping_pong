import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.sounds = {}
        self.reset()

    def set_sounds(self, sounds):
        """Attach sound effects from GameEngine."""
        self.sounds = sounds

    def move(self, player=None, ai=None):
        # Move ball
        self.x += self.vx
        self.y += self.vy

        # Bounce off top/bottom
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.vy *= -1
            if "wall_bounce" in self.sounds:
                self.sounds["wall_bounce"].play()

        # Paddle collisions
        if player and self.rect().colliderect(player.rect()):
            self.x = player.x + player.width
            self.vx = abs(self.vx)
            if "paddle_hit" in self.sounds:
                self.sounds["paddle_hit"].play()

        if ai and self.rect().colliderect(ai.rect()):
            self.x = ai.x - self.width
            self.vx = -abs(self.vx)
            if "paddle_hit" in self.sounds:
                self.sounds["paddle_hit"].play()

    def reset(self):
        # Reset ball to center
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2
        self.vx = random.choice([-6, 6])
        self.vy = random.choice([-4, 4])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
