import pygame, random

# Initialize pygame
pygame.init()

# Set display surface
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Base class for common attributes and methods
class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, width=None, height=None):
        super().__init__()
        self.image = pygame.image.load(image_path)
        if width and height:
            self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Bullet(GameObject):
    def __init__(self, image_path, x, y, velocity, bullet_group):
        super().__init__(image_path, x, y)
        self.velocity = velocity
        bullet_group.add(self)
    
    def update(self):
        self.rect.y += self.velocity
        if self.rect.bottom < 0 or self.rect.top > WINDOW_HEIGHT:
            self.kill()

class PlayerBullet(Bullet):
    def __init__(self, x, y, bullet_group):
        super().__init__("green_laser.png", x, y, -10, bullet_group)

class AlienBullet(Bullet):
    def __init__(self, x, y, bullet_group):
        super().__init__("red_laser.png", x, y, 10, bullet_group)

class Player(GameObject):
    def __init__(self, bullet_group):
        super().__init__("C:/Users/pc/Desktop/Rigel Infotech/C14/space invader/nanobot.png", WINDOW_WIDTH//2, WINDOW_HEIGHT - 100, 100, 100)
        self.lives = 5
        self.velocity = 8
        self.bullet_group = bullet_group

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity

    def fire(self):
        if len(self.bullet_group) < 2:
            PlayerBullet(self.rect.centerx, self.rect.top, self.bullet_group)

    def reset(self):
        self.rect.centerx = WINDOW_WIDTH//2

class Alien(GameObject):
    def __init__(self, x, y, velocity, bullet_group):
        super().__init__("bacteria.png", x, y, 50, 50)
        self.starting_x = x
        self.starting_y = y
        self.direction = 1
        self.velocity = velocity
        self.bullet_group = bullet_group

    def update(self):
        self.rect.x += self.direction * self.velocity
        if random.randint(0, 1000) > 999 and len(self.bullet_group) < 3:
            self.fire()

    def fire(self):
        AlienBullet(self.rect.centerx, self.rect.bottom, self.bullet_group)
    
    def reset(self):
        self.rect.topleft = (self.starting_x, self.starting_y)
        self.direction = 1

# Game Setup
my_player_bullet_group = pygame.sprite.Group()
my_alien_bullet_group = pygame.sprite.Group()
my_player_group = pygame.sprite.Group()
my_player = Player(my_player_bullet_group)
my_player_group.add(my_player)
my_alien_group = pygame.sprite.Group()

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.fire()

    display_surface.fill((0, 0, 0))
    my_player_group.update()
    my_player_group.draw(display_surface)
    my_alien_group.update()
    my_alien_group.draw(display_surface)
    my_player_bullet_group.update()
    my_player_bullet_group.draw(display_surface)
    my_alien_bullet_group.update()
    my_alien_bullet_group.draw(display_surface)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
