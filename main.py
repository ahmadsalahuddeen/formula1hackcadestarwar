import pygame
import math
import random
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))  

#background
background = pygame.image.load('background.png')

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)


# Title and Icon
pygame.display.set_caption("space invaders")
icon = pygame.image.load('project.png')
pygame.display.set_icon(icon)

# player

playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png')) 
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(5) 
    enemyY_change.append(40)


# bullet
# Ready-you cant see bullet on the screen
# fire -the bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 120
bullet_state = "ready"

#score

score_value = 0
font = pygame.font.Font('Goliend.ttf',62)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render('score : ' +str(score_value),True,(255,255,255))
    screen.blit(score, (x, y))

def player(x,y):
    screen.blit(playerImg, (x, y))


def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) +( math.pow(enemyY-bulletY,2)))
    if distance < 27 :
        return True
    else:
        return False


# game loop
running = True
while running:
    #RGB -red, green, blue
    screen.fill((0, 0, 0))
    # background Img
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
     
        # if keystroke is pressed check wether its right or letf
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                playerX_change = -7
            if event.key == pygame.K_RIGHT:
                playerX_change = 7
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()


                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    # 5=5 + -0.1 -> 5=5 - 0.1
    # 5=5 + 0.1

    # checking for boundries of spaceship so it doesn't go out of bounds
    playerX += playerX_change
    if playerX <=0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    # enemy Movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i],enemyY[i], i)
    
    #bullet movement 
    if bulletY <=0:
        bulletY = 480
        bullet_state ='ready' 

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    
    

    player(playerX,playerY)
    
    show_score(textX,textY)
    pygame.display.update()