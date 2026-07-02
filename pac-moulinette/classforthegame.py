from typing import Any, List
from abc import abstractmethod
import random
from maze_wrapper import MazeLoader, LvlConfig

moul_size = 60

class Perssonage():
    def __init__(
        self,
        pos: List,
        name: str,
        access: int,
        pv: int,
        atk: int,
        vitesse: int
    ) -> None:
        self.pos: List = pos
        self.name: str = name
        self.access: int = access
        self.pv: int = pv
        self.atk: int = atk
        self.vitesse: int = vitesse

    @abstractmethod
    def mouve() -> List:
        pass


class Monstre(Perssonage):
    def __init__(
            self,
            pos,
            name,
            access,
            pv,
            atk,
            vitesse
            ):
        super().__init__(
            pos,
            name,
            access,
            pv,
            atk,
            vitesse
        )

    @abstractmethod
    def spe() -> Any:
        pass

    @abstractmethod
    def mouve() -> List:
        pass


class Stud(Perssonage):
    def __init__(
            self,
            pos: List = None,
            name: str = 'Corentin',
            access: int = 1,
            pv: int = 100,
            atk: int = 50,
            vitesse: int = 1,
            dir: str = "Rien",
            life: int = 1,
            pace: int = 4,
            ):
        if pos is None:
            pos = [0, 0]
        super().__init__(
            pos,
            name,
            access,
            pv,
            atk,
            vitesse
        )
        self.life = life
        self.pace = pace
        self.dir = dir

    def chose_dir(self, direction: List) -> List:
        if direction == "W":
            self.pos[0] -= self.vitesse
        if direction == "E":
            self.pos[0] += self.vitesse
        if direction == "S":
            self.pos[1] += self.vitesse
        if direction == "N":
            self.pos[1] -= self.vitesse
        return self.pos

    def spe(self) -> Any:
        if self.pv < 80 and self.pace == 4:
            self.vitesse = self.vitesse * 1.2
            self.pace -= 1
        if self.pv < 60 and self.pace == 3:
            self.vitesse = self.vitesse * 1.2
            self.pace -= 1
        if self.pv < 40 and self.pace == 2:
            self.vitesse = self.vitesse * 1.2
            self.pace -= 1
        if self.pv < 20 and self.pace == 1:
            self.vitesse = self.vitesse * 2
            self.pace -= 1

    def open_gate(self, pos: List, way: str, maze) -> bool:
        if way == "N":
            if maze.themaze[pos[1]][pos[0]].walls & 0b1 and self.pos[1] % 80 <= 1:
                return True
        elif way == "W":
            if (maze.themaze[pos[1]][pos[0]].walls >> 3) & 0b1 and self.pos[0] % 80 <= 1:
                return True
        elif way == "E":
            if (maze.themaze[pos[1]][pos[0]].walls >> 1) & 0b1 and self.pos[0] % 80 >= 1:
                return True
        elif way == "S":
            if (maze.themaze[pos[1]][pos[0]].walls >> 2) & 0b1 and self.pos[1] % 80 >= 1:
                return True
        return False

    def mouve(self, maze) -> List:
        direction = ["W", "E", "N", "S"]
        pos = []
        pos.append(self.pos[0] // 80)
        pos.append(self.pos[1] // 80)
        if self.pos[0] <= 0 or self.open_gate(pos, "W", maze):
            direction.remove("W")
        if self.pos[0] + 80 >= 1280 or self.open_gate(pos, "E", maze):
            direction.remove("E")
        if self.pos[1] <= 0 or self.open_gate(pos, "N", maze):
            direction.remove("N")
        if self.pos[1] + 80 >= 960 or self.open_gate(pos, "S", maze):
            direction.remove("S")
        if self.dir not in direction:
            direction = random.choice(direction)
            self.dir = direction
            return self.chose_dir(direction)
        if self.dir == "W" and "E" in direction:
            direction.remove("E")
        elif self.dir == "E" and "W" in direction:
            direction.remove("W")
        elif self.dir == "S" and "N" in direction:
            direction.remove("N")
        elif self.dir == "N" and "S" in direction:
            direction.remove("S")
        direction = random.choice(direction)
        self.dir = direction
        pos.pop()
        pos.pop()
        return self.chose_dir(direction)


class Piscineux(Perssonage):
    def __init__(
            self,
            pos: List = None,
            name: str = 'Jean',
            access: int = 1,
            pv: int = 100,
            atk: int = 50,
            vitesse: int = 0.5,
            dir: str = "Rien",
            life: int = 1,
            ):
        if pos is None:
            pos = [0, 0]
        super().__init__(
            pos,
            name,
            access,
            pv,
            atk,
            vitesse
        )
        self.life = life
        self.dir = dir

    def chose_dir(self, direction: List) -> List:
        if direction[0] == "W":
            self.pos[0] -= self.vitesse
        if direction[0] == "E":
            self.pos[0] += self.vitesse
        if direction[0] == "S":
            self.pos[1] += self.vitesse
        if direction[0] == "N":
            self.pos[1] -= self.vitesse
        return self.pos

    def spe(self) -> Any:
        pass

    def faster(self, direction, m_pos) -> List[str]:
        long = self.pos[0] - m_pos[0]
        height = self.pos[1] - m_pos[1]
        if long > 0:
            direction[0] = "W"
            direction[1] = "E"
        if height < 0:
            direction[2] = "S"
            direction[3] = "N"
        if long == 0:
            temp = direction[0]
            temp2 = direction[1]
            direction[0] = direction[2]
            direction[1] = direction[3]
            direction[2] = temp
            direction[3] = temp2
        return direction

    def mouve(self, m_pos) -> List:
        direction = ["E", "W", "N", "S"]
        direction = self.faster(direction, m_pos)
        if self.pos[0] <= 0:
            direction.remove("W")
        if self.pos[0] >= 1280:
            direction.remove("E")
        if self.pos[1] <= 0:
            direction.remove("N")
        if self.pos[1] >= 960:
            direction.remove("S")
        return self.chose_dir(direction)


class Moulinette(Perssonage):
    def __init__(
            self,
            pos: List = None,
            name: str = 'Moulinette',
            access: int = 1,
            pv: int = 100,
            atk: int = 50,
            vitesse: int = 1,
            ):
        if pos is None:
            pos = [0, 0]
        super().__init__(
            pos,
            name,
            access,
            pv,
            atk,
            vitesse
        )
        self.pos = pos

    def spe(self):
        pass

    def open_gate(self, pos: List, way: str, maze) -> bool:
        if way == "N":
            if maze.themaze[pos[1]][pos[0]].walls & 0b1 and self.pos[1] % 80 <= 0:
                return True
            if (not maze.themaze[pos[1]][pos[0]].walls & 0b1) and (self.pos[0] // 80) != ((self.pos[0] + moul_size) // 80):
                return True
        elif way == "W":
            if (maze.themaze[pos[1]][pos[0]].walls >> 3) & 0b1 and self.pos[0] % 80 <= 1:
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 3) & 0b1) and (self.pos[1] // 80) != ((self.pos[1] + moul_size) // 80):
                return True
        elif way == "E":
            if (maze.themaze[pos[1]][pos[0]].walls >> 1) & 0b1 and self.pos[0] % 80 >= 1:
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 1) & 0b1) and (self.pos[1] // 80) != ((self.pos[1] + moul_size) // 80):
                return True
        elif way == "S":
            if (maze.themaze[pos[1]][pos[0]].walls >> 2) & 0b1 and self.pos[1] % 80 >= 1:
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 2) & 0b1) and (self.pos[0] // 80) != ((self.pos[0] + moul_size) // 80):
                return True
        return False

    def mouve(self, right: bool, left: bool, down: bool, up: bool, maze) -> List:
        pos = []
        pos.append(self.pos[0] // 80)
        pos.append(self.pos[1] // 80)
        if self.pos[0] <= 0 or self.open_gate(pos, "W", maze):
            left = False
        if self.pos[0] + moul_size >= 1280 or self.open_gate(pos, "E", maze):
            right = False
        if self.pos[1] <= 0 or self.open_gate(pos, "N", maze):
            up = False
        if self.pos[1] + moul_size >= 960 or self.open_gate(pos, "S", maze):
            down = False
        if right is True and self.pos[0] + moul_size <= 1280:
            self.pos[0] += self.vitesse
        if left is True and self.pos[0] > 0:
            self.pos[0] -= self.vitesse
        if down is True and self.pos[1] + moul_size <= 960:
            self.pos[1] += self.vitesse
        if up is True and self.pos[1] > 0:
            self.pos[1] -= self.vitesse
        return self.pos
