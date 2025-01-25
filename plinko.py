import pygame
import sys
import json


class PlinkoGame:
    def __init__(self):
        pygame.init()
        # Load or set default settings
        self.load_settings()

        # Set up display
        self.screen = pygame.display.set_mode((self.settings['width'], self.settings['height']))
        pygame.display.set_caption("Plinko Game")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.GRAY = (128, 128, 128)

        # Game states
        self.MENU = "menu"
        self.PLAYING = "playing"
        self.SETTINGS = "settings"
        self.current_state = self.MENU

        # Font
        self.title_font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 36)

        # Main menu buttons
        self.update_button_positions()

        # Settings options
        self.window_sizes = ["800x600", "1024x768", "1280x720"]
        self.selected_size_index = self.window_sizes.index(f"{self.settings['width']}x{self.settings['height']}")

        # Clock
        self.clock = pygame.time.Clock()

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = {
                'width': 800,
                'height': 600,
                'dark_mode': False
            }
            self.save_settings()

    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)

    def update_button_positions(self):
        width = self.settings['width']
        self.buttons = {
            'start': pygame.Rect(width // 2 - 100, 250, 200, 50),
            'settings': pygame.Rect(width // 2 - 100, 320, 200, 50),
            'quit': pygame.Rect(width // 2 - 100, 390, 200, 50)
        }

        # Settings buttons
        self.settings_buttons = {
            'size_left': pygame.Rect(width // 2 - 150, 200, 30, 30),
            'size_right': pygame.Rect(width // 2 + 120, 200, 30, 30),
            'dark_mode': pygame.Rect(width // 2 - 100, 300, 200, 50),
            'back': pygame.Rect(width // 2 - 100, 500, 200, 50)
        }

    def draw_gradient_background(self):
        height = self.settings['height']
        width = self.settings['width']

        if self.settings['dark_mode']:
            for y in range(height):
                r = int(25 + (y / height) * 20)
                g = int(25 + (y / height) * 20)
                b = int(45 + (y / height) * 20)
                pygame.draw.line(self.screen, (r, g, b), (0, y), (width, y))
        else:
            for y in range(height):
                r = int(100 + (y / height) * 155)
                g = int(150 + (y / height) * 105)
                b = int(255 - (y / height) * 105)
                pygame.draw.line(self.screen, (r, g, b), (0, y), (width, y))

    def draw_menu(self):
        # Draw background
        self.draw_gradient_background()

        # Draw title
        title_color = self.WHITE if self.settings['dark_mode'] else self.BLACK
        title = self.title_font.render("PLINKO!", True, title_color)
        title_rect = title.get_rect(center=(self.settings['width'] // 2, 100))
        self.screen.blit(title, title_rect)

        # Draw buttons
        button_texts = {'start': 'Start Game', 'settings': 'Settings', 'quit': 'Quit'}
        for button_name, button_rect in self.buttons.items():
            # Draw button
            pygame.draw.rect(self.screen, self.BLUE, button_rect, border_radius=10)

            # Draw button text
            text = self.button_font.render(button_texts[button_name], True, self.WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

    def draw_settings(self):
        # Draw background
        self.draw_gradient_background()

        # Draw title
        title_color = self.WHITE if self.settings['dark_mode'] else self.BLACK
        title = self.title_font.render("Settings", True, title_color)
        title_rect = title.get_rect(center=(self.settings['width'] // 2, 100))
        self.screen.blit(title, title_rect)

        # Draw window size selector
        text_color = self.WHITE if self.settings['dark_mode'] else self.BLACK
        size_text = self.button_font.render("Window Size:", True, text_color)
        size_rect = size_text.get_rect(center=(self.settings['width'] // 2, 170))
        self.screen.blit(size_text, size_rect)

        # Draw arrows and current size
        pygame.draw.rect(self.screen, self.BLUE, self.settings_buttons['size_left'], border_radius=5)
        pygame.draw.rect(self.screen, self.BLUE, self.settings_buttons['size_right'], border_radius=5)

        # Draw arrow symbols
        left_arrow = self.button_font.render("<", True, self.WHITE)
        right_arrow = self.button_font.render(">", True, self.WHITE)
        self.screen.blit(left_arrow, self.settings_buttons['size_left'].move(10, 0))
        self.screen.blit(right_arrow, self.settings_buttons['size_right'].move(10, 0))

        # Draw current size
        size_text = self.button_font.render(self.window_sizes[self.selected_size_index], True, text_color)
        size_rect = size_text.get_rect(center=(self.settings['width'] // 2, 215))
        self.screen.blit(size_text, size_rect)

        # Draw dark mode toggle
        pygame.draw.rect(self.screen, self.BLUE, self.settings_buttons['dark_mode'], border_radius=10)
        dark_text = self.button_font.render(f"Dark Mode: {'On' if self.settings['dark_mode'] else 'Off'}",
                                            True, self.WHITE)
        dark_rect = dark_text.get_rect(center=self.settings_buttons['dark_mode'].center)
        self.screen.blit(dark_text, dark_rect)

        # Draw back button
        pygame.draw.rect(self.screen, self.BLUE, self.settings_buttons['back'], border_radius=10)
        back_text = self.button_font.render("Back", True, self.WHITE)
        back_rect = back_text.get_rect(center=self.settings_buttons['back'].center)
        self.screen.blit(back_text, back_rect)

    def apply_window_size(self, size_str):
        width, height = map(int, size_str.split('x'))
        self.settings['width'] = width
        self.settings['height'] = height
        self.screen = pygame.display.set_mode((width, height))
        self.update_button_positions()
        self.save_settings()

    def handle_click(self, pos):
        if self.current_state == self.MENU:
            for button_name, button_rect in self.buttons.items():
                if button_rect.collidepoint(pos):
                    if button_name == 'start':
                        print("Start button clicked - functionality removed as requested")
                    elif button_name == 'settings':
                        self.current_state = self.SETTINGS
                    elif button_name == 'quit':
                        pygame.quit()
                        sys.exit()

        elif self.current_state == self.SETTINGS:
            if self.settings_buttons['back'].collidepoint(pos):
                self.current_state = self.MENU
            elif self.settings_buttons['dark_mode'].collidepoint(pos):
                self.settings['dark_mode'] = not self.settings['dark_mode']
                self.save_settings()
            elif self.settings_buttons['size_left'].collidepoint(pos):
                self.selected_size_index = (self.selected_size_index - 1) % len(self.window_sizes)
                self.apply_window_size(self.window_sizes[self.selected_size_index])
            elif self.settings_buttons['size_right'].collidepoint(pos):
                self.selected_size_index = (self.selected_size_index + 1) % len(self.window_sizes)
                self.apply_window_size(self.window_sizes[self.selected_size_index])

    def run(self):
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.current_state == self.SETTINGS:
                            self.current_state = self.MENU
                        elif self.current_state == self.PLAYING:
                            self.current_state = self.MENU

            # Draw current state
            if self.current_state == self.MENU:
                self.draw_menu()
            elif self.current_state == self.SETTINGS:
                self.draw_settings()

            # Update display
            pygame.display.flip()

            # Control frame rate
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = PlinkoGame()
    game.run()