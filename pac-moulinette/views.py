# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rfeghali <rfeghali@learner.42.tech>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/07/10 21:08:23 by rfeghali          #+#    #+#              #
#    Updated: 2026/07/11 08:53:36 by rfeghali         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import json
import random
from parser import Parser, Config
from enum import Enum
from macro import *
import sys
from abc import ABC, abstractmethod
from collections.abc import Iterable
import pygame
import classforthegame
from maze_wrapper import MazeLoader, Maze
from highscore import HighscoreManager
from typing import List, Dict, Optional


class Pacgum:
    """Pacgum class"""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.active = True

    def draw(self, screen: pygame.Surface) -> None:
        if not self.active:
            return
        screen.blit(image_pacgum, (self.x, self.y))


class SuperPacgum:
    """SuperPacgum class"""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.active = True

    def draw(self, screen: pygame.Surface) -> None:
        if not self.active:
            return
        screen.blit(image_TIG, (self.x, self.y))


class GameState(Enum):
    MAIN_MENU = 1
    PLAYING = 2
    PAUSED = 3
    HIGH_SCORES = 4
    GAME_OVER = 5
    INSTRUCTIONS = 6
    LEVEL_COMPLETE = 7
    VICTORY = 8


class View(ABC):
    """Base class for all views"""

    def __init__(self, screen: pygame.Surface, config: Config) -> None:
        """Initialize the view"""
        self.screen = screen
        self.config = config
        self.next_state: Optional[GameState] = None
        self.font = pygame.font.Font(None, 48)

    @abstractmethod
    def handle_event(self, events: Iterable[pygame.event.Event]) -> None:
        """Process input events"""
        pass

    @abstractmethod
    def draw(self) -> None:
        """Render the view"""
        pass

    def get_next_state(self) -> Optional[GameState]:
        """Return the next game state to transition to"""
        return self.next_state

    def reset(self) -> None:
        """Reset view state when entering"""
        self.next_state = None


