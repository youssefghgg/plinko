import pygame
import sys
import math


class PlinkoGame:
    def __init__(self):
        pygame.init()
        # Set up display
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Plinko Game")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Game states
        self.MENU = "menu"
        self.PLAYING = "playing"
        self.SETTINGS = "settings"
        self.current_state = self.MENU

        # Font
        self.title_font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 36)

        # Buttons
        self.buttons = {
            'start': pygame.Rect(300, 250, 200, 50),
            'settings': pygame.Rect(300, 320, 200, 50),
            'quit': pygame.Rect(300, 390, 200, 50)
        }

        # Game objects
        self.pegs = []
        self.ball = None
        self.setup_pegs()

        # Clock
        self.clock = pygame.time.Clock()

    def setup_pegs(self):
        # Create a triangle pattern of pegs
        rows = 8
        spacing = 50
        for row in range(rows):
            for col in range(row + 1):
                x = self.width // 2 - (row * spacing // 2) + (col * spacing)
                y = 150 + (row * spacing)
                self.pegs.append((x, y))

    def draw_gradient_background(self):
        for y in range(self.height):
            r = int(100 + (y / self.height) * 155)
            g = int(150 + (y / self.height) * 105)
            b = int(255 - (y / self.height) * 105)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))

    def draw_menu(self):
        # Draw background
        self.draw_gradient_background()

        # Draw title
        title = self.title_font.render("PLINKO!", True, self.BLACK)
        title_rect = title.get_rect(center=(self.width // 2, 100))
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

    def draw_game(self):
        # Draw background
        self.draw_gradient_background()

        # Draw pegs
        for peg in self.pegs:
            pygame.draw.circle(self.screen, self.BLACK, peg, 5)

        # Draw ball if it exists
        if self.ball:
            pygame.draw.circle(self.screen, self.RED,
                               (int(self.ball['x']), int(self.ball['y'])), 10)

    def draw_settings(self):
        # Draw background
        self.draw_gradient_background()

        # Draw title
        title = self.title_font.render("Settings", True, self.BLACK)
        title_rect = title.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title, title_rect)

        # Add back button
        back_button = pygame.Rect(300, 500, 200, 50)
        pygame.draw.rect(self.screen, self.BLUE, back_button, border_radius=10)
        back_text = self.button_font.render("Back", True, self.WHITE)
        back_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, back_rect)

    def handle_click(self, pos):
        if self.current_state == self.MENU:
            for button_name, button_rect in self.buttons.items():
                if button_rect.collidepoint(pos):
                    if button_name == 'start':
                        self.current_state = self.PLAYING
                    elif button_name == 'settings':
                        self.current_state = self.SETTINGS
                    elif button_name == 'quit':
                        pygame.quit()
                        sys.exit()

        elif self.current_state == self.PLAYING:
            # Drop a new ball
            if pos[1] < 150:  # Only if clicking above the pegs
                self.ball = {
                    'x': pos[0],
                    'y': pos[1],
                    'dy': 0,  # Vertical velocity
                    'dx': 0  # Horizontal velocity
                }

        elif self.current_state == self.SETTINGS:
            back_button = pygame.Rect(300, 500, 200, 50)
            if back_button.collidepoint(pos):
                self.current_state = self.MENU

    def update_ball(self):
        if self.ball:
            # Apply gravity
            self.ball['dy'] += 0.5

            # Update position
            self.ball['x'] += self.ball['dx']
            self.ball['y'] += self.ball['dy']

            # Check for collisions with pegs
            for peg in self.pegs:
                dx = self.ball['x'] - peg[0]
                dy = self.ball['y'] - peg[1]
                distance = math.sqrt(dx * dx + dy * dy)

                if distance < 15:  # Ball + peg radius
                    # Bounce off peg
                    angle = math.atan2(dy, dx)
                    self.ball['dx'] = math.cos(angle) * 5
                    self.ball['dy'] = math.sin(angle) * 5

            # Remove ball if it goes off screen
            if self.ball['y'] > self.height:
                self.ball = None

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
                        self.current_state = self.MENU

            # Clear screen
            self.screen.fill(self.WHITE)

            # Update and draw based on current state
            if self.current_state == self.MENU:
                self.draw_menu()
            elif self.current_state == self.PLAYING:
                self.update_ball()
                self.draw_game()
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