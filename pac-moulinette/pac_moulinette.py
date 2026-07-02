import pygame
import classforthegame
from mazegenerator import MazeGenerator
from maze_wrapper import MazeLoader, LvlConfig
import asset
from typing import Any

pygame.init()

level = LvlConfig(width=16, height=12, seed=39)
maze_loader = MazeLoader(level)
maze = maze_loader.load()

moul_size = 60
taille = (1280, 960)
pygame.display.set_caption(asset.DRAGON_PATH)
fenetre = pygame.display.set_mode(taille, pygame.RESIZABLE)
image_moulinette = pygame.transform.scale(pygame.image.load(asset.KNIGHT_PATH).convert_alpha(), (moul_size, moul_size))
image_stu = pygame.image.load(asset.DRAGON_PATH).convert_alpha()
image_piscin = pygame.image.load(asset.ELIOT_PATH).convert_alpha()
image_wall0 = pygame.image.load(asset.WALL_0).convert_alpha()
image_wall1 = pygame.image.load(asset.WALL_1).convert_alpha()
image_wall10 = pygame.image.load(asset.WALL_10).convert_alpha()
image_wall11 = pygame.image.load(asset.WALL_11).convert_alpha()
image_wall100 = pygame.image.load(asset.WALL_100).convert_alpha()
image_wall101 = pygame.image.load(asset.WALL_101).convert_alpha()
image_wall110 = pygame.image.load(asset.WALL_110).convert_alpha()
image_wall111 = pygame.image.load(asset.WALL_111).convert_alpha()
image_wall1000 = pygame.image.load(asset.WALL_1000).convert_alpha()
image_wall1100 = pygame.image.load(asset.WALL_1100).convert_alpha()
image_wall1010 = pygame.image.load(asset.WALL_1010).convert_alpha()
image_wall1001 = pygame.image.load(asset.WALL_1001).convert_alpha()
image_wall1011 = pygame.image.load(asset.WALL_1011).convert_alpha()
image_wall1110 = pygame.image.load(asset.WALL_1110).convert_alpha()
image_wall1111 = pygame.image.load(asset.WALL_1111).convert_alpha()
image_wall1101 = pygame.image.load(asset.WALL_1101).convert_alpha()
game = True
right = up = down = left = False
moulinette = classforthegame.Moulinette()
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
            if event.key == pygame.K_UP:
                left = right = down = False
                up = True
            if event.key == pygame.K_DOWN:
                left = right = up = False
                down = True
    pos_moulinette = moulinette.mouve(right, left, down, up, maze)
    pos_stu = stu.mouve()
    pos_piscin = piscin.mouve(pos_moulinette)
    for y in range(len(maze.themaze)):
        row = maze.themaze[y]
        w = 0

        for x in range(len(row)):
            wall = row[x].walls
            if wall & 1:
                w += 1
            if wall & 8:
                w += 1000
            if wall & 2:
                w += 10
            if wall & 4:
                w += 100
            if wall == 15:
                w = 1111
            if w == 0:
                fenetre.blit(image_wall0, (x * 80, y * 80))
            elif w == 1:
                fenetre.blit(image_wall1, (x * 80, y * 80))
            elif w == 10:
                fenetre.blit(image_wall10, (x * 80, y * 80))
            elif w == 11:
                fenetre.blit(image_wall11, (x * 80, y * 80))
            elif w == 100:
                fenetre.blit(image_wall100, (x * 80, y * 80))
            elif w == 101:
                fenetre.blit(image_wall101, (x * 80, y * 80))
            elif w == 110:
                fenetre.blit(image_wall110, (x * 80, y * 80))
            elif w == 111:
                fenetre.blit(image_wall111, (x * 80, y * 80))
            elif w == 1000:
                fenetre.blit(image_wall1000, (x * 80, y * 80))
            elif w == 1100:
                fenetre.blit(image_wall1100, (x * 80, y * 80))
            elif w == 1001:
                fenetre.blit(image_wall1001, (x * 80, y * 80))
            elif w == 1011:
                fenetre.blit(image_wall1011, (x * 80, y * 80))
            elif w == 1010:
                fenetre.blit(image_wall1010, (x * 80, y * 80))
            elif w == 1110:
                fenetre.blit(image_wall1110, (x * 80, y * 80))
            elif w == 1111:
                fenetre.blit(image_wall1111, (x * 80, y * 80))
            elif w == 1101:
                fenetre.blit(image_wall1101, (x * 80, y * 80))
            w = 0
    fenetre.blit(image_moulinette, (pos_moulinette[0] + 10 , pos_moulinette[1] + 10))
    #fenetre.blit(image_stu, pos_stu)
    #fenetre.blit(image_piscin, pos_piscin)
    pygame.display.flip()
