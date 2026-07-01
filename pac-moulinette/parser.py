import json
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List, Any
import sys


class LvlConfig(BaseModel):
    """Level config

    Attributes:
            width, height: dimension of the generated maze
            seed: optional seed to generate the maze
    """

    width: int = Field(default=20, ge=10, le=50)
    height: int = Field(default=20, ge=10, le=50)
    seed: Optional[int] = Field(default=None)


class Config(BaseModel):
    """Game config

    Attributes:
    """

    levels: List[LvlConfig] = Field(
        default_factory=lambda: [LvlConfig() for _ in range(10)], min_length=10
    )
    highscore_filename: str = Field(default="highscore.json")
    lives: int = Field(default=3, ge=1, le=999)
    pacgum: int = Field(default=42, ge=1, le=999)
    points_per_pacgum: int = Field(default=10, ge=1, le=999)
    points_per_super_pacgum: int = Field(default=50, ge=1, le=999)
    points_per_ghost: int = Field(default=200, ge=1, le=999)
    seed: int = Field(default=42)
    level_max_time: int = Field(default=90, ge=30)


class Parser:
    """Load and validate game config from a JSON file"""

    def __init__(self, path: str) -> None:
        """Store the path to the json file"""

        self.path = Path(path)

    def _remove_comments(self, text: str) -> str:
        """Remove # comment lines and inline comments from JSON
        Args:
            text: Raw file content

        Returns:
            Clean JSON string with comments removed
        """
        lines = []
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            lines.append(line)
        return "\n".join(lines)

    def load(self) -> Config:
        """Load the config file"""

        if not self.path.is_file():
            print("[STDERR] - Config is not a file", file=sys.stderr)
            sys.exit(1)
        if not self.path.suffix == ".json":
            print("[STDERR] - Config has the wrong format", file=sys.stderr)
            sys.exit(1)
        try:
            with open(self.path, "r") as f:
                raw = f.read()
        except OSError as e:
            print(
                f"[STDERR] - Failed to read the file: {self.path}, error: {e}",
                file=sys.stderr,
            )
            sys.exit(1)

        clean = self._remove_comments(raw)
        try:
            data: dict[str, Any] = json.loads(clean)
        except json.JSONDecodeError as e:
            print(
                f"[STEDERR] - Config file '{self.path}' is not valid JSON, \
error: {e}",
                file=sys.stderr,
            )
            sys.exit(1)

        return self.validate(data)

    def validate(self, data: dict[str, Any]) -> Config:
        """Validate config data"""
        try:
            config_keys = set(Config.model_fields.keys())
            provided_keys = set(data.keys())
            missing_keys = config_keys - provided_keys
            unknown_keys = provided_keys - config_keys

            for missing_key in missing_keys:
                default_value = getattr(Config(), missing_key)
                print(
                    f"[INFO] - Key '{missing_key}' is missing, using default\
 value: {default_value}",
                    file=sys.stderr,
                )
            for unknown_key in unknown_keys:
                print(f"[INFO] {unknown_key} was ignored")
            return Config.model_validate(data)
        except ValidationError as e:
            defaults = Config()
            data_copy = data.copy()
            for err in e.errors():
                key = str(err["loc"][0])
                data_copy[key] = getattr(defaults, key)
                print(
                    f"[STDERR] - Invalid config field {key}, using default \
value: {getattr(defaults, key)}",
                    file=sys.stderr,
                )
        return Config.model_validate(data_copy)


if __name__ == "__main__":
    print("Testing JSON parsing")
    parser = Parser("../config.json")
    config = parser.load()
    print("\nDisplay settings")
    print(f" Lives: {config.lives}")
    print(f" Pacgum: {config.pacgum}")
    print(f" Max lvl time: {config.level_max_time}")
    print(f" Seed: {config.seed}")
    print(f" Highscore file: {config.highscore_filename}")

    print("\nPoints")
    print(
        f" Pacgum, super pacgum, ghost: {
            config.points_per_pacgum
            }, {config.points_per_super_pacgum}, {config.points_per_ghost}"
    )

    print("\nLevels")
    for i, level in enumerate(config.levels, start=1):
        print(f" Level {i}: {level.width}x{level.height}")
