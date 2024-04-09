import bot
#import
background_image = "47343047c5_105832_ciel-bleu-01.jpg"


import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640, 455))

pygame.display.set_caption("Awalé 2.0")
background = pygame.image.load(background_image).convert()


nba, nbb = 24, 24
plateau = [4,4,4,4,4,4,4,4,4,4,4,4]
run = nba!=0 and nbb!=0

def affichage():
    for i in range(6):
        pygame.draw.circle(background, (250, 250, 0), (70+i*100, 130), 35)
        pygame.draw.circle(background, (250, 250, 0), (70 + i * 100, 330), 35)

def repartition(num):
    contenu = plateau[num]
    i=0
    while plateau[num]!=0:
        plateau[(num + i) % 12] += 1
        plateau[(num) % 12] -= 1
        i+=1

    print(plateau)
num = ''
while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:

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
                num=''
        affichage()
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        pygame.display.update()


pygame.quit()
quit()
#jeu

