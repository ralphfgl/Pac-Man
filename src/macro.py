import pygame
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FPS = 60

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
CELL_SIZE = 30

BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

player_images = []
for i in range(1, 4):
    player_images.append(
        pygame.transform.scale(
            pygame.image.load(f"{BASE_DIR}/assets/player/pacman_{i}.png"),
            (CELL_SIZE, CELL_SIZE),
        )
    )
