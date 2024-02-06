import pygame
from borders import HorizontalBorder, VerticalBorder, RoundedBorder
from coin import Coin
from boost import Boost
from ghosts import Blinky, Pinky, Inky, Clyde
from packman import PackMan
from fruits import Fruits
from random import choice
from board import boards
from copy import deepcopy
from load_image_function import load_image

# Группы спрайтов для отрисовки и взаимодействий
packman_sprite = pygame.sprite.Group()
ghosts_sprites = pygame.sprite.Group()
coins_sprites = pygame.sprite.Group()
boosts_sprites = pygame.sprite.Group()
fruits_sprites = pygame.sprite.Group()


# Класс игры
class Game:
    GHOST_EVENT = pygame.USEREVENT + 1  # Таймер для обновления призраков
    PACKMAN_MOVE_EVENT = pygame.USEREVENT + 2  # Таймер для обновления пакмана
    OPEN_DOORS_EVENT = pygame.USEREVENT + 3  # Таймер для открытия дверей
    FRUIT_EXISTENCE_TIMER = pygame.USEREVENT + 4  # Таймер для существования фрукта

    def __init__(self, screen):
        self.width = 28
        self.height = 31
        self.board = deepcopy(boards)
        self.screen = screen
        self.packman = PackMan(packman_sprite)
        self.packman.parent_game = self
        self.blinky = Blinky(ghosts_sprites)
        self.pinky = Pinky(ghosts_sprites)
        self.inky = Inky(ghosts_sprites)
        self.clyde = Clyde(ghosts_sprites)
        self.points = 0  # Очки, заработанные пакманом
        self.lives = 3  # Жизни пакмана
        self.fruit = None  # Фрукт в игре(None, когда нету фрукта)
        self.fruit_type = 0  # Тип фрукта
        self.points_received_from_fruits = 0  # Очки, заработанные пакманом, сбьев фрукты
        # Очки, заработанные пакманом, не учитывая очки за фрукты, нужные для появления следующего фрукта
        self.fruit_levels = [170, 570, 1070]
        # Количество призраков, сьеденных пакманом за время действия энерджайзера
        self.eaten_ghosts = 0
        # Таймер тиков для буст-мода(максимум 90(то есть суммарно пакман будет бустанут в течении 90 * 70 секунд))
        self.packman_boost_mode_counter = 0
        # На месте, где пакман появиться, нету монетки
        self.board[self.packman.y][self.packman.x] = 0
        # Количество монеток и энерджайзеров суммарно (когда закончаться все монетки и энерджайзеры пакман выиграл
        self.items_count = 245
        # Все призраки
        self.ghosts = (self.blinky, self.pinky, self.inky, self.clyde)
        # Начальные настройки для призраков и определение их начальной картинки
        for ghost in self.ghosts:
            ghost.parent_game = self
            ghost.move(self.packman.get_position())
        for i in range(self.width):
            for j in range(self.height):
                if self.board[j][i] == 1:
                    Coin(i, j, coins_sprites)
                if self.board[j][i] == 2:
                    Boost(i, j, boosts_sprites)

        with open('high_score.txt', 'r') as file:
            self.high_score = int(file.read().strip())

        pygame.time.set_timer(Game.GHOST_EVENT, 100)
        pygame.time.set_timer(Game.PACKMAN_MOVE_EVENT, 90)

    def show_information(self):
        # Отображение HIGH SCORE, SCORE и количество жизней на экране
        self.show_text(28, f'SCORE: {str(self.points).zfill(5)}', (20, 9))
        self.show_text(28, f'HIGH SCORE: {str(self.high_score).zfill(5)}', (320, 9))
        for i in range(self.lives):
            heart = pygame.transform.scale(load_image('HEART.png'), (34, 34))
            self.screen.blit(heart, (7 + i * 40, 311))

    def show_text(self, font_size, string, position):
        # Метод для отображения текста
        font = pygame.font.Font('game_font/unicephalon.ttf', font_size)
        text = font.render(string, 1, (255, 255, 255))
        self.screen.blit(text, position)

    def start(self, size):
        # Отрисовка заставки
        background = pygame.transform.scale(load_image('BACKGROUND.jpg'), (size[0], size[0]))
        self.screen.blit(background, (0, 0))
        time_left = 3
        dots = 0
        dots_update_event = pygame.USEREVENT + 5
        pygame.time.set_timer(dots_update_event, 250)
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == dots_update_event:
                    if dots == 3:
                        dots = 0
                        time_left -= 1
                        if not time_left:
                            running = False
                            pygame.time.set_timer(dots_update_event, 0)
                            break
                    self.show_text(36, f'Before starting {time_left}{'.' * dots}', (110, 700))
                    dots += 1
            background = pygame.transform.scale(load_image('BACKGROUND.jpg'), (size[0], size[0]))
            self.screen.blit(background, (0, 0))
            pygame.display.flip()

    def game_over(self, win):
        if win:
            pass
        else:
            pass
        if self.points > self.high_score:
            with open('high_score.txt', 'r+') as file:
                file.truncate(0)
                file.write(str(self.points))
    def update_packman_direction(self):
        # Изменение направления движения пакмана
        if pygame.key.get_pressed()[pygame.K_w]:
            self.packman.change_direction('UP')
        if pygame.key.get_pressed()[pygame.K_a]:
            self.packman.change_direction('LEFT')
        if pygame.key.get_pressed()[pygame.K_s]:
            self.packman.change_direction('DOWN')
        if pygame.key.get_pressed()[pygame.K_d]:
            self.packman.change_direction('RIGHT')

    def render(self):
        # Отрисовка спрайтов
        global ghosts_sprites
        coins_sprites.draw(self.screen)
        boosts_sprites.draw(self.screen)
        if self.fruit is not None:
            fruits_sprites.draw(self.screen)
        ghosts_sprites.draw(self.screen)
        packman_sprite.draw(self.screen)
        for i in range(self.width):
            for j in range(self.height):
                if 9 > self.board[j][i] > 4:
                    RoundedBorder(i, j, self.board[j][i] - 4).draw(self.screen)
                if self.board[j][i] == 4:
                    HorizontalBorder(i, j).draw(self.screen)
                if self.board[j][i] == 3:
                    VerticalBorder(i, j).draw(self.screen)
        # Условие появления фрукта
        if (self.fruit_type < 3 and self.points - self.points_received_from_fruits > self.fruit_levels[
            self.fruit_type]):
            self.fruit = Fruits(choice([14, 13]), 17, self.fruit_type, fruits_sprites)
            self.fruit_type += 1
            pygame.time.set_timer(self.FRUIT_EXISTENCE_TIMER, 9600)
        # Условие возрождения призрака
        for ghost in self.ghosts:
            if ghost.mode == 'RETURNING_HOME' and ghost.get_position() == ghost.respawn_point:
                ghost.mode = 'HARASSMENT'
        # Столкновение пакмана с манеткой
        if pygame.sprite.spritecollide(self.packman, coins_sprites, True):
            self.points += 10
            self.items_count -= 1
        # Столкновение пакмана с энерджайзером
        if pygame.sprite.spritecollide(self.packman, boosts_sprites, True):
            self.points += 50
            self.items_count -= 1
            self.packman.boost_mode = True
            for ghost in self.ghosts:
                ghost.mode = 'FRIGHT'
            pygame.time.set_timer(Game.PACKMAN_MOVE_EVENT, 70)
        # Столкновение пакмана с фруктом
        if pygame.sprite.spritecollideany(self.packman, fruits_sprites):
            self.points += self.fruit.points
            self.points_received_from_fruits += self.fruit.points
            fruits_sprites.empty()
            self.fruit = None
            pygame.time.set_timer(self.FRUIT_EXISTENCE_TIMER, 0)
        # Столкновение пакмана с призраком
        if pygame.sprite.spritecollideany(self.packman, ghosts_sprites):
            if pygame.sprite.spritecollideany(self.packman, ghosts_sprites).mode != 'RETURNING_HOME':
                if self.packman.boost_mode:
                    pygame.sprite.spritecollideany(self.packman, ghosts_sprites).mode = 'RETURNING_HOME'
                    self.eaten_ghosts += 1
                    self.points += 2 ** self.eaten_ghosts * 100
                else:
                    self.lives -= 1
                    if self.lives:
                        ghosts_sprites.empty()
                        self.blinky = Blinky(ghosts_sprites)
                        self.pinky = Pinky(ghosts_sprites)
                        self.inky = Inky(ghosts_sprites)
                        self.clyde = Clyde(ghosts_sprites)
                        self.ghosts = (self.blinky, self.pinky, self.inky, self.clyde)
                        for ghost in self.ghosts:
                            ghost.parent_game = self
                            ghost.move(self.packman.get_position())
                    else:
                        self.game_over(False)
        # Если закончаться монетки и энерджайзеры - конец игры
        if not self.items_count:
            self.game_over(True)
        self.show_information()

    def update_ghosts(self):
        # Обновление призраков
        for ghost in self.ghosts:
            ghost.update(self.packman.get_position())

    def update_packman(self):
        # Обновление пакмана
        self.update_packman_direction()
        self.packman.update()


