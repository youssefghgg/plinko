import pygame
import math
import random
from ui.base_screen import BaseScreen

class MenuScreen(BaseScreen):
    def __init__(self, settings_manager, on_start, on_settings, on_shop, on_quit):
        super().__init__(settings_manager)
        
        # Callback functions
        self.on_start = on_start
        self.on_settings = on_settings 
        self.on_shop = on_shop
        self.on_quit = on_quit
        
        # Title animation properties
        self.title_points = []
        self.title_animation_time = 0
        self.particles = []  # For particle effects
        self.generate_title_arc()
        self.update_button_positions()
        
        # Coin balance
        self.coins = 100  # Starting amount
        
        # Add floating balls in background
        self.floating_balls = []
        for _ in range(10):
            self.add_floating_ball()
            
    def add_floating_ball(self):
        """Add a floating decorative ball to the background"""
        width, height = self.settings_manager.get_window_size()
        x = random.randint(0, width)
        y = random.randint(0, height)
        speed_x = random.uniform(-0.5, 0.5)
        speed_y = random.uniform(-0.5, 0.5)
        size = random.randint(5, 20)
        color = random.choice([
            (255, 215, 0),   # Gold
            (0, 100, 255),   # Blue
            (255, 255, 255)  # White
        ])
        
        self.floating_balls.append({
            'x': x,
            'y': y,
            'speed_x': speed_x,
            'speed_y': speed_y,
            'size': size,
            'color': color,
            'alpha': random.randint(50, 150)
        })
    
    def update_button_positions(self):
        """Update button positions based on screen size"""
        width, height = self.settings_manager.get_window_size()
        
        # Main buttons - placed in a vertical column
        button_width = 220
        button_height = 60
        button_spacing = 20
        start_y = height // 2
        
        self.buttons = {
            'start': pygame.Rect(width // 2 - button_width // 2, 
                                start_y, 
                                button_width, button_height),
            'settings': pygame.Rect(width // 2 - button_width // 2, 
                                  start_y + button_height + button_spacing, 
                                  button_width, button_height),
            'shop': pygame.Rect(width // 2 - button_width // 2,
                              start_y + 2 * (button_height + button_spacing),
                              button_width, button_height),
            'quit': pygame.Rect(width // 2 - button_width // 2, 
                              start_y + 3 * (button_height + button_spacing), 
                              button_width, button_height)
        }
        
        # Shop button on the money counter
        counter_width = 150
        counter_height = 40
        counter_x = width - counter_width - 10
        counter_y = 15
        self.shop_button = pygame.Rect(counter_x + counter_width - 35, counter_y, 33, 40)
        
    def generate_title_arc(self):
        """Generate points for title text to follow an arc"""
        self.title_points = []
        text = "PLINKO"
        width = self.settings_manager.get_setting('width')
        base_y = 120  # Higher up to make room for animation
        arc_height = 40  # More pronounced arc
        
        # Calculate center
        center_x = width // 2
        
        for i in range(len(text)):
            # Calculate position on arc
            angle = math.pi + (i - len(text) / 2) * 0.3  # More spread out
            x = center_x + (i - len(text) / 2) * 70  # Wider spacing
            y = base_y - math.sin(angle) * arc_height
            self.title_points.append((x, y, text[i]))
            
    def update(self):
        """Update animation states"""
        # Update title animation
        self.title_animation_time += 0.02
        
        # Update floating balls
        width, height = self.settings_manager.get_window_size()
        for ball in self.floating_balls:
            # Move balls
            ball['x'] += ball['speed_x']
            ball['y'] += ball['speed_y']
            
            # Bounce off walls
            if ball['x'] < 0 or ball['x'] > width:
                ball['speed_x'] *= -1
            if ball['y'] < 0 or ball['y'] > height:
                ball['speed_y'] *= -1
                
        # Add particles occasionally
        if random.random() < 0.1:
            # Add a particle near a random letter
            if self.title_points:
                point = random.choice(self.title_points)
                particle_x = point[0] + random.uniform(-20, 20)
                particle_y = point[1] + random.uniform(-10, 30)
                self.particles.append({
                    'x': particle_x,
                    'y': particle_y,
                    'speed_x': random.uniform(-0.3, 0.3),
                    'speed_y': random.uniform(-0.5, 0.2),
                    'size': random.uniform(2, 5),
                    'lifetime': 100,
                    'color': (255, 215, 0)  # Gold particles
                })
                
        # Update particles
        for particle in self.particles[:]:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            particle['lifetime'] -= 1
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
    
    def draw_money_counter(self, screen):
        """Draw money counter with improved design"""
        width = self.settings_manager.get_setting('width')
        
        # Create a background rectangle for the entire counter group
        counter_width = 150
        counter_height = 40
        counter_x = width - counter_width - 10
        counter_y = 15
        
        # Draw shadow first (for depth)
        shadow_rect = pygame.Rect(counter_x + 3, counter_y + 3, counter_width, counter_height)
        pygame.draw.rect(screen, (0, 50, 100), shadow_rect, border_radius=10)
        
        # Draw the background rectangle with rounded corners
        counter_bg = pygame.Rect(counter_x, counter_y, counter_width, counter_height)
        pygame.draw.rect(screen, self.BLUE, counter_bg, border_radius=10)
        
        # Draw coin symbol
        coin_x = counter_x + 20
        coin_y = counter_y + (counter_height // 2)
        
        # Draw outer gold circle with glow effect
        for r in range(17, 14, -1):
            alpha = int(255 * (r - 14) / 3)
            glow_surface = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*self.GOLD[:3], alpha), (r, r), r)
            screen.blit(glow_surface, (coin_x-r, coin_y-r))
            
        pygame.draw.circle(screen, self.GOLD, (coin_x, coin_y), 15)
        pygame.draw.circle(screen, (200, 170, 0), (coin_x, coin_y), 12)
        
        # Draw count with shadow for better visibility
        count_text = self.coin_font.render(str(self.coins), True, self.BLACK)
        count_rect = count_text.get_rect(midleft=(coin_x + 25, coin_y))
        screen.blit(count_text, (count_rect.x+1, count_rect.y+1))  # Black shadow
        
        count_text = self.coin_font.render(str(self.coins), True, self.WHITE)
        screen.blit(count_text, count_rect)
        
        # Draw shop button with improved design
        shop_color = self.DARK_BLUE if self.hovered_button == 'shop_direct' else self.BLUE
        pygame.draw.rect(screen, (0, 50, 100), pygame.Rect(self.shop_button.left+2, self.shop_button.top+2, 
                                                       self.shop_button.width, self.shop_button.height), border_radius=5)
        pygame.draw.rect(screen, shop_color, self.shop_button, border_radius=5)
        
        plus_font = pygame.font.Font(None, 48)
        plus_text = plus_font.render("+", True, self.WHITE)
        plus_rect = plus_text.get_rect(center=self.shop_button.center)
        screen.blit(plus_text, plus_rect)
        
        # Store button for click detection
        self.buttons['shop_direct'] = self.shop_button
        
    def draw_particles(self, screen):
        """Draw particle effects"""
        for particle in self.particles:
            # Calculate alpha based on lifetime
            alpha = min(255, int(particle['lifetime'] * 2.55))
            
            # Create a surface with alpha
            particle_surf = pygame.Surface((int(particle['size']*2), int(particle['size']*2)), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, (*particle['color'], alpha), 
                              (int(particle['size']), int(particle['size'])), 
                              int(particle['size']))
            
            screen.blit(particle_surf, (int(particle['x'] - particle['size']), 
                                      int(particle['y'] - particle['size'])))
    
    def draw_floating_balls(self, screen):
        """Draw decorative floating balls in background"""
        for ball in self.floating_balls:
            # Create a surface with alpha for the ball
            ball_surf = pygame.Surface((ball['size']*2, ball['size']*2), pygame.SRCALPHA)
            pygame.draw.circle(ball_surf, (*ball['color'], ball['alpha']), 
                              (ball['size'], ball['size']), ball['size'])
            
            # Add a subtle glow
            pygame.draw.circle(ball_surf, (*ball['color'], ball['alpha']//3), 
                              (ball['size'], ball['size']), ball['size']+2)
            
            screen.blit(ball_surf, (int(ball['x'] - ball['size']), int(ball['y'] - ball['size'])))
            
    def draw(self, screen):
        """Draw the menu screen"""
        # Draw background
        self.draw_gradient_background(screen)
        
        # Draw floating balls in background (before other elements)
        self.draw_floating_balls(screen)
        
        # Draw title with animation
        title_color = self.WHITE if self.settings_manager.get_setting('dark_mode') else self.BLACK
        for i, (x, y, char) in enumerate(self.title_points):
            # Add animation to y position based on sine wave
            animated_y = y + math.sin(self.title_animation_time + i * 0.5) * 5
            
            # Draw shadow for 3D effect
            shadow_text = self.title_font.render(char, True, (0, 0, 0, 128))
            shadow_rect = shadow_text.get_rect(center=(x+3, animated_y+3))
            screen.blit(shadow_text, shadow_rect)
            
            # Draw main text
            text = self.title_font.render(char, True, title_color)
            rect = text.get_rect(center=(x, animated_y))
            screen.blit(text, rect)
            
        # Draw particles (after title)
        self.draw_particles(screen)
        
        # Draw subtitle
        subtitle_text = "The Ultimate Chance Game"
        subtitle_font = pygame.font.Font(None, 40)
        subtitle_color = self.WHITE if self.settings_manager.get_setting('dark_mode') else (50, 50, 50)
        subtitle = subtitle_font.render(subtitle_text, True, subtitle_color)
        subtitle_rect = subtitle.get_rect(center=(self.settings_manager.get_setting('width') // 2, 180))
        screen.blit(subtitle, subtitle_rect)
        
        # Draw buttons with improved style
        button_texts = {
            'start': 'Play Game',
            'settings': 'Settings',
            'shop': 'Shop',
            'quit': 'Quit'
        }
        
        # Draw buttons with drop shadow and hover effects
        for button_name, button_rect in self.buttons.items():
            if button_name not in ['shop_direct']:  # Skip special buttons
                self.draw_button(screen, button_name, button_rect, button_texts.get(button_name, ''), outline=True)
        
        # Draw money counter
        self.draw_money_counter(screen)
        
    def handle_click(self, pos):
        """Handle mouse clicks on buttons"""
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                # Play button click sound here if needed
                
                if button_name == 'start':
                    return self.on_start()
                elif button_name == 'settings':
                    return self.on_settings()
                elif button_name == 'shop' or button_name == 'shop_direct':
                    return self.on_shop()
                elif button_name == 'quit':
                    return self.on_quit()
                    
        return None  # No button clicked 