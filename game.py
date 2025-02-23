import pygame 
import random 
import math

pygame.init()


WIDTH, HEIGHT = 800, 600 
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Шутер зі зміною зброї")


WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 
RED = (255, 0, 0)



player_width, player_height = 50, 50 
player_x = WIDTH // 2 - player_width // 2 
player_y = HEIGHT - player_height - 10 
player_speed = 5



bullets = [] 
weapon = 1  # Поточна зброя last_shot_time = {1: 0, 2: 0, 3: 0} cooldowns = {1: 0, 2: 1500, 3: 1000}  # Перезарядка в мілісекундах



enemy_width, enemy_height = 50, 50 
enemies = []



kill_count = 0



clock = pygame.time.Clock() 
font = pygame.font.SysFont(None, 36)

def create_enemy(): x = random.randint(0, WIDTH - enemy_width) 
y = random.randint(-150, -enemy_height) 
speed = random.randint(2, 5) 
direction = random.choice([-1, 1]) 
enemies.append({"rect": pygame.Rect(x, y, enemy_width, enemy_height), "speed": speed, "direction": direction})

def shoot(): 
    global bullets, last_shot_time, weapon 
    current_time = pygame.time.get_ticks()

# Якщо зброя ще перезаряджається – не стріляти
    if current_time - last_shot_time[weapon] < cooldowns[weapon]:
        return

    if weapon == 1:  # Базова куля
        bullet = {
        "rect": pygame.Rect(player_x + player_width // 2 - 2, player_y, 5, 10),
        "speed": 10,
        "angle": 90
    }
    bullets.append(bullet)

    elif weapon == 2:  # Повільна широка куля
    bullet = {
            "rect": pygame.Rect(player_x + player_width // 2 - 10, player_y, 20, 20),
            "speed": 6,
            "angle": 90
    }
    bullets.append(bullet)

    elif weapon == 3:  # Тройний постріл
    angles = [70, 90, 110]
    for angle in angles:
            bullet = {
            "rect": pygame.Rect(player_x + player_width // 2 - 2, player_y, 5, 10),
            "speed": 10,
            "angle": angle
        }
    bullets.append(bullet)

last_shot_time[weapon] = current_time

def move_bullets(): global bullets 
for bullet in bullets[:]: rad = math.radians(bullet["angle"]) 
bullet["rect"].x -= int(math.cos(rad) * bullet["speed"]) 
bullet["rect"].y -= int(math.sin(rad) * bullet["speed"]) if bullet["rect"].bottom < 0 or bullet["rect"].left < 0 or bullet["rect"].right > WIDTH: 
bullets.remove(bullet)

def move_enemies(): global enemies 
for enemy in enemies[:]: enemy["rect"].y += enemy["speed"] 
enemy["rect"].x += enemy["direction"] * 3

if enemy["rect"].x <= 0 or enemy["rect"].x >= WIDTH - enemy_width:
        enemy["direction"] *= -1  # Зміна напрямку при досягненні краю

if enemy["rect"].y > HEIGHT:
        enemies.remove(enemy)

def check_collisions(): global bullets, enemies, kill_count 
for bullet in bullets[:]: 
    for enemy in enemies[:]: 
        if bullet["rect"].colliderect(enemy["rect"]): bullets.remove(bullet) 
        enemies.remove(enemy) 
        kill_count += 1 
        break


running = True 
while running: screen.fill(BLACK)

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
            weapon = 1
        elif event.key == pygame.K_2:
            weapon = 2
        elif event.key == pygame.K_3:
            weapon = 3
        elif event.key == pygame.K_SPACE:
            shoot()

# Управління гравцем
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT] and player_x > 0:
    player_x -= player_speed
if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
    player_x += player_speed

# Створення ворогів
if random.randint(1, 50) == 1:
    create_enemy()

move_bullets()
move_enemies()
check_collisions()

# Малювання гравця
pygame.draw.rect(screen, WHITE, pygame.Rect(player_x, player_y, player_width, player_height))

# Малювання куль
for bullet in bullets:
    pygame.draw.rect(screen, WHITE, bullet["rect"])

# Малювання ворогів
for enemy in enemies:
    pygame.draw.rect(screen, RED, enemy["rect"])

# Лічильник вбитих ворогів
text = font.render(f"Вбиті вороги: {kill_count}", True, WHITE)
screen.blit(text, (10, 10))

# Оновлення екрану
pygame.display.flip()
clock.tick(60)

pygame.quit()