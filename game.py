import sys
import random

import pygame

from classes import Stone, StaticStone, Knight, Trap

pygame.init()

clock = pygame.time.Clock()
fps = 60

SCREEN_WIDTH = 800
SCRENN_HEIGHT = 580

screen = pygame.display.set_mode((SCREEN_WIDTH, SCRENN_HEIGHT))
pygame.display.set_caption('Runner')


# Загрузка изображений
background = pygame.image.load('static/image/background_2.jpg')
background_button = pygame.image.load('static/image/background.jpg')
ground = pygame.image.load('static/image/ground.png')
game_over = pygame.image.load('static/image/game_over.jpg')


run_game = False  # Запуск игры
run_button_start = True  # Запуск главного меню


static_stone_group = pygame.sprite.Group()
static_stone = StaticStone(600, 500)
static_stone_group.add(static_stone)

stone_group = pygame.sprite.Group()
stone_sp = Stone()
stone_group.add(stone_sp)

trap_group = pygame.sprite.Group()
trap = Trap(800, 430)
trap_group.add(trap)

knight_group = pygame.sprite.Group()
knight = Knight(100, 400)
knight_group.add(knight)


def start_window():  # Главное меню
    global run_game, run_button_start

    font = pygame.font.Font(None, 24)
    button_surface = pygame.Surface((150, 50))
    text = font.render("Начало игры", True, (0, 0, 0))
    text_rect = text.get_rect(
        center=(button_surface.get_width() / 2,
                button_surface.get_height() / 2))
    button_rect = pygame.Rect(330, 500, 150, 50)

    while run_button_start:
        clock.tick(60)
        screen.blit(background_button, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    run_button_start = False
                    run_game = True

        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(button_surface, (237, 64, 2), (1, 1, 148, 48))

        else:
            pygame.draw.rect(button_surface, (156, 143, 138), (1, 1, 148, 48))

        button_surface.blit(text, text_rect)
        screen.blit(button_surface, (button_rect.x, button_rect.y))
        pygame.display.update()


def game():  # Главный функционал игры
    global run_game
    GROUND_SPEED = 7
    render_offset = [0, 0]
    ground_scroll = 0
    screen_shake = 0

    while run_game:
        clock.tick(fps)

        screen.blit(background, (0, 0))
        screen.blit(ground, (ground_scroll, 188))

        ground_scroll -= GROUND_SPEED
        trap_group.draw(screen)
        trap_group.update()

        if knight.rect.bottomright[1] > static_stone.rect.bottomright[1]+20:
            static_stone_group.draw(screen)
            static_stone_group.update()
            stone_group.draw(screen)
            stone_group.update()
            knight_group.draw(screen)
            knight_group.update()
        else:
            knight_group.draw(screen)
            knight_group.update()
            static_stone_group.draw(screen)
            static_stone_group.update()
            stone_group.draw(screen)
            stone_group.update()

        if abs(ground_scroll) > 3160:
            ground_scroll = 0

        if stone_sp.count == 1:
            if (
                knight.rect.x > stone_sp.rect.x - 60
                and knight.rect.x < stone_sp.rect.x + 60
                and knight.rect.y > stone_sp.rect.y + 30
                and knight.rect.y < stone_sp.rect.y + 30
            ):
                run_game = False

            stone_sp.direction_stone = knight.rect.x / 150
            screen_shake = 30
            static_stone.rect.x = stone_sp.rect.x
            static_stone.rect.y = stone_sp.rect.y

        if (
            not knight.knight_jump and
            knight.rect.right - 80 > trap.rect.left and
            knight.rect.left < trap.rect.right and
            knight.rect.bottomright[1] - 15 < trap.rect.bottomleft[1] and
            knight.rect.bottomright[1] - 25 > trap.rect.topleft[1]
        ):
            run_game = False

        if (
            knight.rect.right - 80 > static_stone.rect.left and
            knight.rect.left < static_stone.rect.right and
            (knight.rect.bottomright[1] - 15 <
             static_stone.rect.bottomleft[1]
             ) and
            (knight.rect.bottomright[1] + 15 >
             static_stone.rect.bottomleft[1]
             )
        ):
            run_game = False

        if screen_shake > 0:
            screen_shake -= 1

        if screen_shake:
            render_offset[0] = random.randint(0, 8) - 4
            render_offset[1] = random.randint(0, 8) - 4

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()

        screen.blit(
            pygame.transform.scale(
                screen, (SCREEN_WIDTH, SCRENN_HEIGHT)
            ), render_offset
        )
        pygame.display.update()


def game_over_window():  # Функция окончания игры и перезапуска
    global run_game
    run_game_over_window = True

    font = pygame.font.Font(None, 24)
    button_surface = pygame.Surface((150, 50))
    text = font.render("Начать заново", True, (0, 0, 0))
    text_rect = text.get_rect(
        center=(button_surface.get_width() / 2,
                button_surface.get_height() / 2))
    button_rect = pygame.Rect(330, 500, 150, 50)

    while run_game_over_window:
        clock.tick(fps)
        screen.blit(game_over, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game_over_window = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    knight.rect.x = 100
                    trap.rect.x = 800
                    static_stone.rect.x = 700
                    stone_sp.count = 1
                    run_game = True
                    run_game_over_window = False
                    game()

        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(button_surface, (237, 64, 2), (1, 1, 148, 48))

        else:
            pygame.draw.rect(button_surface, (156, 143, 138), (1, 1, 148, 48))

        button_surface.blit(text, text_rect)
        screen.blit(button_surface, (button_rect.x, button_rect.y))
        pygame.display.update()


while True:
    start_window()
    game()
    game_over_window()
