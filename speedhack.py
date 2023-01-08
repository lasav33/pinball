import pygame


class Speedhack(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/speedhack.png')
        self.image = pygame.transform.scale(self.image, (50, 20))
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def checker(self, ball):
        return pygame.sprite.collide_rect(self, ball)

    def updateVel(self, ball):
        if ball.yvel < 0:
            return ball.xvel, ball.yvel * 1.1
        if ball.yvel > 0:
            return ball.xvel, ball.yvel * 0.9
