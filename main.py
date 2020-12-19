import pygame
import random
import math

from pygame import mixer


# initialize pygame
pygame.init()

# Creating a screen
screen = pygame.display.set_mode((800,600))

# backgroumd
background = pygame.image.load(r'C:\Users\Bibek Chowdhury\OneDrive\Documents\projects\practice\python\game\SpaceInvader\bg1.jpg')
# bgm
mixer.music.load(r'C:\Users\Bibek Chowdhury\OneDrive\Documents\projects\practice\python\game\SpaceInvader\background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
logo = pygame.image.load(r'C:\Users\Bibek Chowdhury\OneDrive\Documents\projects\practice\python\game\SpaceInvader\icon.png')
pygame.display.set_icon(logo)

# Player img and position
playerImg = pygame.image.load(r'C:\Users\Bibek Chowdhury\OneDrive\Documents\projects\practice\python\game\SpaceInvader\spaceship.png')
playerX = 380 
playerY = 480 
playerX_change = 0
playerY_change = 0

# Score
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10
overFont = pygame.font.Font('freesansbold.ttf',70)
crashState = False

# Enemy img and position
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numOfEnemies = 10
# enemy random position
for i in range(numOfEnemies):
        enemyImg.append(pygame.image.load(r'C:\Users\Bibek Chowdhury\OneDrive\Documents\projects\practice\python\game\SpaceInvader\enemy.png'))
        enemyX.append(random.randint(0,736)) 
        enemyY.append(random.randint(0,150))
        enemyX_change.append(0.3)
        enemyY_change.append(40)


# Bullet img and position
bulletImg = pygame.image.load(r'C:\Users\Bibek Chowdhury\OneDrive\Documents\projects\practice\python\game\SpaceInvader\bullet.png')
bulletX = 0
bulletY = 0
bulletX_change = 0
bulletY_change = 0.8
#ready - not visible || fire- visible
bullet_state = "ready"



# Game Over
def gameOver():
    mixer.music.stop()
    gameOverSound = mixer.Sound(r'C:\Users\Bibek Chowdhury\OneDrive\Documents\projects\practice\python\game\SpaceInvader\gameover.wav')
    gameOverSound.play(0)
    endscore = overFont.render("GAME OVER",True,(255,255,255))
    screen.blit(endscore,(200,250))
    score = font.render("Score: "+ str(scoreValue),True,(255,255,255))
    screen.blit(score,(350,400))

# showscore
def show_score(x,y):
    score = font.render("Score: "+ str(scoreValue),True,(255,255,255))
    screen.blit(score,(x,y))

# player draw
def player(X,Y):
    screen.blit(playerImg,(X,Y))

# enemy draw
def enemy(X,Y,i):
    screen.blit(enemyImg[i],(X,Y))

# bullet fire
def fire_bullet(x,y):
    global bullet_state,scoreValue
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16, y + 10))

# Crash
def isCrashed(enemyX,enemyY,playerX,playerY):
    distance = math.sqrt((math.pow(enemyX-playerX,2)) + (math.pow(enemyY-playerY,2)))
    if distance < 50:
        return True
    else:
        return False

# Collision
def isCollided(enemyX,enemyY,bulletX,bulletY):
    global scoreValue, numOfEnemies
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False



# Game Loop -----------------Main Loop #
run = True
while run:

    # RGB
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background,(0,0))

    #Events fetch
    for event in pygame.event.get():
        # exit ~x~
        if event.type == pygame.QUIT:
            run = False
        # any ketstroke released event check
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0

    # any ketstroke pressed event check
    keys= pygame.key.get_pressed()

    
    if keys[pygame.K_LEFT]:
        playerX_change = -0.8
            
    if keys[pygame.K_UP]:
        playerY_change = -0.8
                
    if keys[pygame.K_RIGHT]:
        playerX_change = 0.8
            
    if keys[pygame.K_DOWN]:
        playerY_change = 0.8

    if keys[pygame.K_SPACE]:
        if bullet_state == "ready":
            bulletSound = mixer.Sound(r'C:\Users\Bibek Chowdhury\OneDrive\Documents\projects\practice\python\game\SpaceInvader\laser.wav')
            bulletSound.play()
            bulletX = playerX
            bulletY = playerY 
            fire_bullet(bulletX,bulletY)
                
        
            

  

    playerX += playerX_change
    playerY += playerY_change

    # setting boundary
    if playerX <=0:
        playerX = 0
    if playerY <=0:
        playerY = 0
    if playerX >=736:
        playerX = 736
    if playerY >=536:
        playerY = 536

    # enemy movement mechanism
    for i in range(numOfEnemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >=736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        
        # Crash
        crash = isCrashed(enemyX[i],enemyY[i],playerX,playerY)
        if crash:
            for j in range(numOfEnemies):
                enemyY[j] = 1000
            crashState = True
            break

        # collision
        collision = isCollided(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosionSound = mixer.Sound(r'C:\Users\Bibek Chowdhury\OneDrive\Documents\projects\practice\python\game\SpaceInvader\explosion.wav')
            explosionSound.play()
            bulletY=0
            bullet_state = "ready"
            scoreValue += 1
           
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(0,150)
            
        
        enemy(enemyX[i],enemyY[i],i) # enemy call
    
    # bullet movement mechanism
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    # bullet reset
    if bulletY <= 0:
        bullet_state = "ready"

  
        

    show_score(textX,textY)
    player(playerX,playerY) # player call
    if crashState is True:
        screen.fill((0, 0, 0))
        gameOver()

    pygame.display.update()

