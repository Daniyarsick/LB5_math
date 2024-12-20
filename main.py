import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 255, 0)
OBSTACLE_COLOR = (255, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Runner")
clock = pygame.time.Clock()

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 70)
        self.speed = 5
        self.jump_power = 15
        self.gravity = 1
        self.velocity = 0

    def update(self):
        # Гравитация
        self.velocity += self.gravity
        self.rect.y += self.velocity

        # Ограничение движения по вертикали
        if self.rect.bottom > HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.velocity = 0

    def jump(self):
        if self.rect.bottom == HEIGHT - 50:
            self.velocity = -self.jump_power

    def move_to_mouse(self, mouse_x):
        # Перемещение игрока к позиции мыши
        if mouse_x < self.rect.centerx:
            self.rect.x -= self.speed
        elif mouse_x > self.rect.centerx:
            self.rect.x += self.speed

        # Ограничение движения по горизонтали
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# Класс препятствий
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(OBSTACLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)
        self.rect.y = -30
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Создание игрока
player = Player()
all_sprites.add(player)

# Функция для создания препятствий
def create_obstacle():
    obstacle = Obstacle()
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

# Основной игровой цикл
running = True
score = 0
spawn_obstacle = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_obstacle, 1500)  # Создание препятствий каждые 1.5 секунды

while running:
    clock.tick(FPS)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == spawn_obstacle:
            create_obstacle()

    # Управление игроком с помощью мыши
    mouse_pos = pygame.mouse.get_pos()  # Получение позиции мыши
    player.move_to_mouse(mouse_pos[0])  # Перемещение игрока к позиции мыши по горизонтали

    # Проверка клика мыши для прыжка
    if pygame.mouse.get_pressed()[0]:  # Левая кнопка мыши
        player.jump()

    # Обновление спрайтов
    all_sprites.update()

    # Проверка столкновений
    if pygame.sprite.spritecollide(player, obstacles, False):
        print(f"Игра окончена! Ваш счёт: {score}")
        running = False

    # Увеличение счёта
    score += 1

    # Отрисовка
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()