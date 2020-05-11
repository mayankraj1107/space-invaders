import pygame
import random
import math
from pygame import mixer

# game inialize
pygame.init()

# variables
running = True
score = 0

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# score
font = pygame.font.Font('freesansbold.ttf', 40)
textX = 10
textY = 10


def show_score(x, y):
    scr = font.render("Score:" + str(score), True, (255, 255, 255))
    screen.blit(scr, (x, y))


# background image
background = pygame.image.load('Mayank.jpg')

# create screen
screen = pygame.display.set_mode((800, 600))

# background sound
mixer.music.load("background.mp3")
mixer.music.play((-1))

# background
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('transport.png')
pygame.display.set_icon(icon)
bground = (0, 0, 0)

# spaceship
shipImg = pygame.image.load('spaceship.png')
shipX = 370
shipY = 480


def ship(x, y):
    screen.blit(shipImg, (x, y))


# aliens
alienImg = []
alienX = []
alienY = []
alienX_move = []
alienY_move = []
no_of_aliens = 8

for i in range(no_of_aliens):
    alienImg.append(pygame.image.load('alien.png'))
    alienX.append(random.randint(0, 736))
    alienY.append(random.randint(50, 150))
    alienX_move.append(4)
    alienY_move.append(30)


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


# raedy - blt not moving
# fire - blt moving

# bullet
bltImg = pygame.image.load('bullet.png')
bltX = 0
bltY = 480
bltX_move = 0
bltY_move = 10
blt_state = "ready"


def bullet(x, y):
    global blt_state
    blt_state = "fire"
    screen.blit(bltImg, (x + 16, y + 10))


# keyboard control
def key_press():
    ship_move = 0
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            ship_move = -5
        if event.key == pygame.K_RIGHT:
            ship_move = 5
        if event.key == pygame.K_SPACE:
            global bltX
            if blt_state is "ready":
                blt_sound = mixer.Sound('laser.wav')
                blt_sound.play()
                bltX = shipX
                bullet(bltX, bltY)
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            ship_move = 0
    return (ship_move)


# collision
def collision(alienX, alienY, bltX, bltY):
    distance = math.sqrt((math.pow(alienX - bltX, 2)) + (math.pow(alienY - bltY, 2)))
    if distance < 27:
        return True
    else:
        return False


# main loop
while running:
    screen.fill(bground)
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # key control
        move = key_press()
    shipX += move

    # bounndry check
    if shipX <= 0:
        shipX = 0
    elif shipX >= 736:
        shipX = 736

    # alien movement
    for i in range(no_of_aliens):

        # game over
        if alienY[i] > 440:
            for j in range(no_of_aliens):
                alienY[j] = 2000
            game_over()
            break

        alienX[i] += alienX_move[i]
        if alienX[i] <= 0:
            alienX_move[i] = 4
            alienY[i] += alienY_move[i]
        elif alienX[i] >= 736:
            alienX_move[i] = -4
            alienY[i] += alienY_move[i]

        # collision
        attack = collision(alienX[i], alienY[i], bltX, bltY)
        if attack:
            attack_sound = mixer.Sound('explosion.wav')
            attack_sound.play()
            bltY = 480
            blt_state = "ready"
            score += 1
            alienX[i] = random.randint(0, 736)
            alienY[i] = random.randint(50, 150)

        # alien position
        alien(alienX[i], alienY[i], i)

    # bullet state
    if bltY <= 0:
        bltY = 480
        blt_state = "ready"

    if blt_state is "fire":
        bullet(bltX, bltY)
        bltY -= bltY_move

    # ship position
    ship(shipX, shipY)
    show_score(textX, textY)

    pygame.display.update()
