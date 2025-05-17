import random
import numpy as np
import pygame
import matplotlib.pyplot as plt

from Pipe import Pipe
from Genome import Genome
from NEAT import speciated_offspring

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 571
screen_height = 700

pipe_gap = 200
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency

in_pipe = False

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird NEAT')

bg = pygame.image.load('../images/background.jpg')
ground_image = pygame.image.load('../images/ground.png')

ground_scroll = 0
ground_speed = 4

pipe_group = pygame.sprite.Group()

population_size = 50
population = [Genome() for _ in range(population_size)]

average_fitness_per_gen = []
average_distance_to_gap_per_gen = []

gen = 0
run = True
while run:
    clock.tick(fps)
    screen.blit(bg, (0, 0))

    pipe_group.draw(screen)
    screen.blit(ground_image, (ground_scroll, 600))

    current_gen_fitness = []
    current_gen_distance_to_gap = []

    if len(pipe_group) == 0:
        pipe_height = random.randint(-100, 100)
        btm_pipe = Pipe(300, int(screen_height / 2) + pipe_height, False, pipe_gap)
        top_pipe = Pipe(300, int(screen_height / 2) + pipe_height, True, pipe_gap)
        pipe_group.add(btm_pipe)
        pipe_group.add(top_pipe)
        last_pipe = pygame.time.get_ticks()
    else:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(300, int(screen_height / 2) + pipe_height, False, pipe_gap)
            top_pipe = Pipe(300, int(screen_height / 2) + pipe_height, True, pipe_gap)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

    for genome in population:
        if genome.alive:
            screen.blit(genome.bird.image, genome.bird.rect)

            if len(pipe_group) > 0:
                if pipe_group.sprites()[0].rect.left < genome.bird.rect.left < pipe_group.sprites()[0].rect.right and not genome.in_pipe:
                    genome.in_pipe = True
                    genome.fitness += 50

                if genome.in_pipe and genome.bird.rect.left > pipe_group.sprites()[0].rect.right:
                    genome.bird.increase_score()
                    genome.fitness += 100
                    genome.in_pipe = False

            if pygame.sprite.spritecollideany(genome.bird, pipe_group) or genome.bird.rect.bottom >= 600:
                genome.alive = False

            inputs = [
                genome.bird.rect.y,
                genome.bird.vel,
                pipe_group.sprites()[0].rect.x - genome.bird.rect.x,
                pipe_group.sprites()[0].get_gap_center(),
                pipe_group.sprites()[0].get_gap_center() - genome.bird.rect.y
            ]
            genome.update_bird(genome.alive, inputs)

            pipe = pipe_group.sprites()[0]

            gap_center = pipe.get_gap_center()
            distance_to_gap = abs(genome.bird.rect.centery - gap_center)
            current_gen_distance_to_gap.append(distance_to_gap)

            fitness = genome.fitness
            current_gen_fitness.append(fitness)

            if distance_to_gap < 100:
                genome.fitness += (100 - distance_to_gap) / 2

            pipe_distance = abs(pipe.rect.centerx - genome.bird.rect.centerx)
            if pipe_distance < 200:
                genome.fitness += (200 - pipe_distance) / 5

            if pipe.rect.right < genome.bird.rect.left:
                genome.fitness += 100

    ground_scroll -= ground_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0

    pipe_group.update(ground_speed)

    if all(not genome.alive for genome in population):
        if current_gen_fitness:
            avg_fitness = np.mean(current_gen_fitness)
            average_fitness_per_gen.append(avg_fitness)
            print(f'Generation {gen}: Average Fitness = {avg_fitness:.2f}')

        if current_gen_distance_to_gap:
            avg_distance_to_gap = np.mean(current_gen_distance_to_gap)
            average_distance_to_gap_per_gen.append(avg_distance_to_gap)
            print(f'Generation {gen}: Average Distance to Gap = {avg_distance_to_gap:.2f}')

        pipe_group.empty()
        gen += 1
        population = speciated_offspring(population, population_size, 0.6)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(average_fitness_per_gen, label='Average Fitness')
plt.xlabel('Generation')
plt.ylabel('Average Fitness')
plt.title('Average Fitness Over Generations')
plt.legend()
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(average_distance_to_gap_per_gen, label='Average Distance to Gap Center', color='orange')
plt.xlabel('Generation')
plt.ylabel('Average Distance to Gap Center')
plt.title('Average Distance to Gap Center Over Generations')
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig('fitness_and_distance_over_generations.png')

pygame.quit()
