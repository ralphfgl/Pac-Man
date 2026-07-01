from typing import Any, List
from abc import abstractmethod
import random


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
            vitesse: int = 0.2,
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
        print(self.pos)
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

    def mouve(self) -> List:
        direction = ["W", "E", "N", "S"]
        if self.pos[0] <= 0:
            direction.remove("W")
        if self.pos[0] >= 480:
            direction.remove("E")
        if self.pos[1] <= 0:
            direction.remove("N")
        if self.pos[1] >= 480:
            direction.remove("S")
        if self.dir not in direction:
            direction = random.choice(direction)
            return self.chose_dir(direction)
        elif self.dir == "W":
            direction.remove("E")
        elif self.dir == "E":
            direction.remove("W")
        elif self.dir == "S":
            direction.remove("")
        elif self.dir == "W":
            direction.remove("E")
        direction = random.choice(direction)
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
        if self.pos[0] >= 480:
            direction.remove("E")
        if self.pos[1] <= 0:
            direction.remove("N")
        if self.pos[1] >= 480:
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

    def mouve(self, right: bool, left: bool, down: bool, up: bool) -> List:
        if right is True and self.pos[0] < 480:
            self.pos[0] += self.vitesse
        if left is True and self.pos[0] > 0:
            self.pos[0] -= self.vitesse
        if down is True and self.pos[1] < 480:
            self.pos[1] += self.vitesse
        if up is True and self.pos[1] > 0:
            self.pos[1] -= self.vitesse
        return self.pos
