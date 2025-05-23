# game.py with full features

import pygame
import random
from settings import *

class Game:
    def __init__(self, screen):
        pygame.mixer.init()

        self.screen = screen
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()

        self.bg_img = pygame.image.load("assets/background.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (WIDTH, HEIGHT))

        self.flap_sound = pygame.mixer.Sound("assets/flap.wav")
        self.hit_sound = pygame.mixer.Sound("assets/hit.wav")

        self.bird_img = pygame.image.load("assets/bird.png").convert_alpha()
        self.bird_img = pygame.transform.scale(self.bird_img, (40, 40))

        self.pipe_img = pygame.image.load("assets/pipe.png").convert_alpha()
        self.pipe_img = pygame.transform.scale(self.pipe_img, (PIPE_WIDTH, 400))

        self.reset_game()

        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, PIPE_FREQUENCY_MS)

    def reset_game(self):
        self.bird_x = BIRD_START_X
        self.bird_y = BIRD_START_Y
        self.bird_velocity = 0
        self.pipes = []
        self.score = 0
        self.bird_rect = self.bird_img.get_rect(center=(self.bird_x, int(self.bird_y)))
        self.pipe_gap = PIPE_GAP
        self.game_over = False

    def draw_bird(self):
        angle = -self.bird_velocity * 3
        rotated_bird = pygame.transform.rotate(self.bird_img, angle)
        rect_for_blit = rotated_bird.get_rect(center=(self.bird_x, int(self.bird_y)))
        self.screen.blit(rotated_bird, rect_for_blit)

    def draw_pipe(self, rect, flipped=False):
        pipe_image = pygame.transform.flip(self.pipe_img, False, True) if flipped else self.pipe_img
        self.screen.blit(pipe_image, rect)

    def check_collision(self):
        for top_pipe, bottom_pipe in self.pipes:
            if self.bird_rect.colliderect(top_pipe) or self.bird_rect.colliderect(bottom_pipe):
                self.hit_sound.play() # Keep commented for now
                return True
        if self.bird_rect.top <= 0 or self.bird_rect.bottom >= HEIGHT:
               self.hit_sound.play() # Keep commented for now
               return True
        return False

    def show_main_menu(self):
        title = self.font.render("Flappy Bird", True, WHITE)
        prompt = self.font.render("Press SPACE to Start", True, WHITE)
        self.screen.blit(self.bg_img, (0, 0))
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 3)))
        self.screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.K_SPACE: # Changed to event.key == pygame.K_SPACE if it's a KEYDOWN
                    waiting = False
                # If still crashing here, ensure your main.py has pygame.init() and sets up the screen correctly.
                # Also, make sure show_main_menu() correctly handles waiting for input.
                # A common error is missing 'event.type == pygame.KEYDOWN'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False


    def show_game_over(self):
        game_over_text = self.font.render("Game Over", True, WHITE)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        retry_text = self.font.render("Press R to Retry or ESC to Exit", True, WHITE)

        self.screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3)))
        self.screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        self.screen.blit(retry_text, retry_text.get_rect(center=(WIDTH // 2, HEIGHT * 2 // 3)))
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()


    def run(self):
        self.show_main_menu()
        running = True

        while running:
            self.screen.blit(self.bg_img, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if not self.game_over:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.bird_velocity = JUMP_STRENGTH
                        self.flap_sound.play()  # Uncomment for sound

                    if event.type == self.SPAWNPIPE:
                        pipe_height = random.randint(100, HEIGHT - self.pipe_gap - 100)
                        top_pipe = pygame.Rect(WIDTH, 0, PIPE_WIDTH, pipe_height)
                        bottom_pipe = pygame.Rect(WIDTH, pipe_height + self.pipe_gap, PIPE_WIDTH, HEIGHT - pipe_height - self.pipe_gap)
                        top_pipe.scored = False
                        self.pipes.append((top_pipe, bottom_pipe))

            if not self.game_over:
                self.bird_velocity += GRAVITY
                self.bird_y += self.bird_velocity
                self.bird_rect.center = (self.bird_x, int(self.bird_y))
                print(f"Bird Position: {self.bird_rect.topleft}, Velocity: {self.bird_velocity}")

                self.draw_bird()

                for top_pipe, bottom_pipe in self.pipes:
                    top_pipe.x -= PIPE_VELOCITY
                    bottom_pipe.x -= PIPE_VELOCITY
                    self.draw_pipe(top_pipe, flipped=True)
                    self.draw_pipe(bottom_pipe)
                self.pipes = [p for p in self.pipes if p[0].right > 0]

                if self.check_collision():
                    print("Game Over Triggered")
                    self.game_over = True
                    self.show_game_over()

                for top_pipe, _ in self.pipes:
                    if self.bird_rect.left > top_pipe.right and not top_pipe.scored:
                        self.score += 1
                        top_pipe.scored = True
                        if self.pipe_gap > MIN_PIPE_GAP:
                            self.pipe_gap -= 5
                            if self.pipe_gap < MIN_PIPE_GAP:
                                self.pipe_gap = MIN_PIPE_GAP

                score_surface = self.font.render(f"Score: {self.score}", True, WHITE)
                self.screen.blit(score_surface, (10, 10))
            else:
                pass

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
        exit()
                  

    # def run(self):
    #     self.show_main_menu()
    #     running = True

    #     while running:
    #         self.screen.blit(self.bg_img, (0, 0))

    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 running = False

    #             if not self.game_over:
    #                 if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
    #                     self.bird_velocity = JUMP_STRENGTH
    #                     self.flap_sound.play() # Keep commented
    #                 # Comment out the SPAWNPIPE event temporarily
    #                 if event.type == self.SPAWNPIPE:
    #                     pipe_height = random.randint(100, HEIGHT - self.pipe_gap - 100)
    #                     top_pipe = pygame.Rect(WIDTH, 0, PIPE_WIDTH, pipe_height)
    #                     bottom_pipe = pygame.Rect(WIDTH, pipe_height + self.pipe_gap, PIPE_WIDTH, HEIGHT - pipe_height - self.pipe_gap)
    #                     top_pipe.scored = False
    #                     self.pipes.append((top_pipe, bottom_pipe))

    #         if not self.game_over:
    #             # --- Step 1: Comment out all game logic except bird movement and drawing ---
    #             self.bird_velocity += GRAVITY
    #             self.bird_y += self.bird_velocity
    #             self.bird_rect.center = (self.bird_x, int(self.bird_y))
    #             self.draw_bird()

    #             # Comment out pipes and collision for now
    #             for top_pipe, bottom_pipe in self.pipes:
    #                 top_pipe.x -= PIPE_VELOCITY
    #                 bottom_pipe.x -= PIPE_VELOCITY
    #                 self.draw_pipe(top_pipe, flipped=True)
    #                 self.draw_pipe(bottom_pipe)
    #             self.pipes = [p for p in self.pipes if p[0].right > 0]

    #             if self.check_collision():
    #                 self.game_over = True
    #                 self.show_game_over()

    #             for top_pipe, _ in self.pipes:
    #                 if self.bird_rect.left > top_pipe.right and not top_pipe.scored:
    #                     self.score += 1
    #                     top_pipe.scored = True
    #                     if self.pipe_gap > MIN_PIPE_GAP:
    #                         self.pipe_gap -= 5
    #                         if self.pipe_gap < MIN_PIPE_GAP:
    #                             self.pipe_gap = MIN_PIPE_GAP

    #             score_surface = self.font.render(f"Score: {self.score}", True, WHITE)
    #             self.screen.blit(score_surface, (10, 10))
    #         else:
    #             pass

    #         pygame.display.update()
    #         self.clock.tick(FPS)

    #     pygame.quit()
    #     exit()