import bot
#import
background_image = "47343047c5_105832_ciel-bleu-01.jpg"


import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640, 455))

pygame.display.set_caption("Awalé 2.0")
background = pygame.image.load(background_image).convert()

last_posA = 0
last_posB = 0
nba, nbb = 24, 24
plateau_jeu = [4,4,4,4,4,4,4,4,4,4,4,4]
plateau_visu = plateau_jeu
run = nba!=0 and nbb!=0
tour = True
def affichage():
    for i in range(6):
        plateau_visu  = plateau_jeu[:6]+plateau_jeu[12:5:-1]
        pygame.draw.circle(background, (250, 250, 0), (70+i*100, 130), 35)
        pygame.draw.circle(background, (250, 250, 0), (70 + i * 100, 330), 35)
        print(plateau_visu)

def repartition(num):
    contenu = plateau_jeu[num]
    i=0
    while plateau_jeu[num]!=0:
        plateau_jeu[(num + i) % 12] += 1
        plateau_jeu[(num) % 12] -= 1
        i=(i-1)%12

num = ''
while run:

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos)

            if 34<pos[0]<105 :
                if 95<pos[1]<165:
                    repartition(0)
                elif 296<pos[1]<366:
                    repartition(11)
            if 135<pos[0]<206 :
                if 95<pos[1]<165:
                    repartition(1)
                elif 296<pos[1]<366:
                    repartition(10)
            if 235<pos[0]<306 :
                if 95<pos[1]<165:
                    repartition(2)
                elif 296<pos[1]<366:
                    repartition(9)
            if 335<pos[0]<406 :
                if 95<pos[1]<165:
                    repartition(3)
                elif 296<pos[1]<366:
                    repartition(8)
            if 435<pos[0]<506 :
                if 95<pos[1]<165:
                    repartition(4)
                elif 296<pos[1]<366:
                    repartition(7)
            if 535<pos[0]<606 :
                if 95<pos[1]<165:
                    repartition(5)
                elif 296<pos[1]<366:
                    repartition(6)

        '''if event.type == pygame.KEYDOWN and len(str(num))<2:

            if event.key == pygame.K_1:
                num=num+'1'
            elif event.key == pygame.K_2:
                num=num+'2'
            elif event.key == pygame.K_3:
                num+='3'
            elif event.key == pygame.K_4:
                num+='4'
            elif event.key == pygame.K_5:
                num+='5'
            elif event.key == pygame.K_6:
                num+='6'
            elif event.key == pygame.K_7:
                num+='7'
            elif event.key == pygame.K_8:
                num+='8'
            elif event.key == pygame.K_9:
                num+='9'
            elif event.key == pygame.K_0:
                num+='0'
                print(num)

            elif event.key == pygame.KSCAN_DELETE :
                num-=num[len(num)]
                print(num)
            elif event.key == pygame.K_RETURN:
                print(num)
                repartition(int(num))
                num='''''
        affichage()
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        pygame.display.update()
    tour = not tour

pygame.quit()
quit()
#jeu

