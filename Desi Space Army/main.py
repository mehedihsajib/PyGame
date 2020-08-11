import pygame
from pygame import mixer
import random
import math

# Initialize the pygame module.
pygame.init()

# Create a screen
screen = pygame.display.set_mode((800, 600))
# Create background with custom image
backgroundImg = pygame.image.load('space-bg.png')

# Background music
#mixer.music.load('background.wav')
#mixer.music.play(-1)

# Set the game window/caption and icon
pygame.display.set_caption("Deshi Space Army")
icon = pygame.image.load('favicon.png')
pygame.display.set_icon(icon)

# Display the player and enemy to the game window
playerImg = pygame.image.load('player.png')
bulletImg = pygame.image.load('bullet.png')

# Positioning the player and enemies to game window by X an Y axis.
playerX = 370
playerY = 480
# Moving player by pressing arrow key
playerX_move = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_move = []
enemyY_move = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_move.append(2)
    enemyY_move.append(50)

# Bullet
bulletX = 0
bulletY = 480
bulletX_move = 0
bulletY_move = 9
bullet_state = "ready"

# Counting score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

texX = 10
textY = 10

# Game over font
over_font = pygame.font.Font("freesansbold.ttf", 60)


def show_score(x, y):
    """ Func about showing score to the screen """
    score = font.render("Score: " + str(score_value), True, (255, 255, 0))
    screen.blit(score, (x, y))


def game_over_text():
    """ Func about showing score to the screen """
    over_text = over_font.render("GAME OVER", True, (255, 255, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    """ This function about display the player and positioning the player to window """
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    """ This function about display the enemy and positioning the enemy to window """
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    """ This function all about bullet """
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    """ This func about distance between bullet and enemy """
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Holding the screen until Quit(X) button is pressed
running = True
while running:

    # Give the background color of game window
    screen.fill((0, 0, 0))
    # Draw background image to the screen
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed then check weather is right or left.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_move = -4
            if event.key == pygame.K_RIGHT:
                playerX_move = 4
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

                    # bullet sound
                    bullet_sound = mixer.Sound('funny-bullet.wav')
                    mixer.Sound.play(bullet_sound)

        # If keystroke is release/unpressed.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_move = 0

    # Create boundary for player so that it can't go out from window.
    playerX += playerX_move

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Moving enemies
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 460:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            show_score(330, 320)
            game_over_sound = mixer.Sound('game-over.wav')
            mixer.Sound.play(game_over_sound)
            break

        enemyX[i] += enemyX_move[i]
        if enemyX[i] <= 0:
            enemyX_move[i] = 2
            enemyY[i] += enemyY_move[i]
        elif enemyX[i] >= 736:
            enemyX_move[i] = -2
            enemyY[i] += enemyY_move[i]

        # If collusion happend reset the bullet
        collusion = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collusion:
            bulletY = 480
            bullet_state = 'ready'
            # Increment the score when enemy shoot
            score_value += 1

            # explosion sound
            explosion_sound = mixer.Sound('funny-explosion.wav')
            mixer.Sound.play(explosion_sound)

            # reset the enemy after shot down
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        # Calling the enemy().
        enemy(enemyX[i], enemyY[i], i)

    # Moving bullets
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_move

    # Calling the player()
    player(playerX, playerY)

    # Calling the show_score() function
    show_score(texX, textY)

    # Updating the game
    pygame.display.update()
