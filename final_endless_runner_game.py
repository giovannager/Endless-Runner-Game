# Name: Giovanna Gerda
# Date Coding began: 01/07/2020

# import libraries
import pygame
import random

from os import path

images_dir = path.join(path.dirname(__file__), 'images')
sounds_dir = path.join(path.dirname(__file__), 'sounds')

WIDTH = 800
HEIGHT = 400
FPS = 60

# ========================================== COLOUR DEFINITIONS =======================================================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# ========================================== END OF - COLOUR DEFINITIONS ==============================================

# ======================================== INITIALIZE PYGAME AND CREATE WINDOW ========================================
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moonbyul's Hip Adventure")
clock = pygame.time.Clock()

# Define variables
game_over = True
high_score = 0

# Obtain font type (name)
font_name = pygame.font.match_font("ariel")

# Define a function to draw text
def draw_text(surf, text, size, colour, x, y):
    font = pygame.font.Font(font_name, size)
    # create a text object
    text_surface = font.render(text, True, colour)
    # create a rectangular area to render the text to
    text_rect = text_surface.get_rect()
    # Set positioning for the text
    text_rect.topleft = (int(x), int(y))
    # blit the text to the screen
    surf.blit(text_surface, text_rect)


# Define the game over screen text and configurations
def game_over_screen():
    screen.blit(intro_screen, intro_screen_rect)
    draw_text(screen, "Moonbyul's Hip Adventure", 60, BLACK, 100, int(HEIGHT * 1 / 16))
    draw_text(screen, "HIGH SCORE: " + str(high_score) + " m", 40, BLACK, 250, int(HEIGHT * 3/ 8))
    draw_text(screen, "Press any key to view instructions", 20, BLACK, 250, int(HEIGHT * 9 / 16))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                game_instructions()
                waiting = False


# Define the game instructions screen text and configurations
def game_instructions():
    screen.fill(WHITE)
    draw_text(screen, "Instructions", 50, BLACK, 20, int(HEIGHT / 16))
    draw_text(screen, "  Objective", 30, BLACK, 20, int(HEIGHT * 4 / 16))
    draw_text(screen, "- Travel the farthest distance!", 25, BLACK, 20, int(HEIGHT * 6 / 16))
    draw_text(screen, "- Jump over or shoot x-boxes that", 25, BLACK, 20, int(HEIGHT * 7 / 16))
    draw_text(screen, "  block your path", 25, BLACK, 20, int(HEIGHT * 8 / 16))
    draw_text(screen, "- Collect radish power-ups to", 25, BLACK, 20, int(HEIGHT * 9 / 16))
    draw_text(screen, "  obtain ammo", 25, BLACK, 20, int(HEIGHT * 10 / 16))
    draw_text(screen, "  Be sure not to hit the x-boxes!", 25, BLACK, 20, int(HEIGHT * 12 / 16))
    draw_text(screen, "  The game will end if you do!", 25, BLACK, 20, int(HEIGHT * 13 / 16))
    draw_text(screen, "  Gameplay", 30, BLACK, 500, int(HEIGHT * 4 / 16))
    draw_text(screen, "- Press the up-arrow key to jump", 25, BLACK, 500, int(HEIGHT * 6 / 16))
    draw_text(screen, "- Press the space bar to shoot", 25, BLACK, 500, int(HEIGHT * 7 / 16))
    draw_text(screen, "Press space to start", 16, BLACK, 510, int(HEIGHT * 7 / 8))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                waiting = False


# Create a background class
class Background(pygame.sprite.Sprite):
    # the sprite for the background
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image = background
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = 0
        self.speedx = -1

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right == WIDTH:
            background_two = Background_two()
            background_sprite.add(background_two)
        if self.rect.right == 0:
            self.kill()


# Create a second background class (to scroll the images)
class Background_two(pygame.sprite.Sprite):
    # the sprite for the background
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image = background
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = WIDTH
        self.speedx = -1
        self.flag = False

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right == WIDTH:
            background = Background_two()
            background_sprite.add(background)
        if self.rect.right == 0:
            self.kill()


