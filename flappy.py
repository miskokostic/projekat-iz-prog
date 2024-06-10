import pygame
from pygame.locals import *
import random

pygame.init()
clock = pygame.time.Clock()
fps = 60
width = 1000
height = 650
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Flappy Bird')
#font
font = pygame.font.Font('freesansbold.ttf', 32)
#boja slova
boja = (255,255,255)
#pozadina
pozadina = pygame.image.load("pozadina 1.png")
pod = pygame.image.load("pod.PNG")
#restart
restartdugme = pygame.image.load("restart.png")
#kretanje 
pod_kret = 0
kret = 4
#pocetak igrice i let
let = False
#kraj igrice
kraj = False
#poeni
score = 0

pass_pipe=False
def ispocetka():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = height//2
    score = 0
    return score
razdaljina = 200 #razdaljina izmedju zida
t = 1500 #na kolko vreme se stvori zid
poslednji = pygame.time.get_ticks()-t#poslednji zid
class ptica(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('ptica.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
    def update(self):
        #gravitacija
        if let == True:
            self.vel+=0.5
            if(self.vel > 8):
                self.vel = 8 
            if self.rect.bottom <= 550 or self.vel < 0:
                self.rect.y+=int(self.vel)
        # skok
        if pygame.mouse.get_pressed()[0] == 1 and kraj ==False:
            self.vel = -10
        if(kraj == True):
            self.image = pygame.image.load('umro.png')
        else:
            self.image = pygame.image.load('ptica.png')
class zid(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("zid.png")  
        self.rect = self.image.get_rect()
        #1 = gore -1 = dole
        
        if position == 1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y - int(razdaljina/2)]
        if position == -1:
            self.rect.topleft = [x,y+int(razdaljina/2)]
    def update(self):
        self.rect.x -= kret
        if self.rect.right < 0:
            self.kill()
class dugme():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    def draw(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))   
        # mis pozicija
        pos = pygame.mouse.get_pos()
        #mis na dugmetu
        action = False
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        return action
      

button = dugme(width//2-100,height//2-150,restartdugme)

bird_group = pygame.sprite.Group()
flappy = ptica(100,int(height/2))
bird_group.add(flappy)

pipe_group = pygame.sprite.Group()
#ispis za poene
def ispis(text,font,text_col,x,y):
    screen.blit(font.render(text,True,text_col), (x,y))




run = True

while run:
    clock.tick(fps)

    #postavljanje pozadine
    screen.blit(pozadina,(0,0))
    
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    
    #postavljanje poda i kretanje
    screen.blit(pod,(pod_kret,550))
    #poeni
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score+=1
                pass_pipe = False
    #ispis poena
    ispis(str(score),font,boja,int(width/2),30)
    #trazi dodir
    
    if pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or flappy.rect.top < 0:
        kraj = True
        

    #da li je udarilka zemlju
    if(flappy.rect.bottom > 550):
        kraj = True
        
        let = False
   
    
    if kraj == False and let == True:
        #novi zid
        sad = pygame.time.get_ticks()
        if sad - poslednji > t:
            visinaa = random.randint(-100,100)
            gornja = zid(width,int(height/2)+ visinaa,1)
            donja = zid(width,int(height/2)+ visinaa,-1)
            pipe_group.add(donja)
            pipe_group.add(gornja)  
            poslednji = sad
        pod_kret -= kret
        if abs(pod_kret) > 40:
            pod_kret = 0
        
        pipe_group.update()

    if kraj == True:
        if button.draw() == True:
            kraj = False
            score = ispocetka()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN and let == False and kraj == False:
            let = True

    pygame.display.update()
pygame.quit()