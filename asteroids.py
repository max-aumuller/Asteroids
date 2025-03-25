import pygame
import random
import math
from pygame import Vector2
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create the asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = random.randint(-2, 2)
        self.y_speed = random.randint(-2, 2)

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.top > 900 or self.rect.bottom < 0:
            self.kill()
        elif self.rect.left > 1280 or self.rect.right < 0:
            self.kill()

# Create the asteroid group
asteroids = pygame.sprite.Group()

# create player class
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        pygame.init()
        pygame.display.set_mode((1280, 900))
        player_x = 20
        player_y = 20
        self.image = pygame.image.load("ship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = pos)
        self.rect.x = 350
        self.rect.y = 250
        self.direction = Vector2(0, -1)
        self.x_speed = 0
        self.y_speed = 0
        self.angle = 0
        self.orig_image = self.image
        self.pos = Vector2(player_x, player_y)
        self.offset = Vector2(50, 0)
        self.orig_rect = self.image.get_rect(center=(1280//2, 900//2))
        self.angle = 0
    
    def update(self):
        if self.rect.top > 960:
            self.rect.y += -10
        elif self.rect.bottom < 0:
            self.rect.y += 10
        
        if self.rect.left > 1280:
            self.rect.x += -10
        elif self.rect.right < 0:
            self.rect.x += 10
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.y_speed = -10
    
    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pygame.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos+offset_rotated)


# create player group
all_sprites = pygame.sprite.Group()
player = pygame.sprite.Group()
player1 = Player((320, 240))
player.add(player1)
all_sprites.add(player1)

pygame.init()

# Set the width and height of the screen [width, height]
size = (1280, 900)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Asteroids")
 
# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_LEFT:
                player1.angle+=1
                rotated_image = pygame.transform.rotozoom(player1.image, player1.angle, 1)  # rotozoom avoids size issues
                rotated_rect = rotated_image.get_rect(center= player1.orig_rect.center)

 
    # --- Game logic should go here
    if len(asteroids) < 4:
        asteroid = Asteroid(20, 20, random.randint(0, 700), random.randint(0, 500))
        asteroids.add(asteroid)
        all_sprites.add(asteroid)
        print("i am here")
    if pygame.sprite.spritecollide(player1, asteroids, True):
        asteroid.kill()
    
    if player1.y_speed < 0:
        player1.rect.y += player1.y_speed
        player1.y_speed += 0.3

    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(WHITE)
 
    # --- Drawing code should go here 
    all_sprites.update()
    all_sprites.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
    print(len(asteroids))

# Close the window and quit.
pygame.quit()
