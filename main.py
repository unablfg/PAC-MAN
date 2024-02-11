import sys
import pygame
from game_sizes import CELL_SIZE, TOP_MARGIN
from game import Game

while True:
    if __name__ == '__main__':
        pygame.init()

        size = width, height = 28 * CELL_SIZE, 31 * CELL_SIZE + TOP_MARGIN
        SCREEN = pygame.display.set_mode(size)
        SCREEN.fill((0, 0, 0))

        GAME = Game(SCREEN)
        GAME.start(size)
        pygame.time.set_timer(GAME.OPEN_DOORS_EVENT, 3000)

        while not GAME.restart_flag:
            SCREEN.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == GAME.PACKMAN_MOVE_EVENT:
                    GAME.update_packman()
                    if GAME.packman.boost_mode:
                        GAME.packman_boost_mode_counter += 1
                        if GAME.packman_boost_mode_counter == 90:
                            for ghost in GAME.ghosts:
                                if ghost.mode == 'FRIGHT':
                                    ghost.mode = 'HARASSMENT'
                            GAME.packman_boost_mode_counter = 0
                            GAME.packman.boost_mode = False
                            GAME.eaten_ghosts = 0
                            pygame.time.set_timer(event, 90)
                if event.type == GAME.OPEN_DOORS_EVENT:
                    GAME.board[12][13:15] = 0, 0
                if event.type == GAME.GHOST_EVENT:
                    GAME.update_ghosts()
                if event.type == GAME.FRUIT_EXISTENCE_TIMER:
                    GAME.fruits_sprites.empty()
                    GAME.fruit = None
                    pygame.time.set_timer(GAME.FRUIT_EXISTENCE_TIMER, 0)

            GAME.render()
            pygame.display.flip()

        pygame.quit()
