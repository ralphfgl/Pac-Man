import json
from parser import Parser
from enum import Enum
from macro import *
import sys
from abc import ABC, abstractmethod
import pygame
import classforthegame
from maze_wrapper import MazeLoader
import asset


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
            self.screen.blit(surface, surface_rect)
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
        self.animation_counter = 0

    def reset(self):
        """Start game when entering this view"""
        super().reset()
        self.current_level = 0
        self.score = 0
        self.lives = self.config.lives
        self._load_level()
        # self.i = 0

    def _load_level(self):
        """Load a level from config"""
        self.maze_loader = MazeLoader(self.config.levels[self.current_level])
        self.maze = self.maze_loader.load()
        self.moulinette = classforthegame.Moulinette()
        self.stu = classforthegame.Stud()
        self.piscin = classforthegame.Piscineux()

    def handle_event(self, events):
        right = left = down = up = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.next_state = GameState.PAUSED
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
        screen.blit(image_s_pac_gum, (30, 30))
        if self.moulinette.pos == self.stu.pos:
            self.lives -= 1
        if self.moulinette.pos == self.piscin.pos:
            self.lives -= 1
        if self.moulinette.pos[0] // 80 == 0:
            if self.moulinette.pos[1] // 80 == 0:
                self.piscin.fuit = True
        image_piscin = image_piscin_norm
        image_stu = image_stu_norm
        self.piscin.pos = self.piscin.mouve(self.moulinette.pos, self.maze)
        self.stu.pos = self.stu.mouve(self.maze, self.moulinette.pos)
        self.moulinette.pos = self.moulinette.mouve(
            right, left, down, up, self.maze
        )
        self._draw_player()
        self.screen.blit(
            image_stu,
            (
                self.stu.pos[0] + 40 - moul_size / 2,
                self.stu.pos[1] + 40 - moul_size / 2,
            ),
        )
        self.screen.blit(
            image_piscin,
            (
                self.piscin.pos[0] + 40 - moul_size / 2,
                self.piscin.pos[1] + 40 - moul_size / 2,
            ),
        )
        self.animation_counter = (self.animation_counter + 1) % 12
        if self.lives <= 0:
            self.next_state = GameState.GAME_OVER

    def draw(self):
        """Draw everything"""
        self.screen.fill(BLACK)
        self._draw_maze()
        self._draw_player()
        self._draw_hud()

    def _draw_player(self):
        """Draw the player"""
        counter = self.animation_counter // 4
        if self.moulinette.one_dir == "E" or self.moulinette.one_dir is None:
            self.screen.blit(
                moulinette_front_images[counter],
                (
                    self.moulinette.pos[0] + 40 - moul_size / 2,
                    self.moulinette.pos[1] + 40 - moul_size / 2,
                ),
            )
        elif self.moulinette.one_dir == "W":
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
                pygame.transform.rotate(moulinette_front_images[counter], 90),
                (
                    self.moulinette.pos[0] + 40 - moul_size / 2,
                    self.moulinette.pos[1] + 40 - moul_size / 2,
                ),
            )
        elif self.moulinette.one_dir == "S":
            self.screen.blit(
                pygame.transform.rotate(moulinette_front_images[counter], 270),
                (
                    self.moulinette.pos[0] + 40 - moul_size / 2,
                    self.moulinette.pos[1] + 40 - moul_size / 2,
                ),
            )

    def _draw_maze(self):
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

    def _draw_hud(self):
        """Draw heads-up display"""
        level_text = self.font.render(
            f"Level: {self.current_level + 1}", True, WHITE
        )
        self.screen.blit(level_text, (210, SCREEN_HEIGHT - 30))

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (360, SCREEN_HEIGHT - 30))

        lives_text = self.font.render(f"Lives: {self.lives}", True, RED)
        self.screen.blit(lives_text, (510, SCREEN_HEIGHT - 30))


if __name__ == "__main__":
    parser = Parser("../config.json")
    config = parser.load()
    pygame.init()

    moul_size = 40
    taille = (SCREEN_WIDTH, SCREEN_HEIGHT)
    clok = pygame.time.Clock()
    pygame.display.set_caption(asset.DRAGON_PATH)
    screen = pygame.display.set_mode(taille, pygame.RESIZABLE)
    # image_moulinette = pygame.transform.scale(
    #     pygame.image.load(asset.KNIGHT_PATH).convert_alpha(),
    #     (moul_size, moul_size),
    # )
    image_stu_norm = pygame.transform.scale(
        pygame.image.load(asset.DRAGON_PATH).convert_alpha(),
        (moul_size, moul_size),
    )
    image_stu_Fuit = pygame.transform.scale(
        pygame.image.load(asset.DRAGON_PATH).convert_alpha(),
        (moul_size, moul_size),
    )
    image_piscin_norm = pygame.image.load(asset.ELIOT_PATH).convert_alpha()
    image_piscin_Fuit = pygame.image.load(asset.ELIOT_PATH).convert_alpha()
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
    image_s_pac_gum = pygame.image.load(asset.PAC_GUM).convert_alpha()
    game = True
    # moulinette = classforthegame.Moulinette()
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
