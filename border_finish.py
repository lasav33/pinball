import pygame


class Border(pygame.sprite.Sprite):
    def __init__(self, x, y, widht, higth, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((widht, higth))
        self.color = color
        self.rect = pygame.Rect(x, y, widht, higth)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (0, 0, 500, 500), 5)

    def checker(self, ball):
        return not self.rect.colliderect(ball.rect)

    def updateVel(self, ball):
        if ball.rect.left < self.rect.left \
                or ball.rect.right > self.rect.right:
            return -ball.xvel * ball.coeff, ball.yvel
        elif ball.rect.top < self.rect.top:
            return ball.xvel, -ball.yvel * ball.coeff


class Finish(Border):
    def __init__(self, x, y, widht, higth, color):
        Border.__init__(self, x, y, widht, higth, color)
        self.image = pygame.Surface((widht, higth))
        self.image.fill(color)
        self.rect = pygame.Rect(x, y, widht, higth)

    def checker(self, ball):
        return not Border.checker(self, ball)

    def updateVel(self, ball):
        return



