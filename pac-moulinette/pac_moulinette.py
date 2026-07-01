import pygame
import classforthegame
from mazegenerator import MazeGenerator
from maze_wrapper import MazeLoader, LvlConfig
import asset

level = LvlConfig(width=16, height=12, seed=42)
maze_loader = MazeLoader(level)
maze = maze_loader.load()


pygame.init()
taille = (480, 480)
pygame.display.set_caption(asset.DRAGON_PATH)
fenetre = pygame.display.set_mode(taille, pygame.RESIZABLE)
fond = pygame.image.load(asset.MAZE_PATH).convert()
image_moulinette = pygame.image.load(asset.KNIGHT_PATH).convert_alpha()
image_stu = pygame.image.load(asset.DRAGON_PATH).convert_alpha()
image_piscin = pygame.image.load(asset.ELIOT_PATH).convert_alpha()
image_wall = pygame.image.load(asset.WALL_PATH).convert_alpha()
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
            if event.key == pygame.K_DOWN:
                left = right = up = False
                down = True
            if event.key == pygame.K_UP:
                left = right = down = False
                up = True
    pos_wall = (100, 100)
    pos_moulinette = moulinette.mouve(right, left, down, up, pos_wall)
    pos_stu = stu.mouve()
    pos_piscin = piscin.mouve(pos_moulinette)
    fenetre.blit(fond, (0, 0))
    fenetre.blit(image_moulinette, pos_moulinette)
    fenetre.blit(image_stu, pos_stu)
    fenetre.blit(image_piscin, pos_piscin)
    fenetre.blit(image_wall, pos_wall)
    pygame.display.flip()
print(maze.themaze[0][0].walls)
