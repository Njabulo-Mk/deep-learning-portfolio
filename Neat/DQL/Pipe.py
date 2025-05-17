import pygame


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, pipe_gap):
        pygame.sprite.Sprite.__init__(self)
        # load image and create rectangle
        self.image = pygame.image.load('../images/pipe.png')
        self.rect = self.image.get_rect()

        # check if the top-pipe or the bottom-pipe is being made
        self.top_pipe = position
        # the gap between the two pipes
        self.gap = pipe_gap

        # if pos=1 keep the image and as is then make the pipe move up
        # otherwise make the pipe move down
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    '''
    This function moves the pipe and when off screen the pipe is removed
    '''
    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

    '''
    Get the center of the gap as a information for the neural network
    '''
    def get_gap_center(self):
        if self.top_pipe:
            return self.rect.bottom + (self.gap / 2)
        else:
            return self.rect.top - (self.gap / 2)
