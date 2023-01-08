import pygame
import sys
import math
import random
import platforms
import border_finish
import rigth_left_border
import speedhack


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.yvel = 0
        self.xvel = 0
        self.coeff = 0.8
        self.onGround = False
        self.image = pygame.image.load('data/ball.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.mid = self.rect.center

    def update(self, left1, right1):
        self.yvel += GRAVITY
        self.collide()
        self.rect.y += self.yvel
        self.rect.x += self.xvel

    def collide(self):
        for object_in_game in objects:
            if object_in_game.checker(self):
                try:
                    self.xvel, self.yvel = object_in_game.updateVel(self)
                except TypeError:
                    global COUNT, COUNT_BEST
                    font1 = pygame.font.Font(None, 36)
                    text2 = font1.render(
                        'ВЫ ПРОИГРАЛИ', True, (255, 0, 0))
                    place2 = text2.get_rect()
                    place2.x = 135
                    place2.y = 250
                    screen.blit(text2, place2)
                    if int(COUNT_BEST) <= COUNT:
                        COUNT_BEST = str(COUNT)
                        font1 = pygame.font.Font(None, 36)
                        text2 = font1.render(
                            f'НОВЫЙ РЕКОРД {COUNT_BEST}', True, (0, 255, 0))
                        place2 = text2.get_rect()
                        place2.x = 125
                        place2.y = 300
                        screen.blit(text2, place2)
                        open('data/Best_count.txt', 'w').write(COUNT_BEST)


class Circle(pygame.sprite.Sprite):
    def __init__(self, x, y, image, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'data/{image}')
        self.image = pygame.transform.scale(self.image, size)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mid = self.rect.center
        self.name = image[6:]

    def checker(self, ball):
        return pygame.sprite.collide_mask(self, ball)

    def updateVel(self, ball):
        global COUNT
        COUNT += int(self.name[:-4])
        v = math.sqrt(ball.xvel ** 2 + ball.yvel ** 2) * ball.coeff
        ballCenter = ball.rect.center
        selfCenter = self.rect.center
        r = math.sqrt((ballCenter[1] - selfCenter[1]) ** 2 + (ballCenter[0] - selfCenter[0]) ** 2)
        r1 = (ball.rect.width + self.rect.width) / 2
        ball.rect.center = (self.rect.centerx + (ballCenter[0] - selfCenter[0]) * r1 / r,
                            self.rect.centery + (ballCenter[1] - selfCenter[1]) * r1 / r)

        beta = math.atan((ballCenter[1] - selfCenter[1]) / (ballCenter[0] - selfCenter[0])) if (ballCenter[0] -
                                                                                                selfCenter[
                                                                                                    0]) != 0 else math.radians(
            90)
        alpha = math.radians(90) - abs(beta)
        print(v * math.cos(alpha), v * math.sin(alpha))
        return v * math.cos(alpha), v * math.sin(alpha)


maps = ['    **    ',
        '          ',
        ' *      * ',
        '   *  *   ',
        '          ',
        '  +    +  ',
        '          ',
        '          ',
        '          ',
        '          ',
        ]
COUNT = 0
COUNT_BEST = open('data/Best_count.txt').read()

circle_list = ['circle25.png', 'circle50.png', 'circle100.png']
pygame.init()
size = 500, 500
y_pos = 450
x_pos = 270
GRAVITY = 0.35
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60
left = right = False
player = Ball(480, 300)
objects = []
rightpl = platforms.Platforms(265, 430, False)
objects.append(rightpl)
leftpl = platforms.Platforms(175, 430, True)
objects.append(leftpl)
rBord = rigth_left_border.Rigth_Left_Border(320, 330, False)
objects.append(rBord)
lBord = rigth_left_border.Rigth_Left_Border(0, 330, True)
objects.append(lBord)
redBorder = border_finish.Finish(10, 480, 480, 10, 'red')
objects.append(redBorder)
all_objects = pygame.sprite.Group()
all_objects.add(objects)
all_objects.add(player)
border = border_finish.Border(15, 15, 460, 460, 'white')
font = pygame.font.Font(None, 36)
text1 = font.render(
    COUNT_BEST, True, (0, 100, 0))
place1 = text1.get_rect()
place1.x = 450
place1.y = 10
font = pygame.font.Font(None, 36)
text = font.render(
    str(COUNT), True, (0, 100, 0))
place = text.get_rect()
place.x = 10
place.y = 10
circle_ob = []
for i in range(len(maps)):
    for j in range(len(maps[i]) - 1):
        if maps[i][j] == '+':
            mapobj = speedhack.Speedhack(j * 50, i * 50)
            all_objects.add(mapobj)
            objects.append(mapobj)
        if maps[i][j] == '*':
            if maps[i][j - 1] == '*':
                continue
            if maps[i][j + 1] == '*':
                mapobj = Circle(j * 50, i * 50, circle_list[random.randrange(len(circle_list))], (100, 100))
            else:
                mapobj = Circle(j * 50, i * 50, circle_list[random.randrange(len(circle_list))], (50, 50))
            all_objects.add(mapobj)
            circle_ob.append(mapobj)
            objects.append(mapobj)

objects.append(border)
GAME = True
while GAME:
    rightpl.ROTATION = False
    leftpl.ROTATION = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player.rect.x = 480
                player.rect.y = 300
                player.xvel = 0
                player.yvel = 0
                COUNT = 0
                COUNT_BEST = open('data/Best_count.txt').read()
    if pygame.key.get_pressed()[pygame.K_RCTRL]:
        rightpl.ROTATION = True
    if pygame.key.get_pressed()[pygame.K_LCTRL]:
        leftpl.ROTATION = True
    screen.fill('black')
    text = font.render(
        str(COUNT), True, (0, 100, 0))
    border.draw(screen)
    player.update(left, right)
    rightpl.rotation()
    leftpl.rotation()
    all_objects.draw(screen)
    screen.blit(text, place)
    screen.blit(text1, place1)
    clock.tick(fps)
    pygame.display.flip()
