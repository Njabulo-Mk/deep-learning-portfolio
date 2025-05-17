import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
import os

from DQL.Bird import Bird
from DQL.DQNAgent import DQNAgent
from DQL.Pipe import Pipe

# start game
pygame.init()

# time game and frames-per-second
clock = pygame.time.Clock()
fps = 60

# size of the screen and set the name
screen_width = 571
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# font for the score
font = pygame.font.SysFont('Bauhaus 93', 60)
white = (255, 255, 255)

# set the back-ground and ground image
bg = pygame.image.load('../images/background.jpg')
ground_img = pygame.image.load('../images/ground.png')

# the speed of the ground, make the bird fly and the gap of the pipe
ground_scroll = 0
scroll_speed = 4
flying = True
pipe_gap = 200

# state_size = inputs and action_size = output.
state_size = 5
action_size = 2
batch_size = 64

# make agent
agent = DQNAgent(state_size, action_size)

scores = []
rewards = []
losses = []

# see if plots directory exists
if not os.path.exists('plots'):
    os.makedirs('plots')


'''
get the state: y-position, velocity, horizontal pipe, pipe-centre and centre-y distance
'''
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


'''
get reward when the bird is close to the centre
'''
def get_reward():
    if game_over:
        return -10
    else:
        pipe_center = pipe_group.sprites()[0].get_gap_center() if len(pipe_group) > 0 else 0
        distance_to_center = abs(flappy.rect.y - pipe_center)
        return 1 - (distance_to_center / screen_height)


'''
reset the bird and velocity
'''
def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    flappy.vel = 0
    return 0


'''
draw the score
'''
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# sprites for bird and pipe. Make the bird.
pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

# run - have the game start
# num_episodes - epochs
run = True
num_episodes = 1000

for episode in range(num_episodes):
    # frame-count - for online replay
    # reset, start game
    frame_count = 0
    print(episode)
    score = reset_game()
    game_over = False
    episode_reward = 0
    episode_loss = 0
    pipe_group.empty()
    last_pipe_x = screen_width

    # make the first pipe
    pipe_height = random.randint(-100, 100)
    btm_pipe = Pipe(500, int(screen_height / 2) + pipe_height, 1, pipe_gap)
    top_pipe = Pipe(500, int(screen_height / 2) + pipe_height, -1, pipe_gap)
    pipe_group.add(btm_pipe)
    pipe_group.add(top_pipe)

    # run the game
    while not game_over:
        clock.tick(fps)

        # when the window set to game over
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                game_over = True

        # draw the game
        screen.blit(bg, (0, 0))

        pipe_group.draw(screen)
        bird_group.draw(screen)
        bird_group.update(flying, game_over)

        screen.blit(ground_img, (ground_scroll, 600))

        # move the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        # get the state and choose an action
        state = get_state()

        action = agent.act(state)
        if action == 1:
            flappy.flap = True

        # check if the game meets the end condition
        if pygame.sprite.spritecollide(flappy, pipe_group, False):
            game_over = True
        if flappy.rect.bottom >= 600:
            game_over = True

        # reward for moving past the pipe and make pipes
        add = 0
        if len(pipe_group) == 0:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(500, int(screen_height / 2) + pipe_height, 1, pipe_gap)
            top_pipe = Pipe(500, int(screen_height / 2) + pipe_height, -1, pipe_gap)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)

        # check if the bird is in the pipes. once you move past the pipe then add the reward
        if len(pipe_group) > 0:
            if pipe_group.sprites()[0].rect.left < flappy.rect.left < pipe_group.sprites()[0].rect.right and not flappy.in_pipe:
                flappy.in_pipe = True

                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(500, int(screen_height / 2) + pipe_height, 1, pipe_gap)
                top_pipe = Pipe(500, int(screen_height / 2) + pipe_height, -1, pipe_gap)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)

            if flappy.in_pipe and flappy.rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                add = 10
                flappy.in_pipe = False

        # move the pipe group
        pipe_group.update(scroll_speed)

        # add the reward and tally the episode
        reward = get_reward() + add
        episode_reward += reward

        # next state and remember the state-actions
        next_state = get_state()
        agent.remember(state, action, reward, next_state, game_over)

        # make the online and offline replay
        frame_count += 1
        if len(agent.memory) > batch_size and frame_count % 32 == 0:
            loss = agent.replay(32)
            episode_loss += loss if loss is not None else 0

        draw_text(str(score), font, white, screen_width // 2, 30)

        pygame.display.update()

    agent.replay(128)

    # append score and draw images
    scores.append(score)
    rewards.append(episode_reward)
    losses.append(episode_loss / frame_count if frame_count > 0 else 0)

    if episode % 100 == 0:
        plt.figure(figsize=(10, 6))
        plt.subplot(3, 1, 1)
        plt.plot(scores, label='Score per Episode')
        plt.xlabel('Episode')
        plt.ylabel('Score')
        plt.legend()

        plt.subplot(3, 1, 2)
        plt.plot(rewards, label='Total Reward per Episode')
        plt.xlabel('Episode')
        plt.ylabel('Reward')
        plt.legend()

        plt.subplot(3, 1, 3)
        plt.plot(losses, label='Average Loss per Episode')
        plt.xlabel('Episode')
        plt.ylabel('Loss')
        plt.legend()

        plt.tight_layout()
        plt.savefig(f'plots/plot_episode_{episode}.png')
        plt.close()

agent.save("final_model_.weights.h5")
pygame.quit()
