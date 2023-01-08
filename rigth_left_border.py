import pygame
import math


class Rigth_Left_Border(pygame.sprite.Sprite):
    def __init__(self, x, y, alpha):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/rpl.png')
        self.image = pygame.transform.scale(self.image, (180, 120))
        self.image = pygame.transform.flip(self.image, alpha, False)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isLeft = alpha

    def checker(self, ball):
        return pygame.sprite.collide_mask(self, ball)

    def updateVel(self, ball):
        v = math.sqrt(ball.xvel ** 2 + ball.yvel ** 2) * ball.coeff
        alpha = math.radians(60) - math.atan(ball.xvel / ball.yvel)
        return v * math.cos(alpha) * (1 if self.isLeft else -1), -v * math.sin(alpha)