# Create a player class
class Player(pygame.sprite.Sprite):
    # the sprite for the player
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        # Sets a coordinates of size for the player class
        self.image = pygame.Surface((50, 50))
        # Set the image to animation of the player running
        self.position = position
        self.image = byul_animation[self.position][0]
        # Creates a rectangle for the size set
        self.rect = self.image.get_rect()
        # Set the initial position and speed of y
        self.rect.left = 40
        self.rect.bottom = HEIGHT - 30
        self.speedy = 0
        # Timing and score variables
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.ammo = 0
        self.last_shot = pygame.time.get_ticks()
        self.shot_time = 200
        self.score_update = pygame.time.get_ticks()
        self.score_time = 50
        self.score = 0

    def update(self):
        # have the player jump up at a speed of 7 when space is pressed
        if pygame.key.get_pressed()[pygame.K_UP] and self.rect.bottom == HEIGHT - 30:
            self.speedy = -10
        # Have the player fall back down after a certain height
        if self.rect.top <= HEIGHT - 225:
            self.speedy = 10
        # Have the player stop once they reach the starting position
        if self.rect.bottom > HEIGHT - 29:
            self.rect.bottom = HEIGHT - 30
            self.speedy = 0
        self.rect.y += self.speedy

        # Running animation
        if self.rect.bottom == HEIGHT - 30:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame >= len(byul_animation[self.position]):
                    self.frame = 0
                self.image = byul_animation[self.position][self.frame]

        # Jumping pose
        elif HEIGHT - 30 < self.rect.bottom <= HEIGHT - 37:
            self.image = byul_animation[self.position][2]
        else:
            self.image = byul_animation[self.position][4]

        # shoot and increase ammo
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shot_time:
                self.last_shot = now
                if self.ammo > 0:
                    self.ammo -= 1
                    self.shoot()

        # increase score
        now = pygame.time.get_ticks()
        if now - self.score_update > self.score_time:
            self.score_update = now
            self.score += 1

    # Define a function to shoot
    def shoot(self):
        sing_sound.play()
        sing = Sing(self.rect.top + 10)
        sing_sprites.add(sing)
        all_sprites.add(sing)


# Create a obstacle class
class Obstacle(pygame.sprite.Sprite):
    # the sprite for the obstacle
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Sets coordinates of random size for the obstacle class
        self.size = random.choice([(30, 80), (70, 70), (150, 40)])
        self.image = pygame.Surface(self.size)
        # Randomizes powerup drops
        if random.random() > 0.8:
            powerup = Powerup()
            powerup_sprites.add(powerup)
            all_sprites.add(powerup)
        # Set an image for the randomized conditions
        if self.size == (70, 70):
            self.image = box
        elif self.size == (30, 80):
            self.image = box_two
        else:
            self.image = box_three
        # Creates a rectangle for the size set
        self.rect = self.image.get_rect()
        # Set the initial position and speed of y
        self.left = random.randrange(10, 150)
        self.rect.left = WIDTH + self.left
        self.rect.bottom = HEIGHT - 30
        self.speedx = -15
        # Timing of generation variables
        self.last_generation = pygame.time.get_ticks()
        self.generation_time = 1000
        self.last_kill = pygame.time.get_ticks()
        self.end_time = 1500

    def update(self):
        self.rect.x += self.speedx
        # generate new objects after a certain amount of time
        now = pygame.time.get_ticks()
        if now - self.last_generation > self.generation_time:
            self.last_generation = now
            obstacleTwo = Obstacle()
            all_sprites.add(obstacleTwo)
            object_sprites.add(obstacleTwo)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_kill > self.end_time:
            self.last_kill = current_time
            self.kill()


# Create a powerup class
class Powerup(pygame.sprite.Sprite):
    # the sprite for the powerup
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Set coordinates of size for the powerup class
        self.size = (25, 25)
        self.image = pygame.Surface(self.size)
        # Set the colour of the image to blue
        self.image = radish
        # Creates a rectangle for the size set
        self.rect = self.image.get_rect()
        # Create a radius
        self.radius = 7
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        # Set the initial position and speed of x and the position of y
        xLeft = random.randrange(10, 500)
        self.rect.left = WIDTH + xLeft
        self.rect.bottom = HEIGHT - 150
        self.speedx = -15
        # Timing variables
        self.last_kill = pygame.time.get_ticks()
        self.end_time = 2200

    def update(self):
        self.rect.x += self.speedx
        # Kill the powerup after a certain amount of time
        current_time = pygame.time.get_ticks()
        if current_time - self.last_kill > self.end_time:
            self.last_kill = current_time
            self.kill()


