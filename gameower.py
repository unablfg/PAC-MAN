import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Создание окна
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game Over")

# Шрифт
font = pygame.font.Font(None, 30)

def show_game_over_dialog():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    restart_game()
                elif event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()

        window.fill(WHITE)

        # Рисуем текст диалогового окна
        game_over_text = font.render("GAME OVER", True, BLACK)
        window.blit(game_over_text, ((WINDOW_WIDTH - game_over_text.get_width()) // 2, 50))

        restart_text = font.render("1. Начать заново", True, BLACK)
        window.blit(restart_text, ((WINDOW_WIDTH - restart_text.get_width()) // 2, 100))

        exit_text = font.render("2. Выйти", True, BLACK)
        window.blit(exit_text, ((WINDOW_WIDTH - exit_text.get_width()) // 2, 150))

        pygame.display.update()

def restart_game():
    # Здесь должен быть ваш код для перезапуска игры
    pass 
