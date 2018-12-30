import pygame
import random

WIDTH = 1000
HEIGHT = 700
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255,255, 255)

pygame.init()

screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ghost Shmup")

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerImg
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 8
        self.rect.centery = HEIGHT / 2
        self.speedy = 0
        self.speedx = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        self.flySpeed = 5
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.speedx = self.flySpeed
        if keystate[pygame.K_LEFT]:
            self.speedx = -self.flySpeed
        if keystate[pygame.K_UP]:
            self.speedy = -self.flySpeed
        if keystate[pygame.K_DOWN]:
            self.speedy = self.flySpeed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.top = HEIGHT
        if self.rect.bottom < 0:
            self.rect.bottom = 0
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.right)
        allSprites.add(bullet)
        bullets.add(bullet)



class badBirds(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = birdImg
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.rect.x = random.randrange(1050, 1500)
        self.speedx = random.randrange(1, 5)
        self.speedy = random.randrange(-3, 3)

    def update(self):
        self.rect.x -= self.speedx
        self.rect.y += self.speedy
        if self.rect.right < -10:
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.rect.x = random.randrange(1050, 1500)
            self.speedx = random.randrange(3, 5)
            self.speedy = random.randrange(-3, 3)
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speedy = -self.speedy

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laserImg
        self.image.set_colorkey(BLACK)
        self.rect = pygame.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 12

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > WIDTH:
            self.kill()

background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
playerImg = pygame.image.load("ghost.png").convert()
birdImg = pygame.image.load("bird.png").convert()
laserImg = pygame.image.load("laser.png").convert()

allSprites = pygame.sprite.Group()
birds = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
allSprites.add(player)

for i in range(8):
    m = badBirds()
    allSprites.add(m)
    birds.add(m)

running = True
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

    allSprites.update()

    hits = pygame.sprite.spritecollide(birds, bullets, True, True)
    for hit in hits:
        m = badBirds()
        allSprites.add(m)
        birds.add(m)

    hits = pygame.sprite.spritecollide(player, birds, False)
    if hits:
        running = False

    screen.blit(background, background_rect)
    allSprites.draw(screen)

    pygame.display.flip()

pygame.quit()