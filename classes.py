import random

import pygame


class Knight(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.count = 0
        self.count_jump = 0
        for num in range(1, 4):
            img = pygame.image.load(f"static/image/knight/knight_{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.knight_position = 0
        self.knight_jump = False

    def update(self):
        self.count += 1
        knight_cooldown = 5

        if pygame.key.get_pressed()[pygame.K_RIGHT] and self.rect.x <= 650:
            self.rect.x += 7

        if pygame.key.get_pressed()[pygame.K_LEFT] and self.rect.x >= 0:
            self.rect.x -= 7

        if pygame.key.get_pressed()[pygame.K_UP] and self.rect.y >= 330:
            self.rect.y -= 1

        if pygame.key.get_pressed()[pygame.K_DOWN] and self.rect.y <= 470:
            self.rect.y += 1

        if pygame.key.get_pressed()[pygame.K_SPACE] and not self.knight_jump:
            self.knight_position = self.rect.y
            self.rect.y -= 20
            self.knight_jump = True
            self.count_jump = 45

        if self.count_jump != 0:
            self.count_jump -= 1

            if self.count_jump == 1:
                self.knight_jump = False
                self.rect.y = self.knight_position

        if self.count > knight_cooldown and not self.knight_jump:
            self.count = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]


class Trap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("static/image/trap.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        if self.rect.x > -100:
            self.rect.x -= 7
        else:
            self.rect.y = random.randint(400, 470)
            self.rect.x = 800


class Stone(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.count_img = 0

        for num in range(1, 4):
            img = pygame.image.load(f"static/image/stone/stone_{num}.png")
            self.images.append(img)

        self.rect = self.images[0].get_rect()
        self.image = self.images[self.index]
        self.count = 150
        self.stone_size = 100
        self.direction_stone = 0
        self.rect.y = 136
        self.rect.x = 50

    def update(self):
        self.count_img += 1
        self.cooldown = 10

        if self.count == 1:
            self.stone_size = 100
            self.count = 150
            self.rect.x = 100
            self.rect.x = 50
            self.rect.y = 136

        if self.count_img > self.cooldown:
            self.count_img = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0

        if self.count > 1:
            scale = pygame.transform.scale(
                self.images[self.index],
                (
                    self.images[0].get_width() // self.stone_size,
                    self.images[0].get_width() // self.stone_size,
                ),
            )
            self.stone_size -= 0.6
            self.count -= 1
            self.rect.x += self.direction_stone

            if self.count > 120:
                self.rect.y -= 3
            elif self.count > 100:
                self.rect.y -= 2
            elif self.count > 88:
                self.rect.y -= 1
            elif self.count > 74:
                self.rect.y += 1
            elif self.count > 62:
                self.rect.y += 2
            elif self.count > 50:
                self.rect.y += 3
            else:
                self.rect.y += random.randint(3, 12)

        self.image = scale


class StaticStone(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("static/image/stone/stone_1.png")
        self.image = pygame.transform.scale(
            self.image, (
                self.image.get_width() // 12, self.image.get_width() // 12
            )
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 7
