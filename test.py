import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Invaders - No Groups")

FPS = 60
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    """A class to model a spaceship the user can control"""

    def __init__(self):
        """Initialize the player"""
        super().__init__()
        self.image = pygame.image.load("C:/Users/pc/Desktop/Rigel Infotech/C14/space invader/nanobot.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT

        self.lives = 5
        self.velocity = 8
        self.bullets = []

    def update(self):
        """Update the player"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

    def fire(self):
        """Fire a bullet"""
        if len(self.bullets) < 2:
            bullet = PlayerBullet(self.rect.centerx, self.rect.top)
            self.bullets.append(bullet)

    def reset(self):
        """Reset the player position"""
        self.rect.centerx = WINDOW_WIDTH // 2


class Alien(pygame.sprite.Sprite):
    """A class to model an enemy alien"""

    def __init__(self, x, y, velocity):
        """Initialize the alien"""
        super().__init__()
        self.image = pygame.image.load("bacteria.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.starting_x = x
        self.starting_y = y
        self.direction = 1
        self.velocity = velocity
        self.bullets = []

    def update(self):
        """Update the alien"""
        self.rect.x += self.direction * self.velocity

        if random.randint(0, 1000) > 999 and len(self.bullets) < 3:
            self.fire()

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.top > WINDOW_HEIGHT:
                self.bullets.remove(bullet)

    def fire(self):
        """Fire a bullet"""
        bullet = AlienBullet(self.rect.centerx, self.rect.bottom)
        self.bullets.append(bullet)

    def reset(self):
        """Reset the alien position"""
        self.rect.topleft = (self.starting_x, self.starting_y)
        self.direction = 1


class PlayerBullet(pygame.sprite.Sprite):
    """A class to model a bullet fired by the player"""

    def __init__(self, x, y):
        """Initialize the bullet"""
        super().__init__()
        self.image = pygame.image.load("green_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = 10

    def update(self):
        """Update the bullet"""
        self.rect.y -= self.velocity


class AlienBullet(pygame.sprite.Sprite):
    """A class to model a bullet fired by the alien"""

    def __init__(self, x, y):
        """Initialize the bullet"""
        super().__init__()
        self.image = pygame.image.load("red_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = 10

    def update(self):
        """Update the bullet"""
        self.rect.y += self.velocity


# Create player
player = Player()

# Create aliens
aliens = []  # Create an empty list

for _ in range(5):
    x = random.randint(50, WINDOW_WIDTH - 50)  # Random X position
    y = random.randint(50, 200)  # Random Y position
    velocity = random.randint(2, 4)  # Random speed
    
    alien = Alien(x, y, velocity)  # Create an Alien instance
    aliens.append(alien)  # Add it to the list

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()

    # Update all objects
    player.update()
    for alien in aliens:
        alien.update()

    # Draw everything
    display_surface.fill((0, 0, 0))
    display_surface.blit(player.image, player.rect)

    # Draw player bullets
    for bullet in player.bullets:
        display_surface.blit(bullet.image, bullet.rect)

    # Draw aliens and their bullets
    for alien in aliens:
        display_surface.blit(alien.image, alien.rect)
        for bullet in alien.bullets:
            display_surface.blit(bullet.image, bullet.rect)

    # Refresh display
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
