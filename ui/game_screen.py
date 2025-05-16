import pygame
import math
import random
from .base_screen import BaseScreen
from core.game_objects import Ball, Pin
from .dashboard import Dashboard

class GameScreen(BaseScreen):
    def __init__(self, settings_manager, on_back, on_shop, active_skin="default"):
        super().__init__(settings_manager)
        
        # Callbacks
        self.on_back = on_back
        self.on_shop = on_shop
        
        # Game state
        self.coins = 100  # Starting amount
        self.balls = []  # Active balls
        self.pins = []  # Pins
        self.pin_positions = []  # Positions for collision
        self.multipliers = [110, 41, 10, 5, 3, 2, 1.5, 1, 0.5, 0.3, 0.5, 1, 1.5, 2, 3, 5, 10, 41, 110]
        self.multiplier_rects = []
        
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
        
        # Special effects and skins
        self.active_ball_skin = active_skin  # Use the provided skin
        self.lucky_charm_active = False
        self.lucky_charm_time = 0
        
        # Create dashboard
        self.dashboard = Dashboard(settings_manager, self.drop_ball, self.coins)
        
        # Initialize board elements
        self.create_pins()
        self.create_multiplier_zones()
        self.update_button_positions()
        
    def update_button_positions(self):
        """Update button positions for navigation"""
        width, height = self.settings_manager.get_window_size()
        
        # Navigation buttons
        self.buttons = {
            'back': pygame.Rect(10, 10, 100, 40),
            'shop': pygame.Rect(width - 110, 10, 100, 40)
        }
        
    def create_pins(self):
        """Create pins for the game board"""
        width, height = self.settings_manager.get_window_size()
        
        pin_radius = 5
        start_y = 100  # Starting Y position
        vertical_spacing = 30  # Space between rows
        horizontal_spacing = 30  # Space between pins in the same row
        
        # Calculate the width of the widest row to center the entire pin layout
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
        start_y = 100  # Same as pins
        multiplier_y = start_y + (15 * vertical_spacing) + 15  # Position below the last row of pins
        
        # Calculate position of the left-most multiplier
        last_row_x = (width - ((16) * horizontal_spacing)) // 2 - 16
        
        # Clear previous rects
        self.multiplier_rects = []
        
        # Create rectangles for each multiplier
        for i, multiplier in enumerate(self.multipliers):
            # Calculate x position
            x = last_row_x + (i * horizontal_spacing) - (horizontal_spacing // 2)
            
            # Create rectangle
            multiplier_width = 25
            multiplier_height = 25
            multiplier_rect = pygame.Rect(x - (multiplier_width // 2), multiplier_y,
                                         multiplier_width, multiplier_height)
            
            self.multiplier_rects.append(multiplier_rect)
            
    def drop_ball(self, bet_amount):
        """Drop a new ball on the board"""
        if bet_amount <= self.coins and bet_amount > 0:
            width = self.settings_manager.get_setting('width')
            
            # Calculate the starting position - more centered
            center_x = width / 2
            random_offset = random.uniform(-20, 20)  # Random starting position
            ball_start_x = center_x + random_offset
            ball_start_y = 70
            
            # Choose ball color based on active skin
            ball_color = (255, 200, 0)  # Default gold
            
            # Apply the correct skin color
            if self.active_ball_skin == "gold":
                ball_color = (255, 215, 0)  # Brighter gold
            elif self.active_ball_skin == "rainbow":
                # Random color for rainbow effect
                ball_color = (
                    random.randint(150, 255),
                    random.randint(150, 255),
                    random.randint(150, 255)
                )
            elif self.active_ball_skin == "ice":
                ball_color = (100, 200, 255)  # Ice blue
            elif self.active_ball_skin == "fire":
                ball_color = (255, 100, 0)  # Fire orange/red
            
            # Create new ball with bet amount
            new_ball = Ball(ball_start_x, ball_start_y, 9.5, ball_color, bet_amount)
            new_ball.dy = 2  # Initial drop speed
            # Add slight random initial horizontal velocity
            new_ball.dx = random.uniform(-0.8, 0.8)
            
            # Apply lucky charm effect if active
            if self.lucky_charm_active:
                # Lucky charm gives slightly more favorable physics
                new_ball.dx = random.uniform(-0.5, 0.5)  # Less horizontal variance
            
            self.balls.append(new_ball)
            
            # Deduct bet amount (rounded)
            self.coins = round(self.coins - bet_amount, 2)
            
            # Update dashboard coins
            self.dashboard.update_coins(self.coins)
            
    def update(self):
        """Update game elements"""
        # Update dashboard
        self.dashboard.update()
        
        # Keep coins synchronized with dashboard
        if hasattr(self.dashboard, 'coins') and self.dashboard.coins != self.coins:
            self.coins = self.dashboard.coins
        
        # Update lucky charm timer
        if self.lucky_charm_active and self.lucky_charm_time > 0:
            self.lucky_charm_time -= 1/60  # Decrease by 1 second per 60 frames
            if self.lucky_charm_time <= 0:
                self.lucky_charm_active = False
        
        # Update balls and check for collisions
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
            # Update ball and check if it should be removed
            if ball.update(self.pin_positions, boundaries, self.multipliers, 
                          self.multiplier_rects, self.on_win):
                self.balls.remove(ball)
                
    def on_win(self, amount):
        """Handle winning event"""
        self.coins = round(self.coins + amount, 2)
        self.dashboard.update_coins(self.coins)
        
    def draw(self, screen):
        """Draw the game screen"""
        # Draw background
        self.draw_gradient_background(screen)
        
        # Draw navigation buttons
        self.draw_button(screen, 'back', self.buttons['back'], "Back")
        self.draw_button(screen, 'shop', self.buttons['shop'], "Shop")
        
        # Draw lucky charm timer if active
        if self.lucky_charm_active and self.lucky_charm_time > 0:
            # Create semi-transparent overlay for timer
            timer_surface = pygame.Surface((150, 30), pygame.SRCALPHA)
            timer_surface.fill((0, 0, 0, 100))  # Semi-transparent black
            
            # Calculate minutes and seconds
            minutes = int(self.lucky_charm_time // 60)
            seconds = int(self.lucky_charm_time % 60)
            
            # Create timer text
            font = pygame.font.Font(None, 24)
            timer_text = font.render(f"Lucky: {minutes:02}:{seconds:02}", True, (255, 215, 0))
            
            # Position in top right
            timer_rect = timer_surface.get_rect(topright=(self.settings_manager.get_setting('width') - 10, 10))
            text_rect = timer_text.get_rect(center=timer_rect.center)
            
            # Draw timer
            screen.blit(timer_surface, timer_rect)
            screen.blit(timer_text, text_rect)
        
        # Draw pins
        for pin in self.pins:
            pin.draw(screen)
            
        # Draw multiplier zones
        for i, rect in enumerate(self.multiplier_rects):
            # Calculate color based on multiplier value
            multiplier = self.multipliers[i]
            
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
            pygame.draw.rect(screen, color, rect, border_radius=5)
            
            # Draw multiplier text
            multiplier_font = pygame.font.Font(None, 20)
            text = multiplier_font.render(f"{multiplier}x", True, self.WHITE)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
            
        # Draw active balls
        for ball in self.balls:
            ball.draw(screen)
            
        # Draw dashboard
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
        
        # Check dashboard buttons
        dashboard_result = self.dashboard.handle_click(pos)
        
        # Always synchronize coins with dashboard after any click
        if hasattr(self.dashboard, 'coins'):
            self.coins = self.dashboard.coins
            
        return dashboard_result  # Return the result from dashboard
        
    def update_coins(self, new_coins):
        """Update coins in both the game and dashboard"""
        self.coins = new_coins
        if hasattr(self.dashboard, 'update_coins'):
            self.dashboard.update_coins(new_coins) 