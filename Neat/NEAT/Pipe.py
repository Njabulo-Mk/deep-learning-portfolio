import pygame.sprite


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, pipe_gap):
        pygame.sprite.Sprite.__init__(self)
        # load images set rectangle around the pipe
        self.image = pygame.image.load('../images/pipe.png')
        self.rect = self.image.get_rect()
        # save pipe gap and if the position of the pipe is the top or bottom
        self.gap = pipe_gap
        self.top_pipe = position

        # flip the image if top and make the gap
        if position:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]
        if not position:
            self.rect.topleft = [x, y + int(pipe_gap/2)]


    '''
    move the pipe to the right and remove the pipe
    '''
    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

    '''get the centre and move up or down depending of the pipe type'''
    def get_gap_center(self):
        if self.top_pipe:
            return self.rect.bottom + (self.gap / 2)
        else:
            return self.rect.top - (self.gap / 2)

