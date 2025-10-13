import pygame
import os
from game.paddle import Paddle
from game.ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Initialize mixer safely
        try:
            pygame.mixer.init()
        except Exception as e:
            print("⚠️ Audio initialization failed:", e)

        # Load sounds
        self.sound_hit = self.load_sound("hit.wav")
        self.sound_wall = self.load_sound("wall.wav")
        self.sound_score = self.load_sound("score.wav")

        # Paddles
        paddle_w, paddle_h = 10, 100
        self.player = Paddle(20, height // 2 - paddle_h // 2, paddle_w, paddle_h)
        self.ai = Paddle(width - 30, height // 2 - paddle_h // 2, paddle_w, paddle_h)

        # Ball
        ball_w, ball_h = 14, 14
        self.ball = Ball(width // 2, height // 2, ball_w, ball_h, width, height)

        # Scores
        self.player_score = 0
        self.ai_score = 0
        self.best_of = 5
        self.target_score = (self.best_of // 2) + 1

        # Fonts
        self.font = pygame.font.SysFont("Arial", 40)
        self.small_font = pygame.font.SysFont("Arial", 22)

        # Game state
        self.game_over = False
        self.waiting_for_replay_choice = False
        self.winner = None

    # -------------------- Load sound safely --------------------
    def load_sound(self, filename):
        """Load a sound from the sounds folder, or return None if missing."""
        try:
            path = os.path.join(os.path.dirname(__file__), "sounds", filename)
            if os.path.exists(path):
                return pygame.mixer.Sound(path)
            else:
                print(f"⚠️ Sound not found: {filename}")
                return None
        except Exception as e:
            print(f"⚠️ Error loading {filename}: {e}")
            return None

    # -------------------- Handle Input --------------------
    def handle_input(self, keys):
        """Player moves with UP/DOWN arrows."""
        if keys[pygame.K_UP]:
            self.player.move(-self.player.speed, self.height)
        if keys[pygame.K_DOWN]:
            self.player.move(self.player.speed, self.height)

    # -------------------- Update --------------------
    def update(self):
        if self.game_over:
            return

        prev_vx, prev_vy = self.ball.velocity_x, self.ball.velocity_y

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # Paddle collision sound (when direction changes horizontally)
        if self.ball.velocity_x != prev_vx:
            if self.sound_hit:
                self.sound_hit.play()

        # Wall bounce sound (when direction changes vertically)
        if self.ball.velocity_y != prev_vy:
            if self.sound_wall:
                self.sound_wall.play()

        # Scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            if self.sound_score:
                self.sound_score.play()
            self.ball.reset()

        elif self.ball.x >= self.width:
            self.player_score += 1
            if self.sound_score:
                self.sound_score.play()
            self.ball.reset()

        # AI follows ball
        self.ai.auto_track(self.ball, self.height)

        # Check for game over
        self.check_game_over()

    # -------------------- Game Over Check --------------------
    def check_game_over(self):
        if self.player_score >= self.target_score:
            self.winner = "PLAYER"
            self.game_over = True
        elif self.ai_score >= self.target_score:
            self.winner = "AI"
            self.game_over = True

        if self.game_over:
            self.show_game_over_screen()

    # -------------------- Game Over Screen --------------------
    def show_game_over_screen(self):
        surface = pygame.display.get_surface()
        surface.fill(BLACK)

        win_text = self.font.render(f"{self.winner} WINS!", True, WHITE)
        replay_text = self.small_font.render(
            "Press 3 / 5 / 7 for Best of 3 / 5 / 7, or ESC to Exit",
            True, WHITE
        )

        surface.blit(win_text, (self.width // 2 - win_text.get_width() // 2, self.height // 2 - 60))
        surface.blit(replay_text, (self.width // 2 - replay_text.get_width() // 2, self.height // 2 + 10))
        pygame.display.flip()

        self.waiting_for_replay_choice = True

    # -------------------- Render --------------------
    def render(self, screen):
        screen.fill(BLACK)

        # Draw paddles, ball, and middle line
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))
