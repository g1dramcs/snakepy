import pygame
import random
import os

pygame.init()

# Setting screen
screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
grey = (100, 100, 100)

# Speed
clock = pygame.time.Clock()
snake_block = 20
snake_speed = 15

# Font
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Record File
record_file = 'snake_records.txt'

def get_player_name():
    screen.fill(blue)
    message("Enter Your Name: ", white)
    pygame.display.update()
    
    player_name = ""
    name_entered = False

    while not name_entered:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_name != "":
                        name_entered = True
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        screen.fill(blue)
        message("Enter Your Name: " + player_name, white)
        pygame.display.update()
    
    return player_name

def save_record(name, score):
    with open(record_file, 'a') as file:
        file.write(f'{name}:{score}\n')

def load_records():
    if not os.path.exists(record_file):
        return []

    with open(record_file, 'r') as file:
        records = [line.strip().split(':') for line in file.readlines()]
        return [(name, int(score)) for name, score in records]

def display_records():
    records = load_records()
    records.sort(key=lambda x: x[1], reverse=True)
    top_records = records[:10]  # Showing only top-10 records

    screen.fill(blue)
    y_offset = 50
    for i, (name, score) in enumerate(top_records):
        record_text = f"{i + 1}. {name}: {score}"
        value = score_font.render(record_text, True, white)
        screen.blit(value, [screen_width / 4, y_offset])
        y_offset += 40

    pygame.display.update()
    wait_for_key()

# Exit function
def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, black, [x[0], x[1], snake_block, snake_block])

# Function for render text messages
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [screen_width / 6, screen_height / 3])

#Score counter
def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, grey)
    screen.blit(value, [10, 10])

# Function for draw walls
def draw_walls(walls):
    for wall in walls:
        pygame.draw.rect(screen, grey, wall)

# Function with walls coord and sizes
def get_walls(level):
    if level == 1:
        walls = []
    elif level == 2:
        walls = [
            pygame.Rect(100, 100, 600, 20),
            pygame.Rect(100, 480, 600, 20)
        ]
    elif level == 3:
        walls = [
            pygame.Rect(100, 100, 600, 20),
            pygame.Rect(100, 480, 600, 20),
            pygame.Rect(100, 100, 20, 300),
            pygame.Rect(680, 100, 20, 300)
        ]
    elif level == 4:
        walls = [
            pygame.Rect(0, 200, 600, 20),
            pygame.Rect(200, 400, 600, 20)
        ]
    elif level == 5:
        walls = [
            pygame.Rect(200, 60, 20, 540),
            pygame.Rect(600, 0, 20, 540)
        ]
    elif level == 6:
        walls = [
            pygame.Rect(100, 100, 600, 20),
            pygame.Rect(100, 480, 600, 20),
            pygame.Rect(20, 140, 20, 320),
            pygame.Rect(760, 140, 20, 320),
            pygame.Rect(200, 300, 400, 20)
        ]
    return walls

def generate_food(snake_block, walls, snake_List):
    while True:
        foodx = round(random.randrange(0, screen_width - snake_block*2) / 20.0) * 20.0
        foody = round(random.randrange(0, screen_height - snake_block*2) / 20.0) * 20.0
        food_rect = pygame.Rect(foodx, foody, snake_block, snake_block)
        collision = False
        for wall in walls:
            if wall.colliderect(food_rect):
                collision = True
                break
        for segment in snake_List:
            if pygame.Rect(segment[0], segment[1], snake_block, snake_block).colliderect(food_rect):
                collision = True
                break
        if not collision:
            return foodx, foody

def gameLoop():
    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    score = 0
    level = 1
    walls = get_walls(level)
    foodx, foody = generate_food(snake_block, walls, snake_List)

    while not game_over:
        while game_close:
            screen.fill(blue)
            message("You Lost! Q-Quit C-Restart R-Records", red)
            your_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        player_name = get_player_name()
                        save_record(player_name, score)
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                    if event.key == pygame.K_r:
                        display_records()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
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

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True

        for wall in walls:
            if wall.collidepoint(x1, y1):
                game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(white)
        pygame.draw.rect(screen, black, [0, 0, screen_width, screen_height], 5)
        draw_walls(walls)
        if score < 30:
            pygame.draw.rect(screen, green, [foodx, foody, snake_block, snake_block])
        elif score >= 30:
            pygame.draw.rect(screen, red, [foodx, foody, snake_block, snake_block])
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
        your_score(score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(snake_block, walls, snake_List)
            Length_of_snake += 1
            score += 1

            if score in [5, 10, 25, 50, 100]:
                level += 1
                walls = get_walls(level)

        clock.tick(snake_speed)

    pygame.quit()

gameLoop()

