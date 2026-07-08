import pygame
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FPS = 60

taille = (1280, 960)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
CELL_SIZE = 80
SPRITE_SIZE = 60

BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

moulinette_front_images = []
for i in range(0, 3):
    moulinette_front_images.append(
        pygame.transform.scale(
            pygame.image.load(f"{BASE_DIR}/assets/sprite_cat_final{i}.png"),
            (SPRITE_SIZE, SPRITE_SIZE),
        )
    )

moulinette_back_images = []
for i in range(3, 6):
    moulinette_back_images.append(
        pygame.transform.scale(
            pygame.image.load(f"{BASE_DIR}/assets/sprite_cat_final{i}.png"),
            (SPRITE_SIZE, SPRITE_SIZE),
        )
    )
