import pygame
import random

class Ball:
    """Ball object that bounces through the pins"""
    
    def __init__(self, x, y, radius, color, bet_amount):
        # Position and size
        self.x = x
        self.y = y
        self.radius = radius
        
        # Appearance
        self.color = color
        
        # Physics properties
        self.dx = random.uniform(-0.3, 0.3)  # Initial horizontal movement
        self.dy = 0  # Initial vertical movement
        
        # Game properties
        self.bet_amount = bet_amount
        self.active = True
        self.last_collision_time = 0  # For collision cooldown
        self.collision_flash = 0  # For visual collision feedback

    def draw(self, screen):
        """Draw the ball on the screen"""
        # Determine if we should show collision flash
        flash_active = hasattr(self, 'collision_flash') and self.collision_flash > 0
        
        # Draw outer circle with glow effect if flashing
        if flash_active:
            # Add a subtle glow for impact
            glow_radius = self.radius + 3
            glow_alpha = min(150, self.collision_flash * 15)
            glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            glow_color = (255, 255, 200, glow_alpha)
            pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), glow_radius)
            screen.blit(glow_surface, (int(self.x - glow_radius), int(self.y - glow_radius)))
        
        # Draw outer circle
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Create inner color (slightly darker version of the ball color)
        inner_color = self.color
        
        # For gold colors, make inner color slightly darker
        if self.color == (255, 215, 0):  # If it's gold
            inner_color = (200, 170, 0)
        elif isinstance(self.color, tuple) and len(self.color) == 3:
            # For other colors, create a slightly darker shade
            r = max(0, self.color[0] - 40)
            g = max(0, self.color[1] - 40)
            b = max(0, self.color[2] - 40)
            inner_color = (r, g, b)
            
        # Draw inner circle for 3D effect
        pygame.draw.circle(screen, inner_color, (int(self.x), int(self.y)), self.radius - 2)
        
        # Add highlight for more realistic look
        highlight_pos = (int(self.x - self.radius * 0.3), int(self.y - self.radius * 0.3))
        highlight_radius = int(self.radius * 0.4)
        highlight_color = (255, 255, 255, 50)  # Semi-transparent white
        
        # Create a surface for the semi-transparent highlight
        highlight_surface = pygame.Surface((highlight_radius*2, highlight_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(highlight_surface, highlight_color, (highlight_radius, highlight_radius), highlight_radius)
        
        # Blit the highlight onto the screen
        screen.blit(highlight_surface, (highlight_pos[0] - highlight_radius, highlight_pos[1] - highlight_radius))

    def check_multiplier_collision(self, multipliers, multiplier_rects, on_win_callback):
        """Check if ball has reached a multiplier zone and trigger win callback"""
        if not self.active:
            return False
            
        for i, rect in enumerate(multiplier_rects):
            if rect.collidepoint((self.x, self.y)):
                multiplier = multipliers[i]
                winnings = round(self.bet_amount * multiplier, 2)
                on_win_callback(winnings)
                self.active = False
                return True
        return False
    
    def is_out_of_bounds(self, bottom_boundary):
        """Check if the ball is below the screen boundary"""
        return self.y > bottom_boundary


class Pin:
    """Pin object that balls bounce off of"""
    
    def __init__(self, x, y, radius=5):
        self.x = x
        self.y = y
        self.radius = radius
        
    def draw(self, screen):
        """Draw the pin on the screen"""
        WHITE = (255, 255, 255)
        GRAY = (128, 128, 128)
        
        # Draw outer white circle
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)
        
        # Draw inner gray circle for 3D effect
        pygame.draw.circle(screen, GRAY, (self.x, self.y), self.radius - 2) 