import pygame
import sys
import json
import math
import random

class Ball:
    def __init__(self, x, y, radius, color, bet_amount):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dx = 0
        self.dy = 0
        self.bet_amount = bet_amount  # Store bet amount with the ball
        self.active = True


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

        # Multiplier values from left to right
        self.multipliers = [110, 41, 10, 5, 3, 2, 1.5, 1, 0.5, 0.3, 0.5, 1, 1.5, 2, 3, 5, 10, 41, 110]

        # Colors for multipliers (from highest to lowest)
        self.multiplier_colors = [
            (80, 0, 0),  # Oxblood (110x)
            (139, 0, 0),  # Dark Red (41x)
            (178, 34, 34),  # Firebrick Red (10x)
            (220, 20, 60),  # Crimson (5x)
            (255, 0, 0),  # Red (3x)
            (255, 69, 0),  # Red-Orange (2x)
            (255, 99, 71),  # Tomato (1.5x)
            (255, 127, 80),  # Coral (1x)
            (255, 165, 0),  # Orange (0.5x)
            (255, 215, 0),  # Yellow (0.3x)
        ]

        # Set initial coins
        self.coins = 100
        # Ball properties
        self.balls = []  # List to store active balls
        self.ball_radius = 10  # Double the size of pins
        self.ball_speed = 0.5  # Vertical speed of the ball
        self.ball_color = self.GOLD
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
        # Add pin positions list
        self.pin_positions = []

        # Dashboard properties
        self.dashboard_width = 200
        self.dashboard_extended = False
        self.dashboard_x = -self.dashboard_width
        self.amount = 0.0
        self.risks = ["Easy (2%)", "Medium (15%)", "Hard (40%)"]
        self.selected_risk = 0
        self.is_dropdown_open = False
        self.ball_radius = 9.5
        self.dashboard_buttons = {}
        self.hovered_dashboard = None  # For hover effects

        # Clock
        self.clock = pygame.time.Clock()

    def drop_ball(self):
        risk_values = [0.02, 0.15, 0.40]  # Easy, Medium, Hard
        bet_amount = self.amount  # Use the full amount selected

        if bet_amount <= self.coins and bet_amount > 0:
            # Calculate the starting position
            first_pin_x = (self.settings['width'] - ((2) * 30)) // 2
            ball_start_x = first_pin_x + 30
            ball_start_y = 70

            # Create new ball with bet amount
            new_ball = Ball(ball_start_x, ball_start_y, self.ball_radius, self.ball_color, bet_amount)
            new_ball.dy = 2  # Initial drop speed increased
            self.balls.append(new_ball)

            # Deduct bet amount (rounded)
            self.coins = round(self.coins - bet_amount, 2)

    def round_coins(self, value):
        """Helper method to round coin values to 2 decimal places."""
        return round(value, 2)

    def update_balls(self):
        gravity = 0.5
        bounce_damping = 0.65  # Slightly increased from 0.6 for more bounce
        pin_radius = 5

        # Calculate invisible wall positions based on pin layout
        left_wall_x = (self.settings['width'] - ((16) * 30)) // 2 - 20
        right_wall_x = self.settings['width'] - left_wall_x

        # Calculate center position for bias
        center_x = self.settings['width'] / 2

        for ball in self.balls[:]:
            if not ball.active:
                continue

            # Update velocity and position
            ball.dy += gravity
            ball.x += ball.dx
            ball.y += ball.dy

            # Add subtle center bias
            distance_from_center = ball.x - center_x
            center_force = -distance_from_center * 0.002  # Subtle force towards center
            ball.dx += center_force

            # Check for invisible wall collisions
            if ball.x - ball.radius < left_wall_x:
                ball.x = left_wall_x + ball.radius
                ball.dx = abs(ball.dx) * 0.6  # Slightly increased wall bounce
            elif ball.x + ball.radius > right_wall_x:
                ball.x = right_wall_x - ball.radius
                ball.dx = -abs(ball.dx) * 0.6  # Slightly increased wall bounce

            # Check for pin collisions
            for pin_x, pin_y in self.pin_positions:
                dx = ball.x - pin_x
                dy = ball.y - pin_y
                distance = math.sqrt(dx * dx + dy * dy)
                min_distance = ball.radius + pin_radius

                if distance < min_distance:
                    # Calculate normal vector from pin to ball
                    nx = dx / distance
                    ny = dy / distance

                    # Move ball out of pin
                    overlap = min_distance - distance
                    ball.x += nx * overlap
                    ball.y += ny * overlap

                    # Calculate relative velocity
                    relative_velocity_x = ball.dx
                    relative_velocity_y = ball.dy

                    # Calculate impulse with slightly increased bounce
                    velocity_dot_normal = (relative_velocity_x * nx + relative_velocity_y * ny)
                    impulse = 1.6 * velocity_dot_normal  # Increased from 1.5 for more bounce
                    ball.dx -= impulse * nx * bounce_damping
                    ball.dy -= impulse * ny * bounce_damping

                    # Add slightly random deflection with center bias
                    random_deflection = (random.random() - 0.5) * 0.35
                    if ball.x < center_x:
                        random_deflection = abs(random_deflection) * 0.7  # Bias towards right
                    else:
                        random_deflection = -abs(random_deflection) * 0.7  # Bias towards left
                    ball.dx += random_deflection

                    # Ensure minimum velocity after bounce
                    min_velocity = 1.6  # Slightly increased minimum velocity
                    velocity = math.sqrt(ball.dx * ball.dx + ball.dy * ball.dy)
                    if velocity < min_velocity:
                        scale = min_velocity / velocity
                        ball.dx *= scale
                        ball.dy *= scale

            # Check if ball has reached multiplier zone
            multiplier_y = 100 + (15 * 30) + 15
            if ball.y >= multiplier_y and ball.active:
                last_row_x = (self.settings['width'] - ((16) * 30)) // 2 - 16
                slot_index = int((ball.x - last_row_x + 15) // 30)

                if 0 <= slot_index < len(self.multipliers):
                    multiplier = self.multipliers[slot_index]
                    winnings = round(ball.bet_amount * multiplier, 2)
                    self.coins = round(self.coins + winnings, 2)
                    ball.active = False

            # Remove balls that have fallen off screen
            if ball.y > self.settings['height']:
                self.balls.remove(ball)

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

    def draw_dashboard(self):
        # Draw dashboard background
        dashboard_rect = pygame.Rect(self.dashboard_x, 0, self.dashboard_width, self.settings['height'])
        pygame.draw.rect(self.screen, self.DARK_BLUE, dashboard_rect)

        # Draw toggle button
        toggle_button = pygame.Rect(self.dashboard_x + self.dashboard_width,
                                    self.settings['height'] // 2 - 50, 20, 100)
        pygame.draw.rect(self.screen,
                         (0, 50, 150) if self.hovered_dashboard == 'toggle' else self.BLUE,
                         toggle_button, border_radius=5)
        self.dashboard_buttons['toggle'] = toggle_button

        # Only draw controls if dashboard is somewhat visible
        if self.dashboard_x > -self.dashboard_width + 20:
            # Draw balance at the top
            balance_text = self.button_font.render("Balance:", True, self.WHITE)
            self.screen.blit(balance_text, (self.dashboard_x + 10, 20))

            # Draw coin symbol and amount for balance
            amount_box = pygame.Rect(self.dashboard_x + 10, 130, 100, 40)  # Made narrower to fit new buttons
            pygame.draw.rect(self.screen,
                             (220, 220, 220) if self.hovered_dashboard == 'amount' else self.WHITE,
                             amount_box, border_radius=5)

            # Draw coin symbol in amount box
            coin_amount_x = amount_box.left + 25
            coin_amount_y = amount_box.centery
            pygame.draw.circle(self.screen, self.GOLD, (coin_amount_x, coin_amount_y), 10)
            pygame.draw.circle(self.screen, (200, 170, 0), (coin_amount_x, coin_amount_y), 8)

            # Draw bet amount
            amount_text = self.button_font.render(f"{self.amount:.1f}", True, self.BLACK)
            amount_rect = amount_text.get_rect(midleft=(coin_amount_x + 15, amount_box.centery))
            self.screen.blit(amount_text, amount_rect)
            self.dashboard_buttons['amount'] = amount_box

            # Draw amount adjustment buttons
            button_size = 30
            spacing = 5

            # Half (÷2) button
            half_button = pygame.Rect(self.dashboard_x + 115, 130, button_size, button_size)
            pygame.draw.rect(self.screen,
                             self.DARK_BLUE if self.hovered_dashboard == 'half' else self.BLUE,
                             half_button, border_radius=5)
            half_text = self.button_font.render("÷2", True, self.WHITE)
            half_rect = half_text.get_rect(center=half_button.center)
            self.screen.blit(half_text, half_rect)
            self.dashboard_buttons['half'] = half_button

            # Double (×2) button
            double_button = pygame.Rect(self.dashboard_x + 115, 130 + button_size + spacing, button_size, button_size)
            pygame.draw.rect(self.screen,
                             self.DARK_BLUE if self.hovered_dashboard == 'double' else self.BLUE,
                             double_button, border_radius=5)
            double_text = self.button_font.render("×2", True, self.WHITE)
            double_rect = double_text.get_rect(center=double_button.center)
            self.screen.blit(double_text, double_rect)
            self.dashboard_buttons['double'] = double_button

            # Decrease button
            decrease_button = pygame.Rect(self.dashboard_x + 160, 130, button_size, button_size)
            pygame.draw.rect(self.screen,
                             self.DARK_BLUE if self.hovered_dashboard == 'decrease' else self.BLUE,
                             decrease_button, border_radius=5)
            decrease_text = self.button_font.render("-", True, self.WHITE)
            decrease_rect = decrease_text.get_rect(center=decrease_button.center)
            self.screen.blit(decrease_text, decrease_rect)
            self.dashboard_buttons['decrease'] = decrease_button

            # Increase button
            increase_button = pygame.Rect(self.dashboard_x + 160, 130 + button_size + spacing, button_size, button_size)
            pygame.draw.rect(self.screen,
                             self.DARK_BLUE if self.hovered_dashboard == 'increase' else self.BLUE,
                             increase_button, border_radius=5)
            increase_text = self.button_font.render("+", True, self.WHITE)
            increase_rect = increase_text.get_rect(center=increase_button.center)
            self.screen.blit(increase_text, increase_rect)
            self.dashboard_buttons['increase'] = increase_button

            # Draw Risk label
            risk_label = self.button_font.render("Risk:", True, self.WHITE)
            self.screen.blit(risk_label, (self.dashboard_x + 10, 190))

            # Draw Risk combobox
            risk_box = pygame.Rect(self.dashboard_x + 10, 220, 180, 40)
            pygame.draw.rect(self.screen,
                             (220, 220, 220) if self.hovered_dashboard == 'risk' else self.WHITE,
                             risk_box, border_radius=5)
            risk_text = self.button_font.render(self.risks[self.selected_risk], True, self.BLACK)
            risk_rect = risk_text.get_rect(midleft=(risk_box.left + 10, risk_box.centery))
            self.screen.blit(risk_text, risk_rect)
            self.dashboard_buttons['risk'] = risk_box

            # Draw dropdown arrow
            pygame.draw.polygon(self.screen, self.BLACK,
                                [(risk_box.right - 25, risk_box.centery - 5),
                                 (risk_box.right - 15, risk_box.centery + 5),
                                 (risk_box.right - 5, risk_box.centery - 5)])

            # Draw dropdown if open
            if self.is_dropdown_open:
                dropdown_height = len(self.risks) * 40
                dropdown_rect = pygame.Rect(risk_box.left, risk_box.bottom,
                                            risk_box.width, dropdown_height)
                pygame.draw.rect(self.screen, self.WHITE, dropdown_rect)

                for i, risk in enumerate(self.risks):
                    item_rect = pygame.Rect(dropdown_rect.left, dropdown_rect.top + i * 40,
                                            dropdown_rect.width, 40)
                    if i == self.selected_risk or self.hovered_dashboard == f'risk_{i}':
                        pygame.draw.rect(self.screen, self.BLUE, item_rect)
                    risk_text = self.button_font.render(risk, True,
                                                        self.WHITE if i == self.selected_risk or
                                                                      self.hovered_dashboard == f'risk_{i}' else self.BLACK)
                    text_rect = risk_text.get_rect(midleft=(item_rect.left + 10, item_rect.centery))
                    self.screen.blit(risk_text, text_rect)
                    self.dashboard_buttons[f'risk_{i}'] = item_rect

            # Draw Drop Ball button
            button_y = self.settings['height'] - 100
            drop_button = pygame.Rect(self.dashboard_x + 10, button_y, 180, 40)
            pygame.draw.rect(self.screen,
                             self.DARK_BLUE if self.hovered_dashboard == 'drop_ball' else self.BLUE,
                             drop_button, border_radius=5)
            button_text = self.button_font.render("Drop Ball", True, self.WHITE)
            text_rect = button_text.get_rect(center=drop_button.center)
            self.screen.blit(button_text, text_rect)
            self.dashboard_buttons['drop_ball'] = drop_button

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
        center_x = (self.settings['width'] // 2) - 29  # Subtract 10 pixels to move left
        base_y = 100
        arc_height = 30  # Height of the arc

        for i in range(len(text)):
            # Calculate position on arc
            angle = math.pi + (i - len(text) / 2) * 0.2
            x = center_x - (len(text) * 20) // 2 + i * 40
            y = base_y - math.sin(angle) * arc_height
            self.title_points.append((x, y, text[i]))

    def draw_money_counter(self):
        # Create a background rectangle for the entire counter group
        counter_width = 150  # Width of the entire counter group
        counter_height = 40  # Height of the counter group
        counter_x = self.settings['width'] - counter_width - 10  # 10 pixels from right edge
        counter_y = 15  # 15 pixels from top

        # Draw the background rectangle with rounded corners
        counter_bg = pygame.Rect(counter_x, counter_y, counter_width, counter_height)
        pygame.draw.rect(self.screen, self.BLUE, counter_bg, border_radius=10)

        # Draw coin symbol
        coin_x = counter_x + 20  # Move coin to be inside the rectangle
        coin_y = counter_y + (counter_height // 2)  # Center vertically
        pygame.draw.circle(self.screen, self.GOLD, (coin_x, coin_y), 15)
        pygame.draw.circle(self.screen, (200, 170, 0), (coin_x, coin_y), 12)

        # Draw count
        count_text = self.coin_font.render(str(self.coins), True, self.WHITE)
        count_rect = count_text.get_rect(midleft=(coin_x + 25, coin_y))
        self.screen.blit(count_text, count_rect)

        # Draw shop button (+) - Moved upward
        shop_button = pygame.Rect(counter_x + counter_width - 35, counter_y , 33,
                                  40)  # Moved up by changing y position
        pygame.draw.rect(self.screen,
                         self.DARK_BLUE if self.hovered_button == 'shop' else self.BLUE,
                         shop_button, border_radius=5)
        plus_font = pygame.font.Font(None, 48)
        plus_text = plus_font.render("+", True, self.WHITE)
        plus_rect = plus_text.get_rect(center=shop_button.center)
        self.screen.blit(plus_text, plus_rect)

        # Using a larger font size for the plus symbol
        plus_font = pygame.font.Font(None, 48)  # Increased font size from 36 to 48
        plus_text = plus_font.render("+", True, self.WHITE)
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

        # Draw arrows and current size with hover effects
        left_color = self.DARK_BLUE if self.hovered_button == 'size_left' else self.BLUE
        right_color = self.DARK_BLUE if self.hovered_button == 'size_right' else self.BLUE

        # Draw arrow buttons with proper colors
        pygame.draw.rect(self.screen, left_color, self.settings_buttons['size_left'], border_radius=5)
        pygame.draw.rect(self.screen, right_color, self.settings_buttons['size_right'], border_radius=5)

        # Draw arrow symbols (centered)
        left_arrow = self.button_font.render("<", True, self.WHITE)
        right_arrow = self.button_font.render(">", True, self.WHITE)

        # Center the arrows in their buttons
        left_rect = left_arrow.get_rect(center=self.settings_buttons['size_left'].center)
        right_rect = right_arrow.get_rect(center=self.settings_buttons['size_right'].center)

        self.screen.blit(left_arrow, left_rect)
        self.screen.blit(right_arrow, right_rect)

        # Draw current size
        size_text = self.button_font.render(self.window_sizes[self.selected_size_index], True, text_color)
        size_rect = size_text.get_rect(center=(self.settings['width'] // 2, 215))
        self.screen.blit(size_text, size_rect)

        # Draw dark mode toggle with hover effect
        dark_mode_color = self.DARK_BLUE if self.hovered_button == 'dark_mode' else self.BLUE
        pygame.draw.rect(self.screen, dark_mode_color, self.settings_buttons['dark_mode'], border_radius=10)
        dark_text = self.button_font.render(f"Dark Mode: {'On' if self.settings['dark_mode'] else 'Off'}", True,
                                            self.WHITE)
        dark_rect = dark_text.get_rect(center=self.settings_buttons['dark_mode'].center)
        self.screen.blit(dark_text, dark_rect)

        # Draw back button with hover effect
        back_color = self.DARK_BLUE if self.hovered_button == 'back' else self.BLUE
        pygame.draw.rect(self.screen, back_color, self.settings_buttons['back'], border_radius=10)
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

        # Check game buttons
        elif self.current_state == self.PLAYING:
            if hasattr(self, 'game_back_button') and self.game_back_button.collidepoint(pos):
                self.hovered_button = 'game_back'
            elif hasattr(self, 'game_shop_button') and self.game_shop_button.collidepoint(pos):
                self.hovered_button = 'game_shop'
                # Check dashboard buttons if in playing state
            elif self.current_state == self.PLAYING:
                self.hovered_dashboard = None
                for button_name, button_rect in self.dashboard_buttons.items():
                    if button_rect.collidepoint(pos):
                        self.hovered_dashboard = button_name
                        break

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

    def update_dashboard(self):
        target_x = 0 if self.dashboard_extended else -self.dashboard_width
        self.dashboard_x += (target_x - self.dashboard_x) * 0.2

    def handle_dashboard_click(self, pos):
        for button_name, button_rect in self.dashboard_buttons.items():
            if button_rect.collidepoint(pos):
                if button_name == 'toggle':
                    self.dashboard_extended = not self.dashboard_extended
                elif button_name == 'increase':
                    new_amount = round(self.amount + 0.1, 1)
                    self.amount = min(new_amount, float(self.coins))
                elif button_name == 'decrease':
                    new_amount = round(self.amount - 0.1, 1)
                    self.amount = max(0, new_amount)
                elif button_name == 'double':
                    new_amount = round(self.amount * 2, 1)
                    self.amount = min(new_amount, float(self.coins))
                elif button_name == 'half':
                    self.amount = round(self.amount / 2, 1)
                elif button_name == 'risk':
                    self.is_dropdown_open = not self.is_dropdown_open
                elif button_name.startswith('risk_'):
                    self.selected_risk = int(button_name.split('_')[1])
                    self.is_dropdown_open = False
                elif button_name == 'drop_ball':
                    self.drop_ball()
                return True
        return False

    def handle_click(self, pos):
        # Handle dashboard clicks first if in playing state
        if self.current_state == self.PLAYING:
            if self.handle_dashboard_click(pos):
                return
        # Check dashboard toggle
        toggle_button = pygame.Rect(self.dashboard_x + self.dashboard_width,
                                    self.settings['height'] // 2 - 50, 20, 100)
        if toggle_button.collidepoint(pos):
            self.dashboard_extended = not self.dashboard_extended
            return

        if self.dashboard_x >= 0:  # Only handle dashboard clicks when extended
            # Check risk dropdown
            risk_box = pygame.Rect(self.dashboard_x + 10, 220, 180, 40)
            if risk_box.collidepoint(pos):
                self.is_dropdown_open = not self.is_dropdown_open
                return

            # Check dropdown items
            if self.is_dropdown_open:
                dropdown_rect = pygame.Rect(risk_box.left, risk_box.bottom,
                                            risk_box.width, len(self.risks) * 40)
                if dropdown_rect.collidepoint(pos):
                    self.selected_risk = (pos[1] - dropdown_rect.top) // 40
                    self.is_dropdown_open = False
                    return

            # Check drop ball button
            if hasattr(self, 'drop_button') and self.drop_button.collidepoint(pos):
                self.drop_ball()
                return
        if self.current_state == self.MENU:
            # Check shop button
            if hasattr(self, 'shop_button') and self.shop_button.collidepoint(pos):
                self.current_state = self.SHOP
                return

            for button_name, button_rect in self.buttons.items():
                if button_rect.collidepoint(pos):
                    if button_name == 'start':
                        self.current_state = self.PLAYING  # Changed this line
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

        elif self.current_state == self.PLAYING:
            if hasattr(self, 'game_back_button') and self.game_back_button.collidepoint(pos):
                self.current_state = self.MENU
            elif hasattr(self, 'game_shop_button') and self.game_shop_button.collidepoint(pos):
                self.current_state = self.SHOP

    def draw_game(self):
        # Draw background
        self.draw_gradient_background()

        # Draw back button (top left)
        back_button = pygame.Rect(10, 10, 100, 40)
        pygame.draw.rect(self.screen,
                         self.DARK_BLUE if self.hovered_button == 'game_back' else self.BLUE,
                         back_button, border_radius=10)
        back_text = self.button_font.render("Back", True, self.WHITE)
        back_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, back_rect)
        self.game_back_button = back_button

        # Draw shop menu button (top right)
        shop_button = pygame.Rect(self.settings['width'] - 205, 10, 200, 40)
        pygame.draw.rect(self.screen,
                         self.DARK_BLUE if self.hovered_button == 'game_shop' else self.BLUE,
                         shop_button, border_radius=10)
        shop_text = self.button_font.render("Shop Menu", True, self.WHITE)
        shop_rect = shop_text.get_rect(center=shop_button.center)
        self.screen.blit(shop_text, shop_rect)
        self.game_shop_button = shop_button

        # Draw Plinko pins
        pin_radius = 5
        start_y = 100  # Starting Y position
        vertical_spacing = 30  # Space between rows
        horizontal_spacing = 30  # Space between pins in the same row

        # Calculate the width of the widest row to center the entire pin layout
        max_pins_in_row = 17  # Changed to 17 for the bottom row
        total_width = (max_pins_in_row - 1) * horizontal_spacing
        start_x = (self.settings['width'] - total_width) // 2

        # Store pin positions for collision detection
        self.pin_positions = []
        self.draw_dashboard()
        # Draw pins row by row
        for row in range(16):  # 16 rows total
            # Calculate number of pins in this row
            pins_in_row = row + 3  # First row has 3 pins, each row adds one more

            # Calculate x position for the first pin in this row to center the row
            row_width = (pins_in_row - 1) * horizontal_spacing
            row_start_x = (self.settings['width'] - row_width) // 2

            # Draw each pin in the row
            for pin in range(pins_in_row):
                x = row_start_x + (pin * horizontal_spacing)
                y = start_y + (row * vertical_spacing)

                # Store pin position
                self.pin_positions.append((x, y))

                # Draw pin
                pygame.draw.circle(self.screen, self.WHITE, (x, y), pin_radius)
                # Draw a slightly smaller inner circle for 3D effect
                pygame.draw.circle(self.screen, self.GRAY, (x, y), pin_radius - 2)
        for ball in self.balls:
            pygame.draw.circle(self.screen, ball.color, (int(ball.x), int(ball.y)), ball.radius)
            # Draw a slightly smaller inner circle for 3D effect
            pygame.draw.circle(self.screen, (200, 170, 0), (int(ball.x), int(ball.y)), ball.radius - 2)

            # Draw the dashboard last
        self.draw_dashboard()
        # Draw multipliers
        multiplier_y = start_y + (15 * vertical_spacing) + 15  # Position between last row pins
        last_row_x = (self.settings['width'] - ((16) * horizontal_spacing)) // 2 - 16  # Center multiplier boxes

        for i, multiplier in enumerate(self.multipliers):
            # Calculate x position to be between pins
            x = last_row_x + (i * horizontal_spacing) - (horizontal_spacing // 2)

            # Calculate color based on multiplier value
            if multiplier >= 110:
                color = self.multiplier_colors[0]
            elif multiplier >= 41:
                color = self.multiplier_colors[1]
            elif multiplier >= 10:
                color = self.multiplier_colors[2]
            elif multiplier >= 5:
                color = self.multiplier_colors[3]
            elif multiplier >= 3:
                color = self.multiplier_colors[4]
            elif multiplier >= 2:
                color = self.multiplier_colors[5]
            elif multiplier >= 1.5:
                color = self.multiplier_colors[6]
            elif multiplier >= 1:
                color = self.multiplier_colors[7]
            elif multiplier >= 0.5:
                color = self.multiplier_colors[8]
            else:  # 0.3x
                color = self.multiplier_colors[9]

            # Draw multiplier box
            multiplier_width = 25  # Made narrower to fit between pins
            multiplier_height = 25  # Made shorter to fit better
            multiplier_rect = pygame.Rect(x - (multiplier_width // 2), multiplier_y,
                                          multiplier_width, multiplier_height)
            pygame.draw.rect(self.screen, color, multiplier_rect, border_radius=5)

            # Draw multiplier text with smaller font
            multiplier_font = pygame.font.Font(None, 20)  # Smaller font size
            text = multiplier_font.render(f"{multiplier}x", True, self.WHITE)
            text_rect = text.get_rect(center=multiplier_rect.center)
            self.screen.blit(text, text_rect)

    def run(self):
        running = True
        while running:
            # Get mouse position for hover effects
            mouse_pos = pygame.mouse.get_pos()
            self.update_hover_state(mouse_pos)

            # Update game state
            if self.current_state == self.PLAYING:
                self.update_dashboard()
                self.update_balls()  # Make sure this is called!

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.current_state in [self.SETTINGS, self.PLAYING, self.SHOP]:
                            self.current_state = self.MENU

            # Draw current state
            if self.current_state == self.MENU:
                self.draw_menu()
            elif self.current_state == self.SETTINGS:
                self.draw_settings()
            elif self.current_state == self.SHOP:
                self.draw_shop()
            elif self.current_state == self.PLAYING:
                self.draw_game()

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = PlinkoGame()
    game.run()