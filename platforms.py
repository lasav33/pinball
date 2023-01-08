import pygame
import math


class Platforms(pygame.sprite.Sprite):
    def __init__(self, x, y, alpha):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/pright.png')
        self.image = pygame.transform.scale(self.image, (55, 35))
        self.image = pygame.transform.flip(self.image, alpha, False)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.degrees = 0
        self.ROTATION = False
        self.isLeft = alpha
        self.mid = self.rect.topright if self.isLeft else self.rect.topleft
        self.orig = self.image

    def rotation(self):
        old_degrees = self.degrees
        if self.ROTATION:
            if self.degrees > -60:
                self.degrees -= 10
        else:
            if self.degrees < 0:
                self.degrees += 10
        if old_degrees != self.degrees:
            self.image = pygame.transform.rotate(self.orig, -self.degrees if self.isLeft else self.degrees)
            width = self.orig.get_rect().width
            newX = self.mid[0] + width / 8 * math.sin(-math.radians(self.degrees)) * (-1 if self.isLeft else 1)
            newY = self.mid[1] - width * 1.5 * (1 - math.cos(math.radians(self.degrees)))
            self.rect = self.image.get_rect(topright=(newX, newY)) if self.isLeft else self.image.get_rect(
                topleft=(newX, newY))

    def checker(self, ball):
        return pygame.sprite.collide_mask(self, ball)

    def updateVel(self, ball):
        v = math.sqrt(ball.xvel ** 2 + ball.yvel ** 2) * ball.coeff + (5 if self.ROTATION else 0)
        alpha = math.radians(60) - math.atan(ball.xvel / ball.yvel)
        return v * math.cos(alpha) * (1 if self.isLeft else -1), -v * math.sin(alpha)
