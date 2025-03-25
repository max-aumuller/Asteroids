import pygame
import random
from pygame import Vector2
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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

# Create player class
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        pygame.init()
        pygame.display.set_mode((1280, 900))
        self.image = pygame.image.load("ship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.orig_image = self.image  # Store original image for rotation
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)  # Use a Vector2 for precise positioning
        self.direction = Vector2(0, -1)  # Facing upward initially
        self.speed = 0  # Movement speed
        self.angle = 0  # Rotation angle

    def update(self):
        # Move the player in the direction it is facing
        self.pos += self.direction * self.speed
        self.rect.center = self.pos  # Keep rect updated

        # Apply friction (gradual speed reduction)
        self.speed *= 0.98  # Simulates inertia (slowly decreases speed)

        # Screen wrapping
        if self.rect.top > 900:
            self.pos.y = 0
        elif self.rect.bottom < 0:
            self.pos.y = 900
        if self.rect.left > 1280:
            self.pos.x = 0
        elif self.rect.right < 0:
            self.pos.x = 1280

    def rotate(self, angle_change):
        """Rotate the image of the sprite and update its direction."""
        self.angle += angle_change
        self.image = pygame.transform.rotozoom(self.orig_image, -self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)  # Keep center position
        self.direction = Vector2(0, -1).rotate(self.angle)  # Update movement direction

# Create player group
all_sprites = pygame.sprite.Group()
player1 = Player((320, 240))
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
    
    # Handle key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        done = True
    if keys[pygame.K_UP]:  # Accelerate forward
        player1.speed += 0.2  # Gradually increase speed

    if keys[pygame.K_LEFT]:  # Rotate counterclockwise
        player1.rotate(-5)
    if keys[pygame.K_RIGHT]:  # Rotate clockwise
        player1.rotate(5)

    # Spawn asteroids
    if len(asteroids) < 4:
        asteroid = Asteroid(20, 20, random.randint(0, 1280), random.randint(0, 900))
        asteroids.add(asteroid)
        all_sprites.add(asteroid)
    
    # Collision detection
    if pygame.sprite.spritecollide(player1, asteroids, True):
        pass  # Placeholder for handling collision
    
    # --- Game logic should go here
    all_sprites.update()
    
    # --- Screen-clearing code goes here
    screen.fill(WHITE)
 
    # --- Drawing code should go here 
    all_sprites.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
