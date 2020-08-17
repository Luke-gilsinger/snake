import pygame
import time
from tkinter import *
import random
import intro_libs as il
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 0)
light_red = (255, 0, 0)
light_green = (0, 255, 0)
blue = (50, 153, 213)
light_blue = (0, 0, 255)
snake_block = 10
snake_speed = 15
snake_style = [red, light_blue, light_blue, light_blue, light_blue, red]
snake_style_pos = 0

def text_objects(text, font, size, color):
    font = pygame.font.Font(font, size)
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message(msg, color, x, y, font, size):
    TextSurf, TextRect = text_objects(msg, font, size, color)
    TextRect.center = (x, y)
    dis.blit(TextSurf, TextRect)


def Your_score(score):
    high_score_file = open('high_score.pyv', 'r')
    high_score = high_score_file.read().replace('\x00', '')
    print(high_score)
    high_score_file.close()
    message("Your Score: " + str(score), yellow, 110, 15, "comicsansms.ttf", 35)
    message("High Score: " + str(high_score), yellow, 110, 45, "comicsansms.ttf", 35)


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, x[2], [x[0], x[1], snake_block, snake_block])


def food(color, x, y, get_snake_block):
    pygame.draw.rect(dis, color, [x, y, get_snake_block, get_snake_block])


def gameLoop(dis, snake_style_pos, clock):
    dis_width, dis_height = dis.get_size()
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    foodcords = {'x': {}, 'y': {}}
    for x in range(100):
        foodcords['y'][x] = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        foodcords['x'][x] = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            pygame.quit()
            game_over = True
            break
        if game_over is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_d:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_w:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_s:
                        y1_change = snake_block
                        x1_change = 0

            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_close = True
            x1 += x1_change
            y1 += y1_change
            dis.fill(blue)
            for x in range(100):
                try:
                    foodx = foodcords['x'][x]
                    foody = foodcords['y'][x]
                except KeyError:
                    pass
                food(green, foodx, foody, snake_block)
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            style = snake_style[snake_style_pos]
            style_len = len(snake_style) - 1
            if style_len == snake_style_pos:
                snake_style_pos = 0
            elif style_len == 0:
                snake_style_pos = 1
            else:
                snake_style_pos = snake_style_pos + 1
            snake_Head.append(style)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            our_snake(snake_block, snake_List)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
            for x in range(100):
                try:
                    cords_y = foodcords['y'][x]
                    cords_x = foodcords['x'][x]
                except KeyError:
                    pass
                if x1 == cords_x and y1 == cords_y:
                    try:
                        del foodcords['y'][x]
                        del foodcords['x'][x]
                    except KeyError:
                        pass
                    Length_of_snake += 1
                    high_score_file = open('high_score.pyv', 'r+')
                    high_score = int(high_score_file.read().replace('\x00', ''))
                    if Length_of_snake - 1 > high_score:
                        high_score = high_score + 1
                        high_score_file.truncate(0)
                        high_score_file.write(str(high_score))
                    high_score_file.close()
            clock.tick(snake_speed)


il.intro(False)
while True:
    pygame.init()
    display = pygame.display
    dis = display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    gameLoop(display.set_mode((0, 0), pygame.FULLSCREEN), snake_style_pos, clock)
    il.intro(True)