class MainMenuView(View):
    def __init__(self, screen: pygame.Surface, config: Config) -> None:
        super().__init__(screen, config)
        self.selected_item = 0
        self.menu_items = [
            ("Play Game", GameState.PLAYING),
            ("View Highscores", GameState.HIGH_SCORES),
            ("Instructions", GameState.INSTRUCTIONS),
            ("Exit", None),
        ]

    def handle_event(self, events: Iterable[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(
                        self.menu_items
                    )
                elif event.key == pygame.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(
                        self.menu_items
                    )
                elif event.key == pygame.K_RETURN:
                    _, next_state = self.menu_items[self.selected_item]
                    if next_state is None:
                        pygame.quit()
                        sys.exit()
                    self.next_state = next_state

    def draw(self) -> None:
        self.screen.fill(BLACK)
        title = self.font.render("PAC-MAN", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        for i, (text, _) in enumerate(self.menu_items):
            color = GREEN if i == self.selected_item else WHITE
            item = self.font.render(text, True, color)
            item_rect = item.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 80))
            self.screen.blit(item, item_rect)


class PauseView(View):
    def __init__(self, screen: pygame.Surface, config: Config) -> None:
        super().__init__(screen, config)
        self.selected_item = 0
        self.menu_items = [
            ("Resume", GameState.PLAYING),
            ("Main Menu", GameState.MAIN_MENU),
        ]

    def handle_event(self, events: Iterable[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = GameState.PLAYING
                elif event.key == pygame.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(
                        self.menu_items
                    )
                elif event.key == pygame.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(
                        self.menu_items
                    )
                elif event.key == pygame.K_RETURN:
                    _, self.next_state = self.menu_items[self.selected_item]

    def draw(self) -> None:
        screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.fill(BLACK)
        self.screen.blit(screen, (0, 0))

        pause_text = self.font.render("PAUSED", True, YELLOW)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(pause_text, pause_rect)

        for i, (text, _) in enumerate(self.menu_items):
            color = GREEN if i == self.selected_item else WHITE
            item = self.font.render(text, True, color)
            item_rect = item.get_rect(center=(SCREEN_WIDTH // 2, 350 + i * 80))
            self.screen.blit(item, item_rect)


class InstructionsView(View):
    """Display game controls"""

    def __init__(self, screen: pygame.Surface, config: Config) -> None:
        super().__init__(screen, config)

    def handle_event(self, events: Iterable[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.next_state = GameState.MAIN_MENU

    def draw(self) -> None:
        self.screen.fill(BLACK)
        title = self.font.render("HOW TO PLAY", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        text = (
            "Objectives:\nNavigate the maze, collect pacgum,\nand run from the ghosts\n\n\n"
            "\nCommands:"
            "\nARROWS  - Move PacMan"
            "\nP       - Pause Game"
            "\nC       - Cheat Mode"
        )
        y = 100
        for line in text.split("\n"):
            surface = self.font.render(line, True, WHITE)
            surface_rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(surface, surface_rect)
            y += self.font.get_linesize()
        back = self.font.render("Press Return to go back", True, GRAY)
        back_rect = back.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        )
        self.screen.blit(back, back_rect)


class HighscoreView(View):
    """Show leaderboard imported from highscore.json file"""

    def __init__(self, screen: pygame.Surface, config: Config) -> None:
        super().__init__(screen, config)
        self.scores: List[Dict[str, str]] = []
        self.highscore_file = config.highscore_filename

    def reset(self) -> None:
        """Load scores when entering view"""

        super().reset()
        self.scores = self._load_scores()

    def _load_scores(self) -> List[Dict[str, str]]:
        """Load scores from JSON file"""

        try:
            with open(self.highscore_file, "r") as f:
                scores: List[Dict[str, str]] = json.load(f)
                scores.sort(key=lambda x: x["score"], reverse=True)
                return scores[:10]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def handle_event(self, events: Iterable[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.next_state = GameState.MAIN_MENU

    def draw(self) -> None:
        self.screen.fill(BLACK)
        title = self.font.render("HIGH SCORES", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, 80))
        self.screen.blit(title, title_rect)
        if not self.scores:
            no_scores = self.font.render("No scores yet!", True, WHITE)
            no_scores_rect = no_scores.get_rect(
                center=(SCREEN_WIDTH // 2, 300)
            )
            self.screen.blit(no_scores, no_scores_rect)
        else:
            rank_header = self.font.render("RANK", True, GREEN)
            self.screen.blit(rank_header, (150, 150))
            name_header = self.font.render("NAME", True, GREEN)
            self.screen.blit(name_header, (300, 150))
            score_header = self.font.render("SCORE", True, GREEN)
            self.screen.blit(score_header, (550, 150))
            pygame.draw.line(self.screen, WHITE, (150, 185), (750, 185), 2)

            y = 200
            for i, entry in enumerate(self.scores, start=1):
                rank_text = self.font.render(f"{i}.", True, WHITE)
                self.screen.blit(rank_text, (150, y))
                name_text = self.font.render(entry["name"], True, WHITE)
                self.screen.blit(name_text, (300, y))
                score_text = self.font.render(
                    str(entry["score"]), True, YELLOW
                )
                self.screen.blit(score_text, (550, y))
                y += 50
        back = self.font.render("Press RETURN to go back", True, GRAY)
        back_rect = back.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        )
        self.screen.blit(back, back_rect)


class GameOverView(View):
    """Game over screen"""

    def __init__(
        self,
        screen: pygame.Surface,
        config: Config,
        highscore_manager: HighscoreManager,
    ) -> None:
        super().__init__(screen, config)
        self.highscore_manager = highscore_manager
        self.score = 0
        self.entering_name = True
        self.name = ""
        self.saved = False

    def reset(self) -> None:
        super().reset()
        self.entering_name = True
        self.name = ""
        self.saved = False

    def handle_event(self, events: Iterable[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.entering_name == True:
                    if event.key == pygame.K_RETURN:
                        if self.name.strip():
                            self.saved = self.highscore_manager.add_score(
                                self.name.strip(), self.score
                            )
                        self.entering_name = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif (
                        event.unicode
                        and event.unicode.isascii()
                        and event.unicode.isalnum()
                        or event.unicode == " "
                        and len(self.name) < 10
                    ):
                        self.name += event.unicode
                elif event.key == pygame.K_RETURN:
                    self.next_state = GameState.MAIN_MENU

    def draw(self) -> None:
        self.screen.fill(BLACK)
        title = self.font.render("GAME OVER", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 130))
        self.screen.blit(title, title_rect)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 230))
        self.screen.blit(score_text, score_rect)

        if self.entering_name:
            prompt = self.font.render("Enter your name:", True, YELLOW)
            prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, 330))
            self.screen.blit(prompt, prompt_rect)

            name = self.font.render(self.name + "_", True, GREEN)
            name_rect = name.get_rect(center=(SCREEN_WIDTH // 2, 400))
            self.screen.blit(name, name_rect)

            instruction = self.font.render(
                "Letters, numbers, spaces (max 10) - RETURN to confirm",
                True,
                GRAY,
            )
            hint_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, 460))
            self.screen.blit(instruction, hint_rect)
        else:
            message = "Score saved !" if self.saved else "Score not saved"
            text = self.font.render(message, True, WHITE)
            self.screen.blit(
                text,
                text.get_rect(center=(SCREEN_WIDTH // 2, 300)),
            )
            back = self.font.render("Press RETURN to continue", True, GRAY)
            self.screen.blit(
                back, back.get_rect(center=(SCREEN_WIDTH // 2, 400))
            )


class VictoryView(View):
    """Victory screen"""

    def __init__(
        self,
        screen: pygame.Surface,
        config: Config,
        highscore_manager: HighscoreManager,
    ):
        super().__init__(screen, config)
        self.highscore_manager = highscore_manager
        self.score = 0
        self.entering_name = True
        self.name = ""
        self.saved = False

    def reset(self) -> None:
        super().reset()
        self.entering_name = True
        self.name = ""
        self.saved = False

    def handle_event(self, events: Iterable[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.entering_name == True:
                    if event.key == pygame.K_RETURN:
                        if self.name.strip():
                            self.saved = self.highscore_manager.add_score(
                                self.name.strip(), self.score
                            )
                        self.entering_name = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif (
                        event.unicode
                        and event.unicode.isascii()
                        and event.unicode.isalnum()
                        or event.unicode == " "
                        and len(self.name) < 10
                    ):
                        self.name += event.unicode
                elif event.key == pygame.K_RETURN:
                    self.next_state = GameState.MAIN_MENU

    def draw(self) -> None:
        self.screen.fill(BLACK)
        title = self.font.render("YOU WON !", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 130))
        self.screen.blit(title, title_rect)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 230))
        self.screen.blit(score_text, score_rect)

        if self.entering_name:
            prompt = self.font.render("Enter your name:", True, YELLOW)
            prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, 330))
            self.screen.blit(prompt, prompt_rect)

            name = self.font.render(self.name + "_", True, GREEN)
            name_rect = name.get_rect(center=(SCREEN_WIDTH // 2, 400))
            self.screen.blit(name, name_rect)

            instruction = self.font.render(
                "Letters, numbers, spaces (max 10) - RETURN to confirm",
                True,
                GRAY,
            )
            hint_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, 460))
            self.screen.blit(instruction, hint_rect)
        else:
            message = "Score saved !" if self.saved else "Score not saved !"
            text = self.font.render(message, True, WHITE)
            self.screen.blit(
                text,
                text.get_rect(center=(SCREEN_WIDTH // 2, 300)),
            )
            back = self.font.render("Press RETURN to continue", True, GRAY)
            self.screen.blit(
                back, back.get_rect(center=(SCREEN_WIDTH // 2, 400))
            )


class GameplayView(View):
    """Main game view with maze"""

    def __init__(self, screen: pygame.Surface, config: Config) -> None:
        super().__init__(screen, config)
        self.maze_loader: Optional[MazeLoader] = None
        self.maze: Maze
        self.player = None
        self.current_level = 0
        self.score = 0
        self.lives = 0
        self.animation_counter = 0
        self.pacgums: List[Pacgum] = []
        self.super_pacgums: List[SuperPacgum] = []

    def reset(self) -> None:
        """Start game when entering this view"""
        super().reset()
        self.current_level = 0
        self.score = 0
        self.lives = self.config.lives
        self._load_level()

    def _load_level(self) -> None:
        """Load a level from config"""
        self.maze_loader = MazeLoader(
            self.config.levels[self.current_level], self.config
        )
        self.maze = self.maze_loader.load(apply_seed=(self.current_level == 0))
        self.moulinette = classforthegame.Moulinette(
            [
                60 * (self.maze.width // 2) - 10,
                60 * (self.maze.height // 2) - 10,
            ]
        )
        self.level_start_ticks = pygame.time.get_ticks()
        self.pause_start: Optional[int] = None
        self._spawn()

    def _spawn(self) -> None:
        self.level_setup = [
            {
                "stud": [
                    (0, 1),
                    (self.maze.width - 1, 1),
                    (1, self.maze.height - 1),
                    (self.maze.width - 1, self.maze.height - 1),
                ],
                "piscin": [None],
            },
            {
                "stud": [
                    (0, 1),
                    (self.maze.width - 1, 1),
                    (1, self.maze.height - 1),
                    (self.maze.width - 1, self.maze.height - 1),
                ],
            },
            {
                "stud": [
                    (0, 1),
                    (self.maze.width - 1, 1),
                    (1, self.maze.height - 1),
                ],
                "piscin": [
                    (self.maze.width - 1, self.maze.height - 1),
                ],
            },
            {
                "stud": [
                    (0, 1),
                    (self.maze.width - 1, 1),
                    (1, self.maze.height - 1),
                ],
                "piscin": [
                    (self.maze.width - 1, self.maze.height - 1),
                ],
            },
            {
                "stud": [
                    (0, 1),
                    (self.maze.width - 1, 1),
                ],
                "piscin": [
                    (1, self.maze.height - 1),
                    (self.maze.width - 1, self.maze.height - 1),
                ],
            },
            {
                "stud": [
                    (0, 1),
                    (self.maze.width - 1, 1),
                ],
                "piscin": [
                    (1, self.maze.height - 1),
                    (self.maze.width - 1, self.maze.height - 1),
                ],
            },
            {
                "stud": [
                    (0, 1),
                ],
                "piscin": [
                    (self.maze.width - 1, 1),
                    (1, self.maze.height - 1),
                    (self.maze.width - 1, self.maze.height - 1),
                ],
            },
            {
                "stud": [
                    (0, 1),
                ],
                "piscin": [
                    (self.maze.width - 1, 1),
                    (1, self.maze.height - 1),
                    (self.maze.width - 1, self.maze.height - 1),
                ],
            },
            {
                "stud": [None],
                "piscin": [
                    (0, 1),
                    (),
                    (self.maze.width - 1, 1),
                    (1, self.maze.height - 1),
                    (self.maze.width - 1, self.maze.height - 1),
                ],
            },
            {
                "stud": [None],
                "piscin": [
                    (0, 1),
                    (),
                    (self.maze.width - 1, 1),
                    (1, self.maze.height - 1),
                    (self.maze.width - 1, self.maze.height - 1),
                ],
            },
        ]
        self.level = self.level_setup[self.current_level]
        self.studs = []
        if self.level["stud"]:
            for x, y in self.level["stud"]:
                self.studs.append(
                    classforthegame.Stud([x * 60 - 10, y * 60 - 10])
                )

        self.piscins = []
        if self.level["piscin"]:
            for x, y in self.level["piscin"]:
                self.piscins.append(
                    classforthegame.Piscineux([x * 60 - 10, y * 60 - 10])
                )

        self.pacgums = []
        super_position = [
            (0, 0),
            (self.maze.width - 1, 0),
            (0, self.maze.height - 1),
            (self.maze.width - 1, self.maze.height - 1),
            (self.maze.width // 2, self.maze.height // 2),
        ]

        available_tiles = []
        for y, row in enumerate(self.maze.themaze):
            for x, cell in enumerate(row):
                if cell.static or (x, y) in super_position:
                    continue
                available_tiles.append((x, y))
        pacgum_position = random.sample(available_tiles, self.config.pacgum)
        for x, y in pacgum_position:
            self.pacgums.append(Pacgum(x * 60 - 10, y * 60 - 10))

        self.super_pacgums = []
        super_position.pop()
        for x, y in super_position:
            self.super_pacgums.append(SuperPacgum(x * 60, y * 60))

    def _second_remaining(self) -> float:
        passed_time_ms = pygame.time.get_ticks() - self.level_start_ticks
        remaining = self.config.level_max_time - (passed_time_ms / 1000)
        return max(0.0, remaining)

    def handle_event(self, events: Iterable[pygame.event.Event]) -> None:
        right = left = down = up = False
        if self.pause_start is not None:
            self.level_start_ticks += (
                pygame.time.get_ticks() - self.pause_start
            )
            self.pause_start = None
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause_start = pygame.time.get_ticks()
                    self.next_state = GameState.PAUSED
                if event.key == pygame.K_y:
                    self.lives = 0
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_c:
                    self.current_level = (self.current_level + 1) % len(
                        self.config.levels
                    )
                    self._load_level()
                elif event.key == pygame.K_RIGHT:
                    left = up = down = False
                    right = True
                elif event.key == pygame.K_LEFT:
                    right = up = down = False
                    left = True
                elif event.key == pygame.K_UP:
                    left = right = down = False
                    up = True
                elif event.key == pygame.K_DOWN:
                    left = right = up = False
                    down = True

        # pacgum logic
        for pacgum in self.pacgums:
            if pacgum.active and self.moulinette.pos == [pacgum.x, pacgum.y]:
                pacgum.active = False
                self.score += self.config.points_per_pacgum
        for pacgum in self.pacgums:
            pacgum.draw(self.screen)
        for super_pacgum in self.super_pacgums:
            if super_pacgum.active and self.moulinette.pos == [
                super_pacgum.x,
                super_pacgum.y,
            ]:
                super_pacgum.active = False
                self.score += self.config.points_per_super_pacgum
        for super_pacgum in self.super_pacgums:
            super_pacgum.draw(self.screen)

        # ghost collision
        if self.moulinette.pos in [
            self.studs[j].pos for j in range(len(self.studs))
        ]:
            self.lives -= 1
            self.moulinette.pos = [
                60 * (self.maze.width // 2) - 10,
                60 * (self.maze.height // 2) - 10,
            ]
            for i, stud in enumerate(self.studs):
                x, y = self.level["stud"][i]
                stud.pos = [x * 60 - 10, y * 60 - 10]
            for i, piscin in enumerate(self.piscins):
                x, y = self.level["piscin"][i]
                piscin.pos = [x * 60 - 10, y * 60 - 10]
        if self.moulinette.pos in [
            self.piscins[j].pos for j in range(len(self.piscins))
        ]:
            self.lives -= 1
            self.moulinette.pos = [
                60 * (self.maze.width // 2) - 10,
                60 * (self.maze.height // 2) - 10,
            ]
            for i, stud in enumerate(self.studs):
                x, y = self.level["stud"][i]
                stud.pos = [x * 60 - 10, y * 60 - 10]
            for i, piscin in enumerate(self.piscins):
                x, y = self.level["piscin"][i]
                piscin.pos = [x * 60 - 10, y * 60 - 10]

        # logique fuite a deplacer
        # if self.moulinette.pos[0] // 80 == 0:
        #     if self.moulinette.pos[1] // 80 == 0:
        #         for piscin in self.piscins:
        #             piscin.fuit = True

        # drawing
        image_piscin = image_piscin_norm
        image_stu = image_stu_norm
        for piscin in self.piscins:
            piscin.pos = piscin.mouve(self.moulinette.pos, self.maze)
        for stud in self.studs:
            stud.pos = stud.mouve(self.maze, self.moulinette.pos)
        self.moulinette.pos = self.moulinette.mouve(
            right, left, down, up, self.maze
        )
        self._draw_player()
        for stud in self.studs:
            self.screen.blit(
                image_stu,
                (
                    stud.pos[0] + 40 - moul_size / 2,
                    stud.pos[1] + 40 - moul_size / 2,
                ),
            )
        for piscin in self.piscins:
            self.screen.blit(
                image_piscin,
                (
                    piscin.pos[0] + 40 - moul_size / 2,
                    piscin.pos[1] + 40 - moul_size / 2,
                ),
            )
        self.animation_counter = (self.animation_counter + 1) % 12
        if self.lives <= 0 or self._second_remaining() <= 0:
            self.next_state = GameState.GAME_OVER
        if all([not pacgum.active for pacgum in self.pacgums]):
            if self.current_level == 9:
                self.next_state = GameState.VICTORY
            else:
                self.current_level += 1

    def draw(self) -> None:
        """Draw everything"""
        self.screen.fill(BLACK)
        self._draw_maze()
        self._draw_player()
        self._draw_hud()

    def _draw_player(self) -> None:
        """Draw the player"""
        counter = self.animation_counter // 4
        if self.moulinette.one_dir == "W" or self.moulinette.one_dir is None:
            self.screen.blit(
                moulinette_front_images[counter],
                (
                    self.moulinette.pos[0] + 40 - moul_size / 2,
                    self.moulinette.pos[1] + 40 - moul_size / 2,
                ),
            )
        elif self.moulinette.one_dir == "E":
            self.screen.blit(
                pygame.transform.flip(
                    moulinette_front_images[counter], True, False
                ),
                (
                    self.moulinette.pos[0] + 40 - moul_size / 2,
                    self.moulinette.pos[1] + 40 - moul_size / 2,
                ),
            )
        elif self.moulinette.one_dir == "N":
            self.screen.blit(
                moulinette_back_images[counter],
                (
                    self.moulinette.pos[0] + 40 - moul_size / 2,
                    self.moulinette.pos[1] + 40 - moul_size / 2,
                ),
            )
        elif self.moulinette.one_dir == "S":
            self.screen.blit(
                moulinette_front_images[counter],
                (
                    self.moulinette.pos[0] + 40 - moul_size / 2,
                    self.moulinette.pos[1] + 40 - moul_size / 2,
                ),
            )

    def _draw_maze(self) -> None:
        """Draw the maze"""
        for y in range(len(self.maze.themaze)):
            row = self.maze.themaze[y]
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
                    screen.blit(image_wall0, (x * 60, y * 60))
                elif w == 1:
                    screen.blit(image_wall1, (x * 60, y * 60))
                elif w == 10:
                    screen.blit(image_wall10, (x * 60, y * 60))
                elif w == 11:
                    screen.blit(image_wall11, (x * 60, y * 60))
                elif w == 100:
                    screen.blit(image_wall100, (x * 60, y * 60))
                elif w == 101:
                    screen.blit(image_wall101, (x * 60, y * 60))
                elif w == 110:
                    screen.blit(image_wall110, (x * 60, y * 60))
                elif w == 111:
                    screen.blit(image_wall111, (x * 60, y * 60))
                elif w == 1000:
                    screen.blit(image_wall1000, (x * 60, y * 60))
                elif w == 1100:
                    screen.blit(image_wall1100, (x * 60, y * 60))
                elif w == 1001:
                    screen.blit(image_wall1001, (x * 60, y * 60))
                elif w == 1011:
                    screen.blit(image_wall1011, (x * 60, y * 60))
                elif w == 1010:
                    screen.blit(image_wall1010, (x * 60, y * 60))
                elif w == 1110:
                    screen.blit(image_wall1110, (x * 60, y * 60))
                elif w == 1111:
                    screen.blit(image_wall1111, (x * 60, y * 60))
                elif w == 1101:
                    screen.blit(image_wall1101, (x * 60, y * 60))
                w = 0

    def _draw_hud(self) -> None:
        """Draw heads-up display"""
        level_text = self.font.render(
            f"Level: {self.current_level + 1}", True, WHITE
        )
        level_rect = level_text.get_rect(
            center=(SCREEN_WIDTH - level_text.get_width(), 100)
        )
        self.screen.blit(level_text, level_rect)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(
            center=(SCREEN_WIDTH - score_text.get_width(), 200)
        )
        self.screen.blit(score_text, score_rect)

        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        lives_rect = lives_text.get_rect(
            center=(SCREEN_WIDTH - lives_text.get_width(), 300)
        )
        self.screen.blit(lives_text, lives_rect)

        remaining = int(self._second_remaining())
        minutes = remaining // 60
        seconds = remaining % 60
        timer_text = self.font.render(
            f"Time: {minutes:02d}:{seconds:02d}", True, WHITE
        )
        timer_rect = timer_text.get_rect(
            center=(SCREEN_WIDTH - timer_text.get_width(), 400)
        )
        self.screen.blit(timer_text, timer_rect)


if __name__ == "__main__":
    parser = Parser("../config.json")
    config = parser.load()
    pygame.init()
    highscore_manager = HighscoreManager(config.highscore_filename)

    moul_size = 30
    taille = (SCREEN_WIDTH, SCREEN_HEIGHT)
    clok = pygame.time.Clock()
    pygame.display.set_caption("PAC-MAN")
    screen = pygame.display.set_mode(taille, pygame.RESIZABLE)
    ### LOADING THE ASSETS ###
    moulinette_front_images = []
    for i in range(0, 3):
        moulinette_front_images.append(
            pygame.transform.scale(
                pygame.image.load(
                    f"{BASE_DIR}/asset/sprite_cat{i}.png"
                ).convert_alpha(),
                (SPRITE_SIZE, SPRITE_SIZE),
            )
        )

    moulinette_back_images = []
    for i in range(3, 6):
        moulinette_back_images.append(
            pygame.transform.scale(
                pygame.image.load(
                    f"{BASE_DIR}/asset/sprite_cat{i}.png"
                ).convert_alpha(),
                (SPRITE_SIZE, SPRITE_SIZE),
            )
        )
    image_stu_norm = pygame.transform.scale(
        pygame.image.load("asset/dragon.png").convert_alpha(),
        (moul_size, moul_size),
    )
    image_stu_Fuit = pygame.transform.scale(
        pygame.image.load("asset/dragon.png").convert_alpha(),
        (moul_size, moul_size),
    )
    image_piscin_norm = pygame.image.load("asset/Eliot.png").convert_alpha()
    image_piscin_Fuit = pygame.image.load("asset/Eliot.png").convert_alpha()
    image_wall0 = pygame.transform.scale(
        pygame.image.load("asset/sprite_None.png").convert_alpha(), (60, 60)
    )
    image_wall1 = pygame.transform.scale(
        pygame.image.load("asset/sprite_N.png").convert_alpha(), (60, 60)
    )
    image_wall10 = pygame.transform.scale(
        pygame.image.load("asset/sprite_E.png").convert_alpha(), (60, 60)
    )
    image_wall11 = pygame.transform.scale(
        pygame.image.load("asset/sprite_NE.png").convert_alpha(), (60, 60)
    )
    image_wall100 = pygame.transform.scale(
        pygame.image.load("asset/sprite_S.png").convert_alpha(), (60, 60)
    )
    image_wall101 = pygame.transform.scale(
        pygame.image.load("asset/sprite_NS.png").convert_alpha(), (60, 60)
    )
    image_wall110 = pygame.transform.scale(
        pygame.image.load("asset/sprite_SE.png").convert_alpha(), (60, 60)
    )
    image_wall111 = pygame.transform.scale(
        pygame.image.load("asset/sprite_NSE.png").convert_alpha(), (60, 60)
    )
    image_wall1000 = pygame.transform.scale(
        pygame.image.load("asset/sprite_W.png").convert_alpha(), (60, 60)
    )
    image_wall1100 = pygame.transform.scale(
        pygame.image.load("asset/sprite_SW.png").convert_alpha(), (60, 60)
    )
    image_wall1010 = pygame.transform.scale(
        pygame.image.load("asset/sprite_EW.png").convert_alpha(), (60, 60)
    )
    image_wall1001 = pygame.transform.scale(
        pygame.image.load("asset/sprite_NW.png").convert_alpha(), (60, 60)
    )
    image_wall1011 = pygame.transform.scale(
        pygame.image.load("asset/sprite_NEW.png").convert_alpha(), (60, 60)
    )
    image_wall1110 = pygame.transform.scale(
        pygame.image.load("asset/sprite_SEW.png").convert_alpha(), (60, 60)
    )
    image_wall1111 = pygame.transform.scale(
        pygame.image.load("asset/sprite_NSEW.png").convert_alpha(), (60, 60)
    )
    image_wall1101 = pygame.transform.scale(
        pygame.image.load("asset/sprite_NSW.png").convert_alpha(), (60, 60)
    )
    image_pacgum = pygame.transform.scale(
        pygame.image.load("asset/sprite_pacgum.png").convert_alpha(), (30, 30)
    )
    image_TIG = pygame.transform.scale(
        pygame.image.load("asset/sprite_TIG.png").convert_alpha(), (30, 30)
    )

    #################################

    game = True
    # moulinette = classforthegame.Moulinette()
    views = {
        GameState.MAIN_MENU: MainMenuView(screen, config),
        GameState.PLAYING: GameplayView(screen, config),
        GameState.PAUSED: PauseView(screen, config),
        GameState.INSTRUCTIONS: InstructionsView(screen, config),
        GameState.HIGH_SCORES: HighscoreView(screen, config),
        GameState.GAME_OVER: GameOverView(screen, config, highscore_manager),
        GameState.VICTORY: VictoryView(screen, config, highscore_manager),
    }

    current_state = GameState.MAIN_MENU
    current_view = views[current_state]
    while game:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game = False

        current_view.draw()
        current_view.handle_event(events)

        next_state = current_view.get_next_state()
        if next_state:
            previous_state = current_state
            current_state = next_state
            current_view = views[current_state]
            if not (
                current_state == GameState.PLAYING
                and previous_state == GameState.PAUSED
            ):
                current_view.reset()
            current_view.next_state = None

        pygame.display.flip()
        clok.tick(FPS)
    pygame.quit()
    sys.exit()
