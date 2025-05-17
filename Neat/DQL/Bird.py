import pygame


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        # index of the image and counter to control animation
        self.index = 0
        self.counter = 0

        # load images
        for num in range(1, 4):
            img = pygame.image.load(f'../images/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]

        # rectangle around the birds and mark the centre of the rectangle
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        # vel - how fast the velocity moving
        # gravity - how fast the bird falls
        # flap_strength - how much the bird moves up
        # min/max_vel - cap the velocity
        self.vel = 0
        self.gravity = 1.8
        self.flap_strength = -2.8
        self.max_vel = 10
        self.min_vel = -8
        self.angle = 0

        # check if bird in pipe and if to flap up or keep falling
        self.in_pipe = False
        self.flap = False

    '''
    This see if the bird is flying or not
    if not: then make the bird fall
    else: have the bird move up
    
    Draw the bird and if the bird is moving up or down tilt accordingly
    '''
    def update(self, flying, game_over):
        if flying:
            if not self.flap:
                self.vel += self.gravity * 0.6
            else:
                self.vel = self.vel * 0.6 + self.flap_strength * 0.4
                self.flap = False

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

        flap_cooldown = 5
        self.counter += 1

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        if not game_over:
            self.angle = max(-30, min(self.vel * -3, 45))
            self.image = pygame.transform.rotate(self.images[self.index], self.angle)
        else:
            self.image = self.images[0]
            self.angle = 0
