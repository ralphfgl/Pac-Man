import json
from parser import Parser
from enum import Enum
from macro import *
import sys
from abc import ABC, abstractmethod
import pygame
from entities import Player
from maze_wrapper import MazeLoader


class GameState(Enum):
    MAIN_MENU = 1
    PLAYING = 2
    PAUSED = 3
    HIGH_SCORES = 4
    GAME_OVER = 5
    INSTRUCTIONS = 6
    LEVEL_COMPLETE = 7


class View(ABC):
    """Base class for all views"""

    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.next_state = None
        self.font = pygame.font.Font(None, 48)

    @abstractmethod
    def handle_event(self, events):
        """Process input events"""
        pass

    @abstractmethod
    def draw(self):
        """Render the view"""
        pass

    def get_next_state(self):
        """Return the next game state to transition to"""
        return self.next_state

    def reset(self):
        """Reset view state when entering"""
        self.next_state = None


class MainMenuView(View):
    def __init__(self, screen, config):
        super().__init__(screen, config)
        self.selected_item = 0
        self.menu_items = [
            ("Play Game", GameState.PLAYING),
            ("View Highscores", GameState.HIGH_SCORES),
            ("Instructions", GameState.INSTRUCTIONS),
            ("Exit", None),
        ]

    def handle_event(self, events):
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

    def draw(self):
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
    def __init__(self, screen, config):
        super().__init__(screen, config)
        self.selected_item = 0
        self.menu_items = [
            ("Resume", GameState.PLAYING),
            ("Main Menu", GameState.MAIN_MENU),
        ]

    def handle_event(self, events):
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

    def draw(self):

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

    def __init__(self, screen, config):
        super().__init__(screen, config)

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.next_state = GameState.MAIN_MENU

    def draw(self):
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
            screen.blit(surface, surface_rect)
            y += self.font.get_linesize()
        back = self.font.render("Press Return to go back", True, GRAY)
        back_rect = back.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        )
        self.screen.blit(back, back_rect)


class HighscoreView(View):
    """Show leaderboard imported from highscore.json file"""

    def __init__(self, screen, config):
        super().__init__(screen, config)
        self.scores = []
        self.highscore_file = config.highscore_filename

    def reset(self):
        """Load scores when entering view"""

        super().reset()
        self.scores = self._load_scores()

    def _load_scores(self):
        """Load scores from JSON file"""

        try:
            with open(self.highscore_file, "r") as f:
                scores = json.load(f)
                scores.sort(key=lambda x: x["score"], reverse=True)
                return scores[:10]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.next_state = GameState.MAIN_MENU

    def draw(self):
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

    def __init__(self, screen, config):
        super().__init__(screen, config)
        self.score = 0

    def set_score(self, score):
        self.score = score

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.next_state = GameState.MAIN_MENU

    def draw(self):
        self.screen.fill(BLACK)
        game_over = self.font.render("GAME OVER", True, RED)
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(game_over, game_over_rect)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        self.screen.blit(score_text, score_rect)
        back = self.font.render("Press RETURN to continue", True, GRAY)
        back_rect = back.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(back, back_rect)


class GameplayView(View):
    """Main game view with maze"""

    def __init__(self, screen, config):
        super().__init__(screen, config)
        self.maze_loader = None
        self.maze = None
        self.player = None
        self.current_level = 0
        self.score = 0
        self.lives = 0
        self.offset_x = 0
        self.offset_y = 0
        self.animation_counter = 0

    def reset(self):
        """Start game when entering this view"""
        super().reset()
        self.current_level = 0
        self.score = 0
        self.lives = self.config.lives
        self._load_level()

    def _load_level(self):
        """Load a level from config"""
        self.maze_loader = MazeLoader(self.config.levels[self.current_level])
        self.maze = self.maze_loader.load()
        self.player = Player(
            self.maze.width * CELL_SIZE // 2, self.maze.height * CELL_SIZE // 2
        )
        self.offset_x = (SCREEN_WIDTH - self.maze.width * CELL_SIZE) // 2
        self.offset_y = (SCREEN_HEIGHT - self.maze.height * CELL_SIZE) // 2

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.next_state = GameState.PAUSED
                elif event.key == pygame.K_c:
                    self.current_level = (self.current_level + 1) % len(
                        self.config.levels
                    )
                    self._load_level()

    def update(self):
        """Game logic"""
        keys = pygame.key.get_pressed()

        self.player.move(keys, self.maze)
        self.direction = self.player.direction

        self.animation_counter = (self.animation_counter + 1) % 12
        if self.lives <= 0:
            self.next_state = GameState.GAME_OVER

    def draw(self):
        """Draw everything"""
        self.screen.fill(BLACK)
        self._draw_maze()
        self._draw_player()
        self._draw_hud()

    def _draw_maze(self):
        """Draw the maze grid"""
        for y, row in enumerate(self.maze.themaze):
            for x, cell in enumerate(row):
                rect = pygame.Rect(
                    self.offset_x + x * CELL_SIZE,
                    self.offset_y + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )

                if cell.static:
                    pygame.draw.rect(self.screen, BLUE, rect)
                else:
                    pygame.draw.rect(self.screen, BLACK, rect)

                if not cell.static:
                    if cell.walls & 0b1:
                        pygame.draw.line(
                            self.screen, BLUE, rect.topleft, rect.topright, 4
                        )
                    if (cell.walls >> 1) & 0b1:
                        pygame.draw.line(
                            self.screen,
                            BLUE,
                            rect.topright,
                            rect.bottomright,
                            4,
                        )
                    if (cell.walls >> 2) & 0b1:
                        pygame.draw.line(
                            self.screen,
                            BLUE,
                            rect.bottomleft,
                            rect.bottomright,
                            4,
                        )
                    if (cell.walls >> 3) & 0b1:
                        pygame.draw.line(
                            self.screen, BLUE, rect.topleft, rect.bottomleft, 4
                        )

    def _draw_player(self):
        """Draw the player"""
        player_x = self.offset_x + self.player.x - CELL_SIZE // 2
        player_y = self.offset_y + self.player.y - CELL_SIZE // 2
        counter = self.animation_counter // 4
        # print(f"Player images available: {len(player_images)}")
        if self.player.direction == "E":
            screen.blit(player_images[counter], (player_x, player_y))
        elif self.direction == "W":
            screen.blit(
                pygame.transform.flip(player_images[counter], True, False),
                (player_x, player_y),
            )
        elif self.player.direction == "N":
            screen.blit(
                pygame.transform.rotate(player_images[counter], 90),
                (player_x, player_y),
            )
        elif self.player.direction == "S":
            screen.blit(
                pygame.transform.rotate(player_images[counter], 270),
                (player_x, player_y),
            )

    def _draw_hud(self):
        """Draw heads-up display"""

        level_text = self.font.render(
            f"Level: {self.current_level + 1}", True, WHITE
        )
        self.screen.blit(level_text, (210, SCREEN_HEIGHT - 30))

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (360, SCREEN_HEIGHT - 30))

        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (510, SCREEN_HEIGHT - 30))


if __name__ == "__main__":
    parser = Parser("../config.json")
    config = parser.load()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("View Test")
    clock = pygame.time.Clock()

    views = {
        GameState.MAIN_MENU: MainMenuView(screen, config),
        GameState.PLAYING: GameplayView(screen, config),
        GameState.PAUSED: PauseView(screen, config),
        GameState.INSTRUCTIONS: InstructionsView(screen, config),
        GameState.HIGH_SCORES: HighscoreView(screen, config),
        GameState.GAME_OVER: GameOverView(screen, config),
    }

    current_state = GameState.MAIN_MENU
    current_view = views[current_state]

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        current_view.handle_event(events)

        if current_state == GameState.PLAYING:
            current_view.update()

        next_state = current_view.get_next_state()
        if next_state:
            print(f"Switching to: {next_state}")
            previous_state = current_state
            current_state = next_state
            current_view = views[current_state]
            if not (
                previous_state == GameState.PAUSED
                and current_state == GameState.PLAYING
            ):
                current_view.reset()
            if current_state == GameState.PLAYING:
                current_view.next_state = None

        current_view.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
