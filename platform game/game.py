import pygame
pygame.init()
from level import lv1

width, height, fps = 1000, 640, 60
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('platform game')
timer = pygame.time.Clock()
bg = pygame.image.load('Asset/BG.png').convert_alpha()
bg = pygame.transform.scale(bg,(width,height))
score = 0
win = 6

font = pygame.font.SysFont('Arial', 60)
font2 = pygame.font.SysFont('arial',30)
font3 = pygame.font.SysFont('arial',60)
def showgameoverText(x,y):
   gameovertext = font.render('GAME OVER', True, (255,0,0))
   screen.blit(gameovertext,(x,y))

def showgamewin(x,y):
    gamewintext = font3.render('You win', True, (8, 143, 143))
    screen.blit(gamewintext, (x,y))

def showscoretext(x,y,):
    scoretext = font2.render((f'score: {score}'), True, (255,0,0))
    screen.blit(scoretext, (x,y))

def healthBar(surf,x,y,pct):
    widthBar =100
    heightBar = 20
    fill= pct*widthBar
    outRect = pygame.Rect(x,y,widthBar,heightBar)
    fillRect = pygame.Rect(x,y,fill,heightBar)
    pygame.draw.rect(surf, (0,255,0), fillRect)
    pygame.draw.rect(surf, (255,255,255), outRect,2)




class Stage():
    def __init__(self,data):
        self.tilelist= []
        tile1 = pygame.image.load('Asset/tile1.png').convert_alpha()
        tile2 = pygame.image.load('Asset/tile2.png').convert_alpha()
        tile3 = pygame.image.load('Asset/tile3.png').convert_alpha()
        tile4 = pygame.image.load('Asset/tile4.png').convert_alpha()
        rowCount = 0
        for row in data:
            colCount =0
            for tile in row:
                if tile == 1:
                    img =pygame.transform.scale(tile1,(tilesize,tilesize))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tilesize
                    imgRect.y = rowCount * tilesize
                    tile = (img,imgRect)
                    self.tilelist.append(tile)
                if tile == 2:
                    img =pygame.transform.scale(tile2,(tilesize,tilesize))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tilesize
                    imgRect.y = rowCount * tilesize
                    tile = (img,imgRect)
                    self.tilelist.append(tile)
                if tile == 3:
                    img =pygame.transform.scale(tile3,(tilesize,tilesize))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tilesize
                    imgRect.y = rowCount * tilesize
                    tile = (img,imgRect)
                    self.tilelist.append(tile)
                if tile == 4:
                    img =pygame.transform.scale(tile4,(tilesize,tilesize))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tilesize
                    imgRect.y = rowCount * tilesize
                    tile = (img,imgRect)
                    self.tilelist.append(tile)
                if tile == 5:
                    kunai = Kunai(colCount*tilesize, rowCount*tilesize)
                    KunaiGroup.add(kunai)
                if tile == 6:
                   musuh = Enemy (colCount*tilesize,rowCount*tilesize)
                   enemyGroup.add(musuh)

                colCount += 1
            rowCount += 1

    def draw(self):
        for tile in self.tilelist:
            screen.blit(tile[0],tile[1])

class Kunai(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()

        obs = pygame.image.load('Asset/kunai.png').convert_alpha()
        obs = pygame.transform.scale(obs,(tilesize,tilesize))
        self.image = obs
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        screen.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.idles = []
        self.walksRight = []
        self.attacksRight = []
        self.walksLeft = []
        self.attacksLeft = []
        for a in range(1,10):
            idle = pygame.image.load(f'Asset/idle {a}.png')
            idle = pygame.transform.scale(idle,(30,30))
            self.idles.append(idle)
        for a in range(1, 10):
            walkRight = pygame.image.load(f'Asset/run {a}.png').convert_alpha()
            walkRight = pygame.transform.scale(walkRight, (30, 30))
            walkLeft = pygame.transform.flip(walkRight, True, False)
            self.walksRight.append(walkRight)
            self.walksLeft.append(walkLeft)
        for a in range(1, 10):
            attackRight = pygame.image.load(f'Asset/attack{a}.png').convert_alpha()
            attackRight = pygame.transform.scale(attackRight, (50, 30))
            attackLeft = pygame.transform.flip(attackRight, True, False)
            self.attacksRight.append(attackRight)
            self.attacksLeft.append(attackLeft)
        self.counter = 0
        self.image = self.idles[self.counter]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 'right'
        self.direction = "left"
        self.isWalking = False
        self.moveSpeed = 0
        self.gravity = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.isJump = False
        self.health = 100
        self.isAttack = False
    def draw(self):
        global score;
        dy = 0
        self.moveSpeed = 0
        self.isWalking = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.isWalking = True
            self.direction = 'right'
            self.moveSpeed = 3

        if keys[pygame.K_a]:
            self.isWalking = True
            self.direction = "left"
            self.moveSpeed = -3

        if keys[pygame.K_w] and self.isJump==False:
            self.gravity = -15
            self.isJump=True

        if keys[pygame.K_SPACE] and self.isAttack==False:
           self.isAttack = True


        #gravity stuff
        self.gravity+=1
        if self.gravity>10:
            self.gravity=10
        dy=self.gravity

        # collision player with Obstacle
        if pygame.sprite.spritecollide(self, KunaiGroup, False) or self.health == 0:
            showgameoverText(400, 250)
            pygame.display.update()
            pygame.time.delay(3000)
            pygame.quit()
        if pygame.sprite.spritecollide(self, enemyGroup, False):
            self.health -= 10
            if self.isAttack==True:
                pygame.sprite.spritecollide(self,enemyGroup,True)
                score += 1
                if self.direction=='right':
                    self.moveSpeed=-25
                    self.rect.x += self.moveSpeed
        if score == win:
            showgamewin(400,250)
            pygame.display.update()
            pygame.time.delay(3000)
            pygame.quit()
        #colison
        for tile in stage.tilelist:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.gravity < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.gravity = 0
                if self.gravity >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.gravity = 0
                    self.isJump = False
            if tile[1].colliderect(self.rect.x+self.moveSpeed,self.rect.y,self.width,self.height):
                self.moveSpeed = 0
        if self.isWalking==False and self.isAttack==False:
           self.counter+=0.25
           if self.counter>=len(self.idles):
               self.counter=0
           self.image=self.idles[int(self.counter)]

        if self.isWalking == True and self.isAttack == False and self.direction == 'right':
            self.counter += 0.25
            if self.counter >= len(self.walksRight):
                self.counter = 0
            self.image = self.walksRight[int(self.counter)]

        if self.isWalking == True and self.isAttack == False and self.direction == 'left':
            self.counter += 0.25
            if self.counter >= len(self.walksLeft):
                self.counter = 0
            self.image = self.walksLeft[int(self.counter)]

        if self.isWalking == False and self.isAttack == True and self.direction == 'right':
            self.counter += 0.25
            if self.counter >= len(self.attacksRight):
                self.counter = 0
            self.image = self.attacksRight[int(self.counter)]
            self.isAttack = False

        if self.isWalking == False and self.isAttack == True and self.direction == 'left':
            self.counter += 0.25
            if self.counter >= len(self.attacksLeft):
                self.counter = 0
            self.image = self.attacksLeft[int(self.counter)]
            self.isAttack = False

        #Update X position
        self.rect.x += self.moveSpeed
        #update Y position
        self.rect.y += self.gravity

        screen.blit(self.image, (self.rect.x, self.rect.y))
        #pygame.draw.rect(screen,(255,0,0),self.rect,2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        for a in range(1, 12):
            image = pygame.image.load(f'Asset/monster ({a}).png').convert_alpha()
            image = pygame.transform.scale(image, (30, 30))
            self.images.append(image)
        self.counter = 0
        self.image = self.images[self.counter]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.counter += 1
        if self.counter >= len(self.images):
            self.counter = 0
        self.image = self.images[self.counter]
        screen.blit(self.image, self.rect)

player = Player(500,200)
enemyGroup = pygame.sprite.Group()
tilesize = 32
KunaiGroup = pygame.sprite.Group()
stage= Stage(lv1)
play = True
while play:
    screen.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()



    stage.draw()
    showscoretext(5,10)
    healthBar(screen,888,10,player.health/100)
    enemyGroup.draw(screen)
    enemyGroup.update()
    KunaiGroup.draw(screen)
    KunaiGroup.update()
    player.draw()
    timer.tick(fps)
    pygame.display.update()