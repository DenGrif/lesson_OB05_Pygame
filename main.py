import pygame
import time

# Инициализация Pygame
pygame.init()

# Задаем параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Арканоид")

# Задаем цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Параметры платформы
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
paddle_speed = 10

# Параметры мяча
BALL_SIZE = 10
ball_speed = [4, -4]

# Параметры кирпичиков
BRICK_WIDTH = 75
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_GAP = 5

# Параметры игры
max_falls = 20  # Максимальное количество падений
falls = 0  # Счётчик падений
brick_move_time = 10000  # Время через которое кирпичики опускаются (в миллисекундах)
last_brick_move = pygame.time.get_ticks()  # Время последнего опускания кирпичиков
game_start_time = time.time()  # Время начала игры
game_over = False
game_result = ""
game_end_time = None  # Время окончания игры

# Определение объектов платформы, мяча и кирпичиков
paddle = pygame.Rect((SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 40), (PADDLE_WIDTH, PADDLE_HEIGHT))
ball = pygame.Rect((SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2), (BALL_SIZE, BALL_SIZE))

bricks = []
for row in range(BRICK_ROWS):
    brick_row = []
    for col in range(BRICK_COLS):
        brick_x = col * (BRICK_WIDTH + BRICK_GAP) + BRICK_GAP
        brick_y = row * (BRICK_HEIGHT + BRICK_GAP) + BRICK_GAP
        brick = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)
        brick_row.append(brick)
    bricks.append(brick_row)


# Функция для вывода текста
def draw_text(text, custom_font, color, x, y):
    rendered_text = custom_font.render(text, True, color)
    screen.blit(rendered_text, (x, y))


# Основной игровой цикл
running = True
while running:
    screen.fill(BLACK)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Если игра закончилась, выводим результаты и не обновляем логику игры
    if game_over:
        end_game_font = pygame.font.SysFont("Arial", 26)

        # Если время окончания игры ещё не зафиксировано, фиксируем его
        if game_end_time is None:
            game_end_time = time.time()

        elapsed_time = game_end_time - game_start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        draw_text(f"Игра окончена: {game_result}", end_game_font, WHITE, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3)
        draw_text(f"Количество пропущенных мячей: {falls}", end_game_font, WHITE, SCREEN_WIDTH // 4,
                  SCREEN_HEIGHT // 3 + 50)
        draw_text(f"Время игры: {minutes} мин {seconds} сек", end_game_font, WHITE, SCREEN_WIDTH // 4,
                  SCREEN_HEIGHT // 3 + 100)
        pygame.display.flip()
        continue

    # Управление платформой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-paddle_speed, 0)
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.move_ip(paddle_speed, 0)

    # Движение мяча
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Столкновение мяча со стенками
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]
    if ball.bottom >= SCREEN_HEIGHT:
        falls += 1  # Увеличиваем счетчик падений
        if falls >= max_falls:
            game_result = "Вы проиграли! Мяч упал 20 раз."
            game_over = True  # Игра заканчивается
        else:
            ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2  # Перезапуск мяча
            ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
            ball_speed = [4, -4]  # Сброс скорости

    # Столкновение мяча с платформой
    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]

    # Столкновение мяча с кирпичиками
    for row in bricks:
        for brick in row:
            if ball.colliderect(brick):
                ball_speed[1] = -ball_speed[1]
                row.remove(brick)
                break

    # Проверка на окончание игры (все кирпичики разбиты)
    bricks_left = sum(len(row) for row in bricks)
    if bricks_left == 0:
        game_result = "Поздравляем! Вы разбили все кирпичики!"
        game_over = True  # Завершение игры

    # Проверка, достигли ли кирпичики платформы (проигрыш)
    for row in bricks:
        for brick in row:
            if brick.bottom >= paddle.top:
                game_result = "Вы проиграли! Кирпичики достигли платформы."
                game_over = True  # Завершение игры

    # Отрисовка объектов
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, RED, ball)

    for row in bricks:
        for brick in row:
            pygame.draw.rect(screen, BLUE, brick)

    # Проверка времени для опускания кирпичиков
    current_time = pygame.time.get_ticks()
    if current_time - last_brick_move > brick_move_time:
        for row in bricks:
            for brick in row:
                brick.move_ip(0, BRICK_HEIGHT + BRICK_GAP)  # Опускаем кирпичики на уровень вниз
        last_brick_move = current_time  # Обновляем время последнего движения кирпичиков

    # Обновление экрана
    pygame.display.flip()

    # Задержка для 60 FPS
    pygame.time.delay(12)

# Завершение работы Pygame
pygame.quit()
