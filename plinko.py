import pygame
import sys
import json
import math

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
        self.DARK_BLUE = (0, 70, 178)  # Darker blue for hover effect
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.GRAY = (128, 128, 128)
        self.GOLD = (255, 215, 0)

        # Game states
        self.MENU = "menu"
        self.PLAYING = "playing"
        self.SETTINGS = "settings"
        self.SHOP = "shop"
        self.current_state = self.MENU

        # Font
        self.title_font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 36)
        self.coin_font = pygame.font.Font(None, 40)

        # Money count
        self.coins = 0

        # Hover state
        self.hovered_button = None

        # Title animation
        self.title_points = []
        self.generate_title_arc()

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

    def generate_title_arc(self):
        # Generate points for title text to follow an arc
        self.title_points = []
        text = "PLINKO!"
        center_x = (self.settings['width'] // 2) - 10  # Subtract 10 pixels to move left
        base_y = 100
        arc_height = 30  # Height of the arc

        for i in range(len(text)):
            # Calculate position on arc
            angle = math.pi + (i - len(text) / 2) * 0.2
            x = center_x - (len(text) * 20) // 2 + i * 40
            y = base_y - math.sin(angle) * arc_height
            self.title_points.append((x, y, text[i]))

    def draw_money_counter(self):
        # Draw coin symbol
        coin_x = self.settings['width'] - 150
        coin_y = 20
        pygame.draw.circle(self.screen, self.GOLD, (coin_x, coin_y + 10), 15)
        pygame.draw.circle(self.screen, (200, 170, 0), (coin_x, coin_y + 10), 12)

        # Draw count
        count_text = self.coin_font.render(str(self.coins), True,
                                           self.WHITE if self.settings['dark_mode'] else self.BLACK)
        count_rect = count_text.get_rect(midleft=(coin_x + 20, coin_y + 10))
        self.screen.blit(count_text, count_rect)

        # Draw shop button (+)
        shop_button = pygame.Rect(self.settings['width'] - 40, coin_y, 30, 30)
        pygame.draw.rect(self.screen, self.BLUE if self.hovered_button != 'shop' else self.DARK_BLUE,
                         shop_button, border_radius=5)
        plus_text = self.button_font.render("+", True, self.WHITE)
        plus_rect = plus_text.get_rect(center=shop_button.center)
        self.screen.blit(plus_text, plus_rect)

        # Store shop button for click detection
        self.shop_button = shop_button

    def draw_menu(self):
        # Draw background
        self.draw_gradient_background()

        # Draw arched title
        title_color = self.WHITE if self.settings['dark_mode'] else self.BLACK
        for x, y, char in self.title_points:
            text = self.title_font.render(char, True, title_color)
            rect = text.get_rect(center=(x, y))
            self.screen.blit(text, rect)

        # Draw buttons
        button_texts = {'start': 'Start Game', 'settings': 'Settings', 'quit': 'Quit'}
        for button_name, button_rect in self.buttons.items():
            # Determine button color based on hover state
            color = self.DARK_BLUE if self.hovered_button == button_name else self.BLUE

            # Draw button
            pygame.draw.rect(self.screen, color, button_rect, border_radius=10)

            # Draw button text
            text = self.button_font.render(button_texts[button_name], True, self.WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

        # Draw money counter
        self.draw_money_counter()

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
        for button_name, button_rect in self.settings_buttons.items():
            color = self.DARK_BLUE if self.hovered_button == button_name else self.BLUE
            pygame.draw.rect(self.screen, color, button_rect,
                             border_radius=5 if 'size' in button_name else 10)
        # Draw dark mode toggle
        pygame.draw.rect(self.screen, self.BLUE, self.settings_buttons['dark_mode'], border_radius=10)
        dark_text = self.button_font.render(f"Dark Mode: {'On' if self.settings['dark_mode'] else 'Off'}",
                                            True, self.WHITE)
        dark_rect = dark_text.get_rect(center=self.settings_buttons['dark_mode'].center)
        self.screen.blit(dark_text, dark_rect)

        # Draw back button
        pygame.draw.rect(self.screen,
                         self.DARK_BLUE if self.hovered_button == 'back' else self.BLUE,
                         self.settings_buttons['back'], border_radius=10)
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

    def update_hover_state(self, pos):
        # Reset hover state
        self.hovered_button = None

        # Check main menu buttons
        if self.current_state == self.MENU:
            for button_name, button_rect in self.buttons.items():
                if button_rect.collidepoint(pos):
                    self.hovered_button = button_name
                    break

            # Check shop button
            if hasattr(self, 'shop_button') and self.shop_button.collidepoint(pos):
                self.hovered_button = 'shop'

        # Check settings buttons
        elif self.current_state == self.SETTINGS:
            for button_name, button_rect in self.settings_buttons.items():
                if button_rect.collidepoint(pos):
                    self.hovered_button = button_name
                    break

        # Check shop buttons
        elif self.current_state == self.SHOP:
            if self.settings_buttons['back'].collidepoint(pos):
                self.hovered_button = 'back'

    def draw_shop(self):
        # Draw background
        self.draw_gradient_background()

        # Draw title
        title_color = self.WHITE if self.settings['dark_mode'] else self.BLACK
        title = self.title_font.render("Shop", True, title_color)
        title_rect = title.get_rect(center=(self.settings['width'] // 2, 100))
        self.screen.blit(title, title_rect)

        # Draw back button
        pygame.draw.rect(self.screen,
                         self.DARK_BLUE if self.hovered_button == 'back' else self.BLUE,
                         self.settings_buttons['back'], border_radius=10)
        back_text = self.button_font.render("Back", True, self.WHITE)
        back_rect = back_text.get_rect(center=self.settings_buttons['back'].center)
        self.screen.blit(back_text, back_rect)

        # Draw money counter
        self.draw_money_counter()

    def handle_click(self, pos):
        if self.current_state == self.MENU:
            # Check shop button
            if hasattr(self, 'shop_button') and self.shop_button.collidepoint(pos):
                self.current_state = self.SHOP
                return

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

        elif self.current_state == self.SHOP:
            if self.settings_buttons['back'].collidepoint(pos):
                self.current_state = self.MENU

    def run(self):
        running = True
        while running:
            # Get mouse position for hover effects
            mouse_pos = pygame.mouse.get_pos()
            self.update_hover_state(mouse_pos)  # Add this line for hover effects

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.current_state in [self.SETTINGS, self.PLAYING, self.SHOP]:  # Add SHOP here
                            self.current_state = self.MENU

            # Draw current state
            if self.current_state == self.MENU:
                self.draw_menu()
            elif self.current_state == self.SETTINGS:
                self.draw_settings()
            elif self.current_state == self.SHOP:  # Add this condition
                self.draw_shop()

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = PlinkoGame()
    game.run()