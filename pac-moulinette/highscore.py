import json
import sys
from pathlib import Path
from typing import Dict, List


class HighscoreManager:
    """Keep in memory the highscore dict."""

    def __init__(self, filename: str) -> None:
        self.path = Path(filename)
        self.scores: List[Dict]
