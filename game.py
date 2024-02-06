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


