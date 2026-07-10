class ScoreEntryView(View):
    def __init__(self, screen, config, highscore_manager: HighscoreManager):
        super().__init__(screen, config)
        self.highscore_manager = highscore_manager
        self.score = 0
        self.entering_name = True
        self.name = ""
        self.saved = False

    def set_score(self, score: int) -> None:
        """Call this before switching to this view so it knows what to save."""
        self.score = score

    def reset(self):
        super().reset()
        self.entering_name = True
        self.name = ""
        self.saved = False

    def handle_event(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if self.entering_name:
                self._handle_name_input(event)
            else:
                if event.key == pygame.K_RETURN:
                    self.next_state = GameState.MAIN_MENU

    def _handle_name_input(self, event):
        if event.key == pygame.K_RETURN:
            clean_name = self.name.strip()
            if clean_name:
                self.highscore_manager.add_score(clean_name, self.score)
                self.saved = True
            self.entering_name = False
        elif event.key == pygame.K_BACKSPACE:
            self.name = self.name[:-1]
        else:
            char = event.unicode
            is_allowed = (
                bool(char)
                and char.isascii()
                and (char.isalnum() or char == " ")
            )
            if is_allowed and len(self.name) < self.MAX_NAME_LEN:
                self.name += char

    def draw(self):
        self.screen.fill(BLACK)
        title = self.font.render(self.title_text, True, self.title_color)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 130))
        self.screen.blit(title, title_rect)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 230))
        self.screen.blit(score_text, score_rect)

        if self.entering_name:
            self._draw_name_entry()
        else:
            self._draw_confirmation()

    def _draw_name_entry(self):
        prompt = self.font.render("Enter your name:", True, YELLOW)
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, 330))
        self.screen.blit(prompt, prompt_rect)

        name_display = self.font.render(self.name + "_", True, GREEN)
        name_rect = name_display.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(name_display, name_rect)

        hint = self.font.render(
            "Letters, numbers, spaces (max 10) - RETURN to confirm", True, GRAY
        )
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, 460))
        self.screen.blit(hint, hint_rect)

    def _draw_confirmation(self):
        msg = "Score saved to highscores!" if self.saved else "Score not saved"
        color = GREEN if self.saved else GRAY
        saved_text = self.font.render(msg, True, color)
        saved_rect = saved_text.get_rect(center=(SCREEN_WIDTH // 2, 360))
        self.screen.blit(saved_text, saved_rect)

        back = self.font.render("Press RETURN to continue", True, GRAY)
        back_rect = back.get_rect(center=(SCREEN_WIDTH // 2, 430))
        self.screen.blit(back, back_rect)
