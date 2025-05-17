import pygame.sprite


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        self.score = 0

        # load the images
        for num in range(1, 4):
            img = pygame.image.load(f'../images/bird{num}.png')
            self.images.append(img)

        # get the first image, make a rectangle around the bird and mark the centre
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        # control the velocity
        self.vel = 0
        self.gravity = 0.9
        self.flap_power = -6
        self.max_vel = 8
        self.min_vel = -10

    '''
    If bird is alive move the bird down, flap the bird by moving it up. Control the max-min on velocity. If bird is at 
    the top move the bird down. When the at the bottom kill the bird.
    '''
    def update(self, alive, flap_decision):
        if alive:
            self.vel += self.gravity

            if flap_decision == 1:
                self.vel = self.flap_power

            if self.vel > self.max_vel:
                self.vel = self.max_vel
            if self.vel < self.min_vel:
                self.vel = self.min_vel

            self.rect.y += int(self.vel)

            if self.rect.top < 0:
                self.rect.top = 0
                self.rect.y += self.max_vel

            if self.rect.bottom >= 600:
                self.rect.bottom = 600

            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0

            self.image = pygame.transform.rotate(self.images[self.index], (-2) * self.vel)

        else:
            self.image = self.images[0]

    '''increase score'''
    def increase_score(self):
        self.score += 1
