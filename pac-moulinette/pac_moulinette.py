import pygame
import classforthegame
import mazegen
import sys

pygame.init()
taille = (640, 480)
pygame.display.set_caption("pac_moulinette")
fenetre = pygame.display.set_mode(taille, pygame.RESIZABLE)
fond = pygame.image.load("maze.jpg").convert()
image_moulinette = pygame.image.load("knight_cat.png").convert_alpha()
image_stu = pygame.image.load("dragon.png").convert_alpha()
image_piscin = pygame.image.load("Eliot.png").convert_alpha()
maze = mazegen.MazeGenerator(sys.argv[1])
game = True
right = up = down = left = False
moulinette = classforthegame.Moulinette(maze)
stu = classforthegame.Stud()
piscin = classforthegame.Piscineux()
pos_moulinette = moulinette.pos
pos_stu = stu.pos
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                left = up = down = False
                right = True
            if event.key == pygame.K_LEFT:
                right = up = down = False
                left = True
            if event.key == pygame.K_DOWN:
                left = right = up = False
                down = True
            if event.key == pygame.K_UP:
                left = right = down = False
                up = True
    pos_moulinette = moulinette.mouve(right, left, down, up)
    pos_stu = stu.mouve()
    pos_piscin = piscin.mouve(pos_moulinette)
    fenetre.blit(fond, (0, 0))
    fenetre.blit(image_moulinette, pos_moulinette)
    fenetre.blit(image_stu, pos_stu)
    fenetre.blit(image_piscin, pos_piscin)
    pygame.display.flip()
