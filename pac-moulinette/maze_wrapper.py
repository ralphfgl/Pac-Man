from sys import stderr
from parser import Parser
from mazegenerator import MazeGenerator  # type: ignore
from parser import LvlConfig, Config
from typing import List
import random
import sys


class Cellule:
    """Structure with cell data"""

    def __init__(self, walls: int, static: bool) -> None:
        self.walls: int = walls
        self.static: bool = static


class Maze:
    """Maze structure"""

    def __init__(
        self, width: int, height: int, themaze: List[List[Cellule]]
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.themaze: List[List[Cellule]] = themaze

    def open_gate(self, room: int, way: str) -> bool:
        if way == "N":
            return not room & 0b1
        elif way == "W":
            return not (room >> 3) & 0b1
        elif way == "E":
            return not (room >> 1) & 0b1
        elif way == "S":
            return not (room >> 2) & 0b1
        return False


class MazeLoader:
    """Load the level config and generates the maze"""

    def __init__(self, lvl: LvlConfig, conf: Config):
        self.lvl = lvl
        self.conf = conf

    def load(self, apply_seed: bool = True) -> Maze:
        try:
            if apply_seed and self.conf.seed is not None:
                seed = self.conf.seed
            else:
                seed = random.randint(1, 9999)
            generator = MazeGenerator(
                (self.lvl.width, self.lvl.height), False, seed=seed
            )

        except Exception as e:
            print(
                f"[STDERR] - Failed to generate the maze, error: {e}",
                file=stderr,
            )
            sys.exit(1)

        themaze = []
        for y in generator.maze:
            cell = []
            for x in y:
                cell.append(Cellule(walls=x, static=x == 15))
            themaze.append(cell)
        return Maze(self.lvl.width, self.lvl.height, themaze)


if __name__ == "__main__":
    print("Testing maze")
    level = LvlConfig(width=16, height=12)
    parser = Parser("../config.json")
    config = parser.load()

    maze_loader = MazeLoader(level, config)
    maze = maze_loader.load()

    print(f"Maze: {maze.width}x{maze.height}")

    wc = "█"
    row: List[Cellule] = []
    for y in range(len(maze.themaze)):
        row = maze.themaze[y]
        left: str = ""
        right: str = ""
        up: str = ""
        middle: str = ""

        for x in range(len(row)):
            wall = row[x].walls
            if wall & 1:
                up += f"{wc}{wc}{wc}{wc}{wc}"
            else:
                up += f"{wc}   {wc}"
            if wall & 8:
                left = f"{wc}"
            else:
                left = " "
            if wall & 2:
                right = f"{wc}"
            else:
                right = " "
            if wall == 15:
                middle += f"{wc}{wc}{wc}{wc}{wc}"
            else:
                middle += f"{left}   {right}"
        print(f"{up}")
        print(f"{middle}")
    print(f"{wc}{wc}{wc}{wc}{wc}" * len(row))
