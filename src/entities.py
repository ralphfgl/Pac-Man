from macro import *
import pygame


class Player:
    """Player class"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = CELL_SIZE
        self.speed = 3
        self.direction = "E"

    def open_gate(self, room: int, way: str) -> bool:
        print(
            f"{self.x} and {self.y} and divided = {self.x % CELL_SIZE} and {self.y % CELL_SIZE}"
        )
        if way == "N" and self.y % CELL_SIZE <= CELL_SIZE // 2:
            return not room & 0b1
        elif way == "W" and self.x % CELL_SIZE <= CELL_SIZE // 2:
            return not (room >> 3) & 0b1
        elif way == "E" and self.x % CELL_SIZE >= CELL_SIZE // 2:
            return not (room >> 1) & 0b1
        elif way == "S" and 1 < self.y % CELL_SIZE >= CELL_SIZE // 2:
            return not (room >> 2) & 0b1
        return True

    def move(self, keys, maze):
        """Move with collision"""
        new_x, new_y = self.x, self.y
        direction = None

        if keys[pygame.K_LEFT]:
            new_x -= self.speed
            direction = "W"
        if keys[pygame.K_RIGHT]:
            new_x += self.speed
            direction = "E"
        if keys[pygame.K_UP]:
            new_y -= self.speed
            direction = "N"
        if keys[pygame.K_DOWN]:
            new_y += self.speed
            direction = "S"

        if direction:
            self.direction = direction

        if direction and not self._check_collision(
            new_x, new_y, maze, direction
        ):
            self.x, self.y = new_x, new_y

    def _check_collision(self, x, y, maze, direction):
        """Check wall collision"""

        current_grid_x = int(self.x // CELL_SIZE)
        current_grid_y = int(self.y // CELL_SIZE)
        new_grid_x = int(x // CELL_SIZE)
        new_grid_y = int(y // CELL_SIZE)

        current_walls = maze.themaze[current_grid_y][current_grid_x].walls
        if not self.open_gate(current_walls, direction):
            return True

        if current_grid_x == new_grid_x and current_grid_y == new_grid_y:
            return False

        if not (
            0 <= new_grid_x < maze.width and 0 <= new_grid_y < maze.height
        ):
            return True

        if maze.themaze[new_grid_y][new_grid_x].static:
            return True

        return False
