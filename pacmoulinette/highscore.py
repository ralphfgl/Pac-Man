import json
import sys
from pathlib import Path
from typing import Dict, List


class HighscoreManager:
    def __init__(self, filename: str) -> None:
        self.path = Path(filename)
        self.scores: List[Dict[str, int | str]] = []
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            return
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(
                f"[STDERR] - Failed to load highscores: {e}", file=sys.stderr
            )
            return

        if not isinstance(data, list):
            print(f"Invalid highscore file", file=sys.stderr)
            return

        self.scores = []
        for x in data:
            try:
                name = str(x["name"][:10].strip())
                score = max(0, int(x["score"]))
                self.scores.append(
                    {"name": name if name else "???", "score": score}
                )
            except Exception as e:
                continue
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:10]

    def add_score(self, name: str, score: int) -> bool:
        name = "".join(c for c in name[:10] if c.isalnum() or c == " ")
        if not name:
            name = "???"
        score = max(0, int(score))
        self.scores.append({"name": name, "score": score})
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:10]
        return self.save()

    def save(self) -> bool:
        try:
            with open(self.path, "w") as f:
                json.dump(self.scores, f, indent=2)
            return True
        except OSError as e:
            print(
                f"[STDERR] - Failed to save highscores: {e}", file=sys.stderr
            )
            return False
