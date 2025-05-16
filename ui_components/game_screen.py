import pygame
import random
from physics.ball_physics import BallPhysics
from physics.game_objects import Ball, Pin
from ui_components.dashboard import Dashboard

class GameScreen:
    """Game screen where gameplay happens"""
    
    def __init__(self, settings_manager, game_state, on_back, on_shop):
        # Store references
        self.settings_manager = settings_manager
        self.game_state = game_state
        self.on_back = on_back
        self.on_shop = on_shop
        
        # Set up colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GOLD = (255, 215, 0)
        self.BLUE = (0, 120, 255)
        self.DARK_BLUE = (0, 80, 180)
        self.GRAY = (40, 40, 40)
        self.LIGHT_GRAY = (200, 200, 200)
        self.GREEN = (50, 200, 100)
        
        # Initialize game elements
        self.balls = []  # Active balls
        self.pins = []  # Pins
        self.pin_positions = []  # Positions for collision
        self.multipliers = [110, 41, 10, 5, 3, 2, 1.5, 1, 0.5, 0.3, 0.5, 1, 1.5, 2, 3, 5, 10, 41, 110]
        self.multiplier_rects = []
        
        # Colors for multipliers (from highest to lowest)
        self.multiplier_colors = [
            (140, 0, 0),    # Deep Red (110x)
            (200, 40, 40),  # Red (41x)
            (240, 80, 80),  # Light Red (10x)
            (240, 120, 0),  # Orange (5x)
            (240, 160, 0),  # Light Orange (3x)
            (240, 200, 0),  # Yellow (2x)
            (200, 220, 0),  # Yellow-Green (1.5x)
            (100, 200, 0),  # Green (1x)
            (0, 160, 80),   # Blue-Green (0.5x)
            (0, 120, 160)   # Blue (0.3x)
        ]
        
        # Set up physics engine
        self.physics = BallPhysics()
        
        # Set up UI elements
        self.dashboard = Dashboard(settings_manager, self.drop_ball, game_state)
        self.hovered_button = None
        
        # Set up fonts
        self.button_font = pygame.font.Font(None, 28)
        self.multiplier_font = pygame.font.Font(None, 20)
        
        # Initialize game elements
        self.create_pins()
        self.create_multiplier_zones()
        self.update_button_positions()
    
    def update_button_positions(self):
        """Update button positions for navigation"""
        width, height = self.settings_manager.get_window_size()
        
        # Navigation buttons
        button_size = 50
        padding = 15
        
        self.buttons = {
            'back': pygame.Rect(padding, padding, button_size, button_size),
            'shop': pygame.Rect(width - button_size - padding, padding, button_size, button_size)
        }
    
    def create_pins(self):
        """Create pins for the game board"""
        width, height = self.settings_manager.get_window_size()
        
        pin_radius = 5
        start_y = 100  # Starting Y position (moved up by 20px from 120)
        vertical_spacing = 30  # Space between rows
        horizontal_spacing = 30  # Space between pins in the same row
        
        # Calculate the width of the widest row to center the layout
        max_pins_in_row = 17  # Bottom row
        total_width = (max_pins_in_row - 1) * horizontal_spacing
        start_x = (width - total_width) // 2
        
        # Clear previous pins
        self.pins = []
        self.pin_positions = []
        
        # Create pins row by row
        for row in range(16):  # 16 rows total
            # Calculate number of pins in this row
            pins_in_row = row + 3  # First row has 3 pins, each row adds one more
            
            # Calculate x position for the first pin in this row to center the row
            row_width = (pins_in_row - 1) * horizontal_spacing
            row_start_x = (width - row_width) // 2
            
            # Create each pin in the row
            for pin in range(pins_in_row):
                x = row_start_x + (pin * horizontal_spacing)
                y = start_y + (row * vertical_spacing)
                
                # Add pin
                new_pin = Pin(x, y, pin_radius)
                self.pins.append(new_pin)
                
                # Store position for collision detection
                self.pin_positions.append((x, y))
    
    def create_multiplier_zones(self):
        """Create multiplier zones at the bottom of the board"""
        width, height = self.settings_manager.get_window_size()
        
        # Position parameters
        vertical_spacing = 30
        horizontal_spacing = 30
        start_y = 100  # Same as pins (moved up by 20px from 120)
        multiplier_y = start_y + (15 * vertical_spacing) - 15  # Position below the last row of pins, moved up by 30px
        
        # Calculate position of the left-most multiplier
        last_row_x = (width - ((16) * horizontal_spacing)) // 2 - 16
        
        # Clear previous rects
        self.multiplier_rects = []
        
        # Create rectangles for each multiplier - ensure they fit the window width
        multiplier_width = 26  # Slightly smaller width for better fit
        multiplier_height = 35
        
        # Calculate total width needed and adjust horizontal spacing if needed
        total_width_needed = multiplier_width * len(self.multipliers)
        available_width = width - 40  # Leave some margin
        
        # Adjust spacing if needed to fit within window
        if total_width_needed > available_width:
            horizontal_spacing = max(20, (available_width - multiplier_width) / (len(self.multipliers) - 1))
        
        for i, multiplier in enumerate(self.multipliers):
            # Calculate x position with new spacing
            x = last_row_x + (i * horizontal_spacing)
            
            # Create rectangle with adjusted size
            multiplier_rect = pygame.Rect(x - (multiplier_width // 2), multiplier_y,
                                         multiplier_width, multiplier_height)
            
            self.multiplier_rects.append(multiplier_rect)
    
    def drop_ball(self, bet_amount):
        """Drop a new ball on the board"""
        # Check if bet is valid
        if bet_amount <= self.game_state.coins and bet_amount > 0:
            width = self.settings_manager.get_setting('width')
            
            # Calculate starting position
            center_x = width / 2
            random_offset = random.uniform(-20, 20)  # Random starting position
            ball_start_x = center_x + random_offset
            ball_start_y = 70  # Start above the first row of pins (moved up by 20px from 90)
            
            # Choose ball color based on active skin
            ball_color = (255, 200, 0)  # Default gold
            
            # Apply the correct skin color
            active_skin = self.game_state.active_ball_skin
            if active_skin == "gold":
                ball_color = (255, 215, 0)  # Brighter gold
            elif active_skin == "rainbow":
                # Random color for rainbow effect
                ball_color = (
                    random.randint(150, 255),
                    random.randint(150, 255),
                    random.randint(150, 255)
                )
            elif active_skin == "ice":
                ball_color = (100, 200, 255)  # Ice blue
            elif active_skin == "fire":
                ball_color = (255, 100, 0)  # Fire orange/red
            
            # Create new ball
            new_ball = Ball(ball_start_x, ball_start_y, 9.5, ball_color, bet_amount)
            new_ball.dy = 2  # Initial drop speed
            # Add slight random horizontal velocity
            new_ball.dx = random.uniform(-0.8, 0.8)
            
            # Apply lucky charm effect if active
            if self.game_state.lucky_charm_active:
                # Lucky charm gives slightly more favorable physics
                new_ball.dx = random.uniform(-0.5, 0.5)  # Less horizontal variance
            
            self.balls.append(new_ball)
            
            # Deduct bet amount from player's coins
            self.game_state.subtract_coins(bet_amount)
    
    def update(self):
        """Update game elements"""
        # Update dashboard
        self.dashboard.update()
        
        width = self.settings_manager.get_setting('width')
        height = self.settings_manager.get_setting('height')
        
        # Define boundaries for ball physics
        boundaries = {
            'left': (width - ((16) * 30)) // 2 - 20,
            'right': width - ((width - ((16) * 30)) // 2 - 20),
            'bottom': height
        }
        
        # Update each ball
        for ball in self.balls[:]:
            # Update ball physics
            self.physics.update_position(ball, self.pin_positions, boundaries)
            
            # Check for multiplier collisions and out-of-bounds
            if ball.check_multiplier_collision(self.multipliers, self.multiplier_rects, self.on_win) or ball.is_out_of_bounds(boundaries['bottom']):
                self.balls.remove(ball)
    
    def on_win(self, amount):
        """Handle winning event"""
        self.game_state.add_coins(amount)
    
    def draw(self, screen):
        """Draw the game screen"""
        # Draw background gradient
        self.draw_gradient_background(screen)
        
        # Draw lucky charm timer if active
        remaining = self.game_state.check_lucky_charm()
        if self.game_state.lucky_charm_active and remaining > 0:
            # Create a more modern timer display
            minutes, seconds = self.game_state.get_lucky_charm_minutes_seconds()
            
            # Calculate width based on remaining time
            max_width = 150
            time_ratio = remaining / 1200  # 1200 is the default duration
            current_width = max_width * time_ratio
            
            # Create timer background
            timer_height = 8
            timer_y = 55  # Moved up to avoid overlap with pins
            timer_bg = pygame.Rect(self.settings_manager.get_setting('width') - max_width - 20, timer_y, max_width, timer_height)
            pygame.draw.rect(screen, (40, 40, 40, 150), timer_bg, border_radius=4)
            
            # Draw timer fill
            timer_fill = pygame.Rect(timer_bg.left, timer_bg.top, current_width, timer_height)
            pygame.draw.rect(screen, self.GOLD, timer_fill, border_radius=4)
            
            # Create timer text
            font = pygame.font.Font(None, 20)
            timer_text = font.render(f"Lucky Charm: {minutes:02}:{seconds:02}", True, self.GOLD)
            text_rect = timer_text.get_rect(midbottom=(timer_bg.centerx, timer_bg.top - 5))
            
            # Draw timer text
            screen.blit(timer_text, text_rect)
        
        # Draw pins with modernized look
        for pin in self.pins:
            pin.draw(screen)
            
        # Draw multiplier zones with better styling
        for i, rect in enumerate(self.multiplier_rects):
            multiplier = self.multipliers[i]
            
            # Calculate color based on multiplier value with smoother transition
            color_index = min(9, int(10 * (1 - (multiplier - 0.3) / (110 - 0.3))))
            color = self.multiplier_colors[color_index]
                
            # Draw multiplier box with rounded corners and border
            pygame.draw.rect(screen, color, rect, border_radius=5)
            
            # Dark overlay at the top of the box for dimension
            pygame.draw.rect(screen, (0, 0, 0, 50), 
                            pygame.Rect(rect.left, rect.top, rect.width, rect.height//3),
                            border_radius=5)
            
            # Draw multiplier text with better font
            text = self.multiplier_font.render(f"{multiplier}x", True, self.WHITE)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
            
        # Draw active balls
        for ball in self.balls:
            ball.draw(screen)
        
        # Draw navigation buttons with modern icons
        self.draw_button_with_icon(screen, 'back', self.buttons['back'], "←")
        self.draw_button_with_icon(screen, 'shop', self.buttons['shop'], "$")
            
        # Draw dashboard UI
        self.dashboard.draw(screen)
    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        # Check navigation buttons
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                if button_name == 'back':
                    return self.on_back()
                elif button_name == 'shop':
                    return self.on_shop()
        
        # Check dashboard clicks
        return self.dashboard.handle_click(pos)
    
    def update_hover_state(self, pos):
        """Update hover state of buttons"""
        self.hovered_button = None
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                self.hovered_button = button_name
                break
                
        # Update dashboard hover state
        self.dashboard.update_hover_state(pos)
    
    def draw_gradient_background(self, screen):
        """Draw a gradient background"""
        width, height = self.settings_manager.get_window_size()
        
        # Check if dark mode is enabled
        dark_mode = self.settings_manager.get_setting('dark_mode', False)
        
        # Create a smoother gradient background
        if dark_mode:
            # Dark mode gradient (dark blue to black)
            for y in range(0, height, 1):
                # Calculate color gradient
                ratio = y / height
                r = int(10 - ratio * 10)
                g = int(15 - ratio * 15)
                b = int(30 - ratio * 20)
                color = (r, g, b)
                pygame.draw.line(screen, color, (0, y), (width, y))
        else:
            # Light mode gradient (blue to darker blue)
            for y in range(0, height, 1):
                # Calculate color gradient
                ratio = y / height
                r = int(10 + ratio * 5)
                g = int(30 + ratio * 20)
                b = int(60 + ratio * 50)
                color = (r, g, b)
                pygame.draw.line(screen, color, (0, y), (width, y))
    
    def draw_button_with_icon(self, screen, button_name, button_rect, icon):
        """Draw a circular button with an icon"""
        # Check if dark mode is enabled
        dark_mode = self.settings_manager.get_setting('dark_mode', False)
        
        # Select colors based on dark mode
        if dark_mode:
            button_bg = (60, 60, 80) if button_name == self.hovered_button else (40, 40, 50)
            shadow_color = (20, 20, 25)
            text_color = self.WHITE
        else:
            button_bg = self.DARK_BLUE if button_name == self.hovered_button else self.BLUE
            shadow_color = (0, 40, 100)
            text_color = self.WHITE
        
        # Draw shadow (circle)
        shadow_center = (button_rect.centerx + 2, button_rect.centery + 2)
        pygame.draw.circle(screen, shadow_color, shadow_center, button_rect.width // 2)
        
        # Draw button (circle)
        pygame.draw.circle(screen, button_bg, button_rect.center, button_rect.width // 2)
        
        # Draw icon
        icon_font = pygame.font.Font(None, 36)
        icon_text = icon_font.render(icon, True, text_color)
        icon_rect = icon_text.get_rect(center=button_rect.center)
        screen.blit(icon_text, icon_rect)
        
    def draw_button(self, screen, button_name, button_rect, text):
        """Draw a button with hover effect (kept for compatibility)"""
        # Check if dark mode is enabled
        dark_mode = self.settings_manager.get_setting('dark_mode', False)
        
        # Select colors based on dark mode
        if dark_mode:
            button_bg = (60, 60, 70) if button_name == self.hovered_button else (40, 40, 50)
            shadow_color = (20, 20, 25)
            text_color = self.WHITE
        else:
            button_bg = self.DARK_BLUE if button_name == self.hovered_button else self.BLUE
            shadow_color = (0, 40, 100)
            text_color = self.WHITE
        
        # Draw shadow
        shadow_rect = pygame.Rect(button_rect.left + 2, button_rect.top + 2,
                                button_rect.width, button_rect.height)
        pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=5)
        
        # Draw button
        pygame.draw.rect(screen, button_bg, button_rect, border_radius=5)
        
        # Draw text
        text_surf = self.button_font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=button_rect.center)
        screen.blit(text_surf, text_rect) 