*This activity has been created as part of the 42 curriculum by <login1>[, <login2>[, <login3>]].*

# Pac-Moulinette

## Description

The aim of the project was to build a Pac-Man clone. The
goal of the activity is twofold: implement a classic arcade game loop (player
movement, ghost AI, collisions, lives, scoring) on top of a maze that is
**procedurally generated** by the assigned maze-generation package, rather
than hand-drawn.

The player controls Moulinette through a randomly generated maze, collects
pac-gum, and avoids (or is chased by) ghosts. Each level has its own size,
and ghost composition. Losing all lives or running out of time
ends the game; the player can then save their score to a persistent
top-10 leaderboard.

## Instructions

### Requirements

- Python 3.10+
- [pygame](https://www.pygame.org/)
- [pydantic](https://docs.pydantic.dev/)
- The assigned `mazegenerator` ("A-Maze-ing") package

Install dependencies with:

```bash
pip install -r requirements.txt
```

### Running the game

From the `pac-moulinette/` directory:

```bash
python pac-man.py
```

The game expects a `config.json` 
See the [Configuration](#configuration) section below for its structure.

### Controls

| Key           | Action                                   |
|---------------|-------------------------------------------|
| Arrow keys    | Move Moulinette                           |
| `P`           | Pause / resume                            |
| `C`           | Cheat: skip to the next level (dev/testing) |
| `ESC`         | Quit                                       |
| Letters/digits/space | Type your name on the game-over / victory screen |
| `Enter`       | Confirm menu selection / confirm name entry / continue |
| `Backspace`   | Delete last character when entering a name |

## Configuration

All tunable game parameters live in `config.json`, validated at startup
against a `pydantic` schema (`parser.py`). Lines starting with `#` are
stripped before parsing, so the file can be commented.

```jsonc
{
  # global settings
  "highscore_filename": "highscore.json",
  "lives": 3,
  "pacgum": 42,
  "points_per_pacgum": 10,
  "points_per_super_pacgum": 50,
  "points_per_ghost": 200,
  "seed": 42,
  "level_max_time": 90,

  # one entry per level, minimum 10 entries required
  "levels": [
    { "width": 20, "height": 20, "seed": 42 },
    { "width": 24, "height": 20 }
  ]
}
```

| Field                     | Default | Description                                              |
|---------------------------|---------|------------------------------------------------------------|
| `highscore_filename`      | `"highscore.json"` | Path to the top-10 leaderboard file                |
| `lives`                   | `3`     | Starting number of lives (1–999)                          |
| `pacgum`                  | `42`    | Amount of pac-gum to place in a level (1–999)              |
| `points_per_pacgum`       | `10`    | Points for a regular pac-gum (1–999)                       |
| `points_per_super_pacgum` | `50`    | Points for a super pac-gum (1–999)                          |
| `points_per_ghost`        | `200`   | Points for eating a ghost (1–999)                          |
| `seed`                    | `42`    | Reserved global RNG seed                                    |
| `level_max_time`          | `90`    | Seconds allowed to clear a level before it's game over (≥30) |
| `levels`                  | 10 default levels | List of per-level configs (`width`, `height`, `seed`) |

Per level: `width` (12–40), `height` (12–24), `seed` (optional int — see
[Maze Generation](#maze-generation) for how/when it's used).

**Validation behavior:** if a key is missing, the default value is used and
an `[INFO]` message is printed. If a key has an invalid value (wrong type,
out of range), that field falls back to its default with a `[STDERR]`
message; unknown keys are ignored with a message rather than causing a
crash. This keeps a slightly malformed config file from blocking the whole
game.

**Ghost composition is intentionally *not* in `config.json`.** It's
hardcoded in `views.py` as  a list of
`{"stud": <count>, "piscineux": <count>}` dicts, one per level

## Highscore

Highscores are stored as a flat JSON list of `{"name": str, "score": int}`
objects, sorted descending, capped at the top 10 entries.

- **Loaded once, at game start.** A single `HighscoreManager` instance
  (`highscore.py`) reads the file when the game boots and is then shared by
  every view that touches scores (`GameOverView`,
  `VictoryView`), so there's one source of truth instead of each screen
  re-reading the file independently.
- **Saved immediately on every new entry**, not just on quit — `add_score()`
  re-sorts, truncates to 10, and rewrites the file synchronously. This
  trades a small amount of I/O for not losing a score if the game crashes
  or is force-closed right after game over.
- We picked a plain top-10 JSON file (over, say, a database) because the
  leaderboard is small, local, and human-inspectable — good enough for the
  scope of this project without adding a dependency.

## Maze Generation

Mazes are generated by the assigned **A-Maze-ing** package
(`mazegenerator.MazeGenerator`), which — given a `(width, height)` and a
seed — produces a grid where each cell is an integer bitmask describing
which of its four walls are open (`N=1, E=2, S=4, W=8`; `15` marks a cell
fully enclosed on all sides).

`maze_wrapper.py` is a thin adapter between our config and that package:

- `MazeLoader.load()` calls `MazeGenerator` with the level's `width`/`height`
  and wraps each returned cell into a `Cellule` (`walls`, and a `static`
  flag for fully-closed cells), assembled into a `Maze` object that the
  rest of the game (rendering, gate/collision checks in
  `classforthegame.py`) consumes.
- **Seeding is deliberately limited to the first level.** `load()` takes an
  `apply_seed` flag; `GameplayView` only passes `apply_seed=True` for level
  index 0. If that level's config has a `seed`, its maze is reproducible
  run to run (useful for a consistent opening/tutorial experience and for
  debugging); every other level ignores its `seed` field (even if one is
  set) and always calls `MazeGenerator` with a fresh random seed, so replay
  variety is preserved past the first level.
- Wall bitmasks are also used directly by the renderer (`_draw_maze` in
  `views.py`) to pick the correct wall sprite for each of the 16 possible
  configurations, and by `Perssonage.open_gate()` (`classforthegame.py`) to
  decide whether an entity can move through a given side of a cell.

## Implementation

- **Language/runtime:** Python 3, `pygame` for windowing/input/rendering
  and the frame loop, `pydantic` for config schema validation.
- **State machine:** the whole game is a `GameState` enum with one `View`
  subclass per state (menu, gameplay, pause, instructions, highscores,
  game over, victory). The main loop in `views.py` asks the current view to
  `draw()`, `handle_event()`, then checks `get_next_state()` to decide
  whether to swap views (and whether to `reset()` the new one — pausing is
  special-cased so gameplay state isn't reset on resume).
- **Entities** (`classforthegame.py`): a shared `Perssonage` base class
  holds position/stats; `Moulinette` (player), `Stud`, and `Piscineux`
  (ghosts) each implement their own movement/gate logic. Ghosts are
  instantiated generically through `GHOST_REGISTRY` so gameplay code never
  needs to special-case a specific ghost class by name, only by type where
  behavior genuinely differs (movement signature, chase vs. flee).
- **Level timer:** `GameplayView` stamps `level_start_ticks` on level load
  and compares elapsed time to `config.level_max_time` every frame. Pausing
  doesn't leak time off the clock — the pause start tick is recorded and
  the elapsed pause duration is added back to `level_start_ticks` the
  moment gameplay resumes.
- **Name entry / highscores:** see [Highscore](#highscore) above.

## General Software Architecture

```
config.json
    │
    ▼
parser.py            Config / LvlConfig (pydantic models) + Parser
    │                 (load, strip comments, validate, fall back to
    │                  defaults on bad/missing/unknown fields)
    ▼
maze_wrapper.py       MazeLoader — bridges LvlConfig -> mazegenerator
    │                 (A-Maze-ing) -> Cellule / Maze
    ▼
views.py              GameState (enum) + View (ABC) and its subclasses:
    │                   MainMenuView, PauseView, InstructionsView,
    │                   HighscoreView, ScoreEntryView
    │                     ├── GameOverView
    │                     └── VictoryView
    │                   GameplayView  (owns: Maze, Moulinette, ghost list,
    │                                  level timer, score/lives, and
    │                                  references to GameOverView /
    │                                  VictoryView to push the final score)
    │                   main loop (state machine driver, asset loading)
    ▼
classforthegame.py    Perssonage (base) -> Moulinette, Stud, Piscineux
                       (position, movement, gate/collision logic)

highscore.py           HighscoreManager — load/save/query top-10 scores,
                        shared by HighscoreView, GameOverView, VictoryView
```

Key relationships:

- `views.py` is the composition root: it builds one `HighscoreManager`,
  wires it into every view that needs it, builds all `View` instances into
  a `GameState -> View` dict, and wires `GameplayView.game_over_view` /
  `.victory_view` so gameplay can push the final score before switching
  state.
- `GameplayView` composes a `Maze` (via `MazeLoader`), one `Moulinette`,
  and a list of ghost objects (built by `GHOST_REGISTRY` +
  `LEVEL_GHOSTS`) — it doesn't know or care about `mazegenerator` directly,
  only about the `Maze`/`Cellule` abstraction `maze_wrapper.py` exposes.
- `ScoreEntryView` is the only class both `GameOverView` and `VictoryView`
  inherit from, so the name-entry/validation/highscore-saving logic exists
  in exactly one place.

## Project Management


Project management artifacts (planning board, meeting notes, task
breakdown) are available in project_management/ directory

## Resources

- [pygame documentation](https://www.pygame.org/docs/) — window, event
  loop, surfaces/blitting, input handling.
- [pydantic documentation](https://docs.pydantic.dev/) — schema
  validation, `Field` constraints, `field_validator`.
- The 42 "A-Maze-ing" subject and the `mazegenerator` package
  documentation/source for the maze generation algorithm and its
  wall-bitmask output format.
- Classic Pac-Man ghost-AI writeups (e.g. articles describing chase/scatter
  behavior) as background for designing `Stud`/`Piscineux` movement.

**AI usage:** 
AI was used for :
- Learning about the pygame lib.
- Learning about project management technique
- Drafting this README.
