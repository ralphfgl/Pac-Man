from typing import Any, List
import random

moul_size = 60


class Perssonage():
    def __init__(
        self,
        pos: List[Any],
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
            stat: int = 1,
            ):
        if pos is None:
            pos = [80 * 11, 1]
        super().__init__(
            pos,
            name,
            access,
            pv,
            atk,
            vitesse
        )
        self.life = life
        self.stat = stat
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

    def open_gate(self, pos: List, way: str, maze) -> bool:
        if way == "N":
            if maze.themaze[pos[1]][pos[0]].walls & 0b1 and (
                 self.pos[1] % 80 <= 1):
                return True
            if (not maze.themaze[pos[1]][pos[0]].walls & 0b1) and (
                 self.pos[0] // 80) != ((self.pos[0] + moul_size) // 80):
                return True
            if (not maze.themaze[pos[1]][pos[0]].walls & 0b1) and (
                 self.pos[0] % 80) <= 0 or ((
                     self.pos[0] + moul_size) % 80) >= 62:
                return True
        elif way == "W":
            if (maze.themaze[pos[1]][pos[0]].walls >> 3) & 0b1 and (
             self.pos[0] % 80 <= 1):
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 3) & 0b1) and (
                 self.pos[1] // 80) != ((self.pos[1] + moul_size) // 80):
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 3) & 0b1) and (
                 self.pos[1] % 80) <= 0 or ((
                     self.pos[1] + moul_size) % 80) >= 62:
                return True
        elif way == "E":
            if (maze.themaze[pos[1]][pos[0]].walls >> 1) & 0b1 and (
                 self.pos[0] + moul_size) % 80 >= 61:
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 1) & 0b1) and (
                 self.pos[1] // 80) != ((self.pos[1] + moul_size) // 80):
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 1) & 0b1) and (
                 self.pos[1] % 80) <= 0 or ((
                     self.pos[1] + moul_size) % 80) >= 62:
                return True
        elif way == "S":
            if (maze.themaze[pos[1]][pos[0]].walls >> 2) & 0b1 and (
                 self.pos[1] + moul_size) % 80 >= 61:
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 2) & 0b1) and (
                 self.pos[0] // 80) != ((self.pos[0] + moul_size) // 80):
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 2) & 0b1) and (
                 self.pos[0] % 80) <= 0 or ((
                     self.pos[0] + moul_size) % 80) >= 62:
                return True
        return False

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

    def mouve(self, maze, m_pos) -> List:
        direction = ["W", "E", "N", "S"]
        pos = []
        pos.append(self.pos[0] // 80)
        pos.append(self.pos[1] // 80)
        if self.open_gate(pos, "W", maze):
            direction.remove("W")
        if self.open_gate(pos, "E", maze):
            direction.remove("E")
        if self.open_gate(pos, "N", maze):
            direction.remove("N")
        if self.open_gate(pos, "S", maze):
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
        return self.chose_dir(direction[0])


class Piscineux(Perssonage):
    def __init__(
            self,
            pos: List = None,
            name: str = 'Jean',
            access: int = 1,
            pv: int = 100,
            atk: int = 50,
            vitesse: int = 1,
            dir: str = "Rien",
            one_dir: str = "rien",
            life: int = 1,
            fuit: bool = False
            ):
        if pos is None:
            pos = [80 * 8, 160]
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
        self.one_dir = one_dir
        self.fuit = fuit

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

    def faster(self, direction: List, m_pos) -> List[str]:
        long = self.pos[0] - m_pos[0]
        height = self.pos[1] - m_pos[1]
        if long != 0:
            if long > 0:
                direction.remove("E")
            if long < 0:
                direction.remove("W")
        else:
            direction.remove("W")
            direction.remove("E")
        if height != 0:
            if height < 0:
                direction.remove("N")
            if height > 0:
                direction.remove("S")
        else:
            direction.remove("N")
            direction.remove("S")
        return direction

    def open_gate(self, pos: List, way: str, maze) -> bool:
        if way == "N":
            if maze.themaze[pos[1]][pos[0]].walls & 0b1 and (
                 self.pos[1] % 80 <= 1):
                return True
            if (not maze.themaze[pos[1]][pos[0]].walls & 0b1) and (
                 self.pos[0] // 80) != ((self.pos[0] + moul_size) // 80):
                return True
            if (not maze.themaze[pos[1]][pos[0]].walls & 0b1) and (
                 self.pos[0] % 80) <= 0 or ((
                     self.pos[0] + moul_size) % 80) >= 62:
                return True
        elif way == "W":
            if (maze.themaze[pos[1]][pos[0]].walls >> 3) & 0b1 and (
                 self.pos[0] % 80 <= 1):
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 3) & 0b1) and (
                 self.pos[1] // 80) != ((self.pos[1] + moul_size) // 80):
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 3) & 0b1) and (
                 self.pos[1] % 80) <= 0 or ((
                     self.pos[1] + moul_size) % 80) >= 62:
                return True
        elif way == "E":
            if (maze.themaze[pos[1]][pos[0]].walls >> 1) & 0b1 and (
                 self.pos[0] + moul_size) % 80 >= 61:
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 1) & 0b1) and (
                 self.pos[1] // 80) != ((self.pos[1] + moul_size) // 80):
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 1) & 0b1) and (
                 self.pos[1] % 80) <= 0 or ((
                     self.pos[1] + moul_size) % 80) >= 62:
                return True
        elif way == "S":
            if (maze.themaze[pos[1]][pos[0]].walls >> 2) & 0b1 and (
                 self.pos[1] + moul_size) % 80 >= 61:
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 2) & 0b1) and (
                 self.pos[0] // 80) != ((
                     self.pos[0] + moul_size) // 80):
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 2) & 0b1) and (
                 self.pos[0] % 80) <= 0 or ((
                     self.pos[0] + moul_size) % 80) >= 62:
                return True
        return False

    def mouve(self, m_pos, maze) -> List:
        direction = ["E", "W", "N", "S"]
        pos = []
        pos.append(self.pos[0] // 80)
        pos.append(self.pos[1] // 80)
        if self.fuit is False:
            direction = self.faster(direction, m_pos)
            if "W" in direction and self.open_gate(pos, "W", maze):
                direction.remove("W")
            if "E" in direction and self.open_gate(pos, "E", maze):
                direction.remove("E")
            if "N" in direction and self.open_gate(pos, "N", maze):
                direction.remove("N")
            if "S" in direction and self.open_gate(pos, "S", maze):
                direction.remove("S")
            if not direction:
                return self.pos
        else:
            if self.open_gate(pos, "W", maze):
                direction.remove("W")
            if self.open_gate(pos, "E", maze):
                direction.remove("E")
            if self.open_gate(pos, "N", maze):
                direction.remove("N")
            if self.open_gate(pos, "S", maze):
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
        return self.chose_dir(direction[0])


class Moulinette(Perssonage):
    def __init__(
            self,
            pos: List = None,
            name: str = 'Moulinette',
            access: int = 1,
            pv: int = 100,
            atk: int = 50,
            vitesse: int = 1,
            next_dir: str = "rien",
            one_dir: str = "rien"
            ):
        if pos is None:
            pos = [0, 1]
        super().__init__(
            pos,
            name,
            access,
            pv,
            atk,
            vitesse
        )
        self.next_dir = next_dir
        self.one_dir = one_dir

    def spe(self):
        pass

    def open_gate(self, pos: List, way: str, maze) -> bool:
        if way == "N":
            if maze.themaze[pos[1]][pos[0]].walls & 0b1 and (
                 self.pos[1] % 80 <= 1):
                return True
            if (not maze.themaze[pos[1]][pos[0]].walls & 0b1) and (
                 self.pos[0] // 80) != ((
                     self.pos[0] + moul_size) // 80):
                return True
            if (not maze.themaze[pos[1]][pos[0]].walls & 0b1) and (
                 self.pos[0] % 80) <= 0 or ((
                     self.pos[0] + moul_size) % 80) >= 62:
                return True
        elif way == "W":
            if (maze.themaze[pos[1]][pos[0]].walls >> 3) & 0b1 and (
                 self.pos[0] % 80 <= 1):
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 3) & 0b1) and (
                 self.pos[1] // 80) != ((self.pos[1] + moul_size) // 80):
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 3) & 0b1) and (
                 self.pos[1] % 80) <= 0 or ((
                     self.pos[1] + moul_size) % 80) >= 62:
                return True
        elif way == "E":
            if (maze.themaze[pos[1]][pos[0]].walls >> 1) & 0b1 and (
                 self.pos[0] + moul_size) % 80 >= 61:
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 1) & 0b1) and (
                 self.pos[1] // 80) != ((self.pos[1] + moul_size) // 80):
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 1) & 0b1) and (
                 self.pos[1] % 80) <= 0 or ((
                     self.pos[1] + moul_size) % 80) >= 62:
                return True
        elif way == "S":
            if (maze.themaze[pos[1]][pos[0]].walls >> 2) & 0b1 and (
                 self.pos[1] + moul_size) % 80 >= 61:
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 2) & 0b1) and (
                 self.pos[0] // 80) != ((
                     self.pos[0] + moul_size) // 80):
                return True
            if (not (maze.themaze[pos[1]][pos[0]].walls >> 2) & 0b1) and (
                 self.pos[0] % 80) <= 0 or ((
                     self.pos[0] + moul_size) % 80) >= 62:
                return True
        return False

    def mouve(
            self,
            right: bool,
            left: bool,
            down: bool,
            up: bool,
            maze) -> List:
        pos = []
        pos.append(self.pos[0] // 80)
        pos.append(self.pos[1] // 80)
        if right is True:
            self.next_dir = "right"
        if left is True:
            self.next_dir = "left"
        if up is True:
            self.next_dir = "up"
        if down is True:
            self.next_dir = "down"
        if self.open_gate(pos, "W", maze):
            left = False
        else:
            if self.next_dir == "left":
                self.pos[0] -= self.vitesse
                self.one_dir = "W"
                return self.pos
        if self.open_gate(pos, "E", maze):
            right = False
        else:
            if self.next_dir == "right":
                self.pos[0] += self.vitesse
                self.one_dir = "E"
                return self.pos
        if self.open_gate(pos, "N", maze):
            up = False
        else:
            if self.next_dir == "up":
                self.pos[1] -= self.vitesse
                self.one_dir = "N"
                return self.pos
        if self.open_gate(pos, "S", maze):
            down = False
        else:
            if self.next_dir == "down":
                self.pos[1] += self.vitesse
                self.one_dir = "S"
                return self.pos

        if self.pos[0] <= 0 or self.open_gate(pos, self.one_dir, maze):
            pass
        else:
            if self.one_dir == "W":
                self.pos[0] -= self.vitesse
            elif self.one_dir == "E":
                self.pos[0] += self.vitesse
            elif self.one_dir == "N":
                self.pos[1] -= self.vitesse
            elif self.one_dir == "S":
                self.pos[1] += self.vitesse
        return self.pos
