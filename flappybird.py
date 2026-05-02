import pygame
import random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


try:
    bg = pygame.image.load("background.png").convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
except:
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill((0, 0, 0))

pygame.display.set_caption("THE BIGGEST ALLIEN")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 40, bold=True)


hitsound = pygame.mixer.Sound("babax.mp3")
pygame.mixer.music.load("fon.mp3")
pygame.mixer.music.play(-1)

BIRD_SIZE = 50
try:
    BIRD_IMG = pygame.image.load("allien.png").convert_alpha()
    BIRD_IMG = pygame.transform.scale(BIRD_IMG, (BIRD_SIZE, BIRD_SIZE))
except:
    BIRD_IMG = pygame.Surface((BIRD_SIZE, BIRD_SIZE))
    BIRD_IMG.fill((255, 255, 0))


class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.6
        self.jump_strength = -8
        self.rect = BIRD_IMG.get_rect(center=(self.x, self.y))

    def jump(self):
        self.velocity = self.jump_strength

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        self.rect.center = (self.x, int(self.y))

    def draw(self):
        screen.blit(BIRD_IMG, self.rect)


class PipeManager:
    def __init__(self):
        self.pipes = []
        self.base_speed = 4
        self.speed = 4
        self.gap = 160
        self.spawn_timer = 0
        self.spawn_frequency = 90
        self.color = (176, 104, 9)

    def update(self, score):
        level = score // 10

        self.speed = self.base_speed + level

        self.spawn_frequency = max(40, 90 - (level * 5))

        self.spawn_timer += 1
        if self.spawn_timer > self.spawn_frequency:
            self.spawn_timer = 0
            pipe_y = random.randint(150, HEIGHT - 150)
            top = pygame.Rect(WIDTH, 0, 60, pipe_y - self.gap // 2)
            bottom = pygame.Rect(WIDTH, pipe_y + self.gap // 2, 60, HEIGHT)
            self.pipes.append({'top': top, 'bottom': bottom, 'passed': False})

        for pipe in self.pipes:
            pipe['top'].x -= self.speed
            pipe['bottom'].x -= self.speed

        self.pipes = [p for p in self.pipes if p['top'].right > 0]

    def draw(self):
        for pipe in self.pipes:
            pygame.draw.rect(screen, self.color, pipe['top'])
            pygame.draw.rect(screen, self.color, pipe['bottom'])


def main():
    bird = Bird()
    pipes = PipeManager()
    score = 0
    running = True
    game_over = False

    while running:
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_over:
                        bird.jump()
                    else:
                        bird = Bird()
                        pipes = PipeManager()
                        score = 0
                        game_over = False

        if not game_over:
            bird.update()
            pipes.update(score)

            if bird.rect.top < 0 or bird.rect.bottom > HEIGHT:
                game_over = True

            for pipe in pipes.pipes:
                if bird.rect.colliderect(pipe['top']) or bird.rect.colliderect(pipe['bottom']):
                    game_over = True

                if not pipe['passed'] and pipe['top'].right < bird.rect.left:
                    score += 1
                    pipe['passed'] = True

        pipes.draw()
        bird.draw()

        score_txt = font.render(str(score), True, (255, 255, 255))
        screen.blit(score_txt, (WIDTH // 2 - score_txt.get_width() // 2, 50))

        level_txt = font.render(f"Lvl: {score // 10}", True, (255, 255, 0))
        screen.blit(level_txt, (10, 10))

        if game_over:
            msg = font.render("ти програв!", True, (255, 50, 50))
            hint = pygame.font.SysFont("Arial", 25).render("пробіл - почати знову", True, (255, 255, 255))
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()