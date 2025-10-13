import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
GREY = (180, 180, 180)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Initialize paddles and ball
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 10, 10, width, height)

        # Scores and settings
        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 3  # Default: best of 5 (3 wins)
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 50)

        # --- Load sounds ---
        try:
            self.sounds = {
                "paddle_hit": pygame.mixer.Sound("game/sounds/hit.wav"),
                "wall_bounce": pygame.mixer.Sound("game/sounds/wall.wav"),
                "score": pygame.mixer.Sound("game/sounds/score.wav"),
            }
        except FileNotFoundError:
            print("⚠️ Sound files not found. Continuing without sound.")
            self.sounds = {}

        self.ball.set_sounds(self.sounds)
        self.game_over = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if not self.game_over:
            # Player controls (Arrow keys + W/S)
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player.move(-self.player.speed, self.height)
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.player.move(self.player.speed, self.height)

    def update(self):
        if self.game_over:
            return

        # Move ball and check collisions
        self.ball.move(self.player, self.ai)

        # Scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            if "score" in self.sounds:
                self.sounds["score"].play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            if "score" in self.sounds:
                self.sounds["score"].play()
            self.ball.reset()

        # Check for winner
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            self.game_over = True

        # AI tracking
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Display scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        if self.game_over:
            self.show_replay_menu(screen)

    def show_replay_menu(self, screen):
        """Display replay options after game ends."""
        screen.fill((0, 0, 0))
        winner = "Player" if self.player_score > self.ai_score else "AI"
        title = self.large_font.render(f"{winner} Wins!", True, WHITE)
        screen.blit(title, (self.width // 2 - title.get_width() // 2, 150))

        options = [
            "Press 3 → Best of 3",
            "Press 5 → Best of 5",
            "Press 7 → Best of 7",
            "Press ESC → Exit",
        ]
        for i, text in enumerate(options):
            label = self.font.render(text, True, GREY)
            screen.blit(label, (self.width // 2 - label.get_width() // 2, 300 + i * 50))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    elif event.key == pygame.K_3:
                        self.start_new_game(2)
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.start_new_game(3)
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.start_new_game(4)
                        waiting = False

    def start_new_game(self, win_target):
        """Reset everything for a new game."""
        self.player_score = 0
        self.ai_score = 0
        self.winning_score = win_target
        self.ball.reset()
        self.game_over = False
