import pygame
import random
pygame.init()

# Розміри екрану
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("шутер")

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Гравець
player_width, player_height = 50, 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# bulets
bullet_width, bullet_height = 5, 10
bullets = []
bullet_fired = False  # Для контролю, щоб пуля не летіла стрімко

# Вороги
enemy_width, enemy_height = 50, 50
enemies = []

# Швидкість гри
clock = pygame.time.Clock()

# Лічильник вбитих ворогів
kill_count = 0

def create_enemy():
    x = random.randint(0, WIDTH - enemy_width)
    y = random.randint(-150, -enemy_height)
    speed = random.randint(2, 5)  # Різна швидкість ворогів
    direction = random.choice([-1, 1])  # Випадковий напрямок для зигзагу
    enemies.append({"rect": pygame.Rect(x, y, enemy_width, enemy_height), "speed": speed, "direction": direction})

def move_bullets():
    global bullets, bullet_fired
    for bullet in bullets:
        bullet.y -= 10
        if bullet.y < 0:
            bullets.remove(bullet)
    
    # Дозволяємо стріляти тільки після того, як пуля вийде з екрану
    bullet_fired = False

def move_enemies():
    global enemies
    for enemy in enemies:
        enemy["rect"].y += enemy["speed"]
        enemy["rect"].x += enemy["direction"] * 3  # Зигзагообразний рух

        # Перевірка меж екрану для ворога
        if enemy["rect"].x <= 0 or enemy["rect"].x >= WIDTH - enemy_width:
            enemy["direction"] *= -1  # Змінюємо напрямок, коли ворог досягає межі

        # Якщо ворог досягає низу екрану, видаляємо його
        if enemy["rect"].y > HEIGHT:
            enemies.remove(enemy)

def check_collisions():
    global bullets, enemies, kill_count
    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy["rect"]):
                bullets.remove(bullet)
                enemies.remove(enemy)
                kill_count += 1
                break

# Основний цикл гри
running = True
while running:
    screen.fill(BLACK)
    
    # Обробка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not bullet_fired:
            bullets.append(pygame.Rect(player_x + player_width // 2 - bullet_width // 2, player_y, bullet_width, bullet_height))
            bullet_fired = True  # Встановлюємо, що пуля була випущена

    # Управління гравцем
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Створення ворогів
    if random.randint(1, 50) == 1:
        create_enemy()

    # Рух куль і ворогів
    move_bullets()
    move_enemies()
    
    # Перевірка на зіткнення
    check_collisions()

    # Малюємо гравця
    pygame.draw.rect(screen, WHITE, pygame.Rect(player_x, player_y, player_width, player_height))

    # Малюємо кулі
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    # Малюємо ворогів
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy["rect"])

    # Виводимо лічильник вбитих ворогів
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Вбиті вороги: {kill_count}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()