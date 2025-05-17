import pygame
import random
import numpy as np

from DQL.Bird import Bird
from DQL.DQNAgent import DQNAgent
from DQL.Pipe import Pipe

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 571
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

font = pygame.font.SysFont('Bauhaus 93', 60)
white = (255, 255, 255)

bg = pygame.image.load('../images/background.jpg')
ground_img = pygame.image.load('../images/ground.png')

ground_scroll = 0
scroll_speed = 4
pipe_gap = 200

state_size = 5
action_size = 2

# make the agent
agent = DQNAgent(state_size, action_size)
agent.load("final_model_.weights.h5")
agent.epsilon = 0.01


def get_state():
    next_pipe = pipe_group.sprites()[0] if len(pipe_group) > 0 else None
    if next_pipe:
        inputs = [
            flappy.rect.y / screen_height,
            flappy.vel / flappy.max_vel,
            (next_pipe.rect.x - flappy.rect.x) / screen_width,
            next_pipe.get_gap_center() / screen_height,
            (next_pipe.get_gap_center() - flappy.rect.y) / screen_height
        ]
    else:
        inputs = [0, 0, 0, 0, 0]

    state = np.array(inputs)
    return state.reshape(1, 5)


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    flappy.vel = 0
    return 0


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

run = True
while run:
    score = reset_game()
    game_over = False
    pipe_group.empty()

    while not game_over:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                game_over = True

        screen.blit(bg, (0, 0))
        pipe_group.draw(screen)
        bird_group.draw(screen)
        bird_group.update(flying=True, game_over=game_over)
        screen.blit(ground_img, (0, 600))

        if len(pipe_group) == 0:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(400, int(screen_height / 2) + pipe_height, 1, pipe_gap)
            top_pipe = Pipe(400, int(screen_height / 2) + pipe_height, -1, pipe_gap)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)

        state = get_state()
        action = agent.act(state)

        if action == 1:
            flappy.flap = True

        if pygame.sprite.spritecollide(flappy, pipe_group, False):
            game_over = True
        if flappy.rect.bottom >= 600:
            game_over = True

        if len(pipe_group) > 0:
            if pipe_group.sprites()[0].rect.left < flappy.rect.left < pipe_group.sprites()[0].rect.right and not flappy.in_pipe:
                flappy.in_pipe = True

            if flappy.in_pipe and flappy.rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                flappy.in_pipe = False

        pipe_group.update(scroll_speed)
        draw_text(str(score), font, white, int(screen_width / 2), 30)
        pygame.display.update()

pygame.quit()
