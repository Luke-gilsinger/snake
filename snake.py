import pygame
import time
import random
pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 0)
light_red = (255, 0, 0)
light_green = (0, 255, 0)
blue = (50, 153, 213)
display = pygame.display
dis = display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Snake Game by Ultraprogamer and Lukeg007')
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

def text_objects(text, font, size, color):
    font = pygame.font.Font(font, size)
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message(msg, color, x, y, font, size):
    TextSurf, TextRect = text_objects(msg, font, size, color)
    TextRect.center = (x, y)
    dis.blit(TextSurf, TextRect)


def Your_score(score):
    message("Your Score: " + str(score), yellow, 25, 15, "comicsansms.ttf", 35)


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def food(color, x, y, get_snake_block):
    pygame.draw.rect(dis, color, [x, y, get_snake_block, get_snake_block])


def button(color, light_color, x, y, w, h, msg_color, msg):
    mouse = pygame.mouse.get_pos()
    message(msg, msg_color, (x+(w/2)), y+(h/2), 'bahnschrift.ttf', 20)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(dis, light_color, [x, y, w, h])
    else:
        pygame.draw.rect(dis, color, [x, y, w, h])


def intro(msg=None):
    game_intro = True
    dis = display.set_mode((0, 0), pygame.FULLSCREEN)
    dis_height = display.get_surface().get_height()
    dis_width = display.get_surface().get_width()
    while game_intro:
        dis.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.VIDEORESIZE:
                dictionary = event.dict
                dis_width = dictionary['w']
                dis_height = dictionary['h']
        if not msg is None:
            msg_txt = msg['txt']
            msg_x = msg['x']
            msg_y = msg['y']
            msg_color = msg['color']
            msg_font = msg['font']
            msg_size = msg['size']
            message(msg_txt, msg_color, msg_x, msg_y, msg_font, msg_size)
        message('Snake', black, dis_width / 2, dis_height / 2 - 150, 'comicsansms.ttf', 35)
        button(green, light_green, dis_width / 2 - 200, dis_height / 2 + 100, 100, 50, white, 'Play')
        button(red, light_red, dis_width / 2 + 100, dis_height / 2 + 50, 100, 50, white, 'Quit')
        pygame.display.update()
        clock.tick(15)


def gameLoop(dis):
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
        foodcords['x'][x] = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            intro(msg={'txt': 'You lost!', 'color': light_red, 'x': dis_width / 2, 'y': dis_height / 2 - 90, 'font': 'bahnschrift.ttf', 'size': 25})

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        for x in range(100):
            foodx = foodcords['x'][x]
            foody = foodcords['y'][x]
            food(green, foodx, foody, snake_block)
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
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
            cords_y = foodcords['y'][x]
            cords_x = foodcords['x'][x]
            if x1 == cords_x and y1 == cords_y:
                foodcords['y'][x] = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                foodcords['x'][x] = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop(display.set_mode((0, 0), pygame.FULLSCREEN))