# Create the sing (bullet) class
class Sing(pygame.sprite.Sprite):
    # the sprite for the sing bullet
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        # Set coordinates of size for the sing class
        self.image = pygame.Surface((10, 10))
        self.image = ammo_image
        self.rect = self.image.get_rect()
        self.radius = 5
        # initial position and speed variables
        self.rect.left = 80
        self.rect.top = y
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > WIDTH:
            self.kill()


# Load all images
background = pygame.image.load(path.join(images_dir, "MamamooBg.png")).convert()

radish = pygame.image.load(path.join(images_dir, "Radish.png")).convert()
radish.set_colorkey(WHITE)

ammo_image = pygame.image.load(path.join(images_dir, "SingAmmo.png")).convert()
ammo_image.set_colorkey(WHITE)

intro_screen = pygame.image.load(path.join(images_dir, "moonbyul.png")).convert()
intro_screen_rect = intro_screen.get_rect()

box = pygame.image.load(path.join(images_dir, "box.png")).convert()
box_two = pygame.image.load(path.join(images_dir, "box2.png")).convert()
box_three = pygame.image.load(path.join(images_dir, "box3.png")).convert()

byul_animation = {}
byul_animation["run"] = []
# Load animation images
for i in range(1, 6):
    filename = 'ByulRun{}.png'.format(i)
    img = pygame.image.load(path.join(images_dir, filename)).convert()
    img.set_colorkey(WHITE)
    byul_animation["run"].append(img)


# Load background music
pygame.mixer.music.load(path.join(sounds_dir, "hip mamamoo.wav"))

# Load sounds
hit_sound = pygame.mixer.Sound(path.join(sounds_dir, "hit.wav"))
sing_sound = pygame.mixer.Sound(path.join(sounds_dir, "sing.wav"))
powerup_sound = pygame.mixer.Sound(path.join(sounds_dir, "powerup.wav"))


# Play the background music in an endless loop
pygame.mixer.music.play(loops=-1)
# ======================================== END OF - INITIALIZE PYGAME AND CREATE ======================================

# ===================================================== GAME LOOP =====================================================
done = False
while not done:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            game_over = True
    if game_over == True:
        game_over_screen()
        game_over = False
        # Create the all sprites group
        all_sprites = pygame.sprite.Group()
        player_sprite = pygame.sprite.Group()
        object_sprites = pygame.sprite.Group()
        background_sprite = pygame.sprite.Group()
        powerup_sprites = pygame.sprite.Group()
        sing_sprites = pygame.sprite.Group()

        # Create an instance of the background class and add it to all_sprites and background_sprite
        background_img = Background()
        background_sprite.add(background_img)

        # Create an instance of the Player class and add it to all_sprites and player_sprite
        player = Player("run")
        player_sprite.add(player)
        all_sprites.add(player)

        # Create an instance of the Obstacle class and add it to all_sprites and obstacle_sprites
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        object_sprites.add(obstacle)

    # --------------------------------------------------- UPDATE --------------------------------------------------
    background_sprite.update()
    all_sprites.update()

    if player.score > high_score:
        high_score = player.score

    # Check for collision
    hits = pygame.sprite.groupcollide(player_sprite, object_sprites, False, False)
    for hit in hits:
        hit_sound.play()
        game_over = True

    hits = pygame.sprite.groupcollide(player_sprite, powerup_sprites, False, True, pygame.sprite.collide_circle)
    if hits:
        powerup_sound.play()
        player.ammo += 1

    hits = pygame.sprite.groupcollide(object_sprites, sing_sprites, True, True, pygame.sprite.collide_circle)
    if hits:
        hit_sound.play()
        obstacle = Obstacle()
        object_sprites.add(obstacle)
        all_sprites.add(obstacle)

    # --------------------------------------------------- DRAW ----------------------------------------------------
    screen.fill(BLACK)
    background_sprite.draw(screen)
    all_sprites.draw(screen)
    draw_text(screen, "DISTANCE: " + str(player.score) + " m", 30, BLACK, 20, 10)
    draw_text(screen, "AMMO: " + str(player.ammo), 30, BLACK, WIDTH - 150, 10)

    # ---------------------------------------------- REFRESH THE SCREEN -------------------------------------------
    pygame.display.flip()
pygame.quit()