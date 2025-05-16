import pygame
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

    def draw(self, screen):
        """Draw the ball on the screen"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Draw a slightly smaller inner circle for 3D effect
        pygame.draw.circle(screen, (200, 170, 0), (int(self.x), int(self.y)), self.radius - 2)

    def update(self, pin_positions, boundaries, multipliers, multiplier_rects, on_win_callback):
        """Update ball position and handle collisions"""
        gravity = 0.5
        bounce_damping = 0.65
        pin_radius = 5
        
        # Update velocity with gravity
        self.dy += gravity
        
        # Update position
        self.x += self.dx
        self.y += self.dy
        
        # Add subtle center bias (improves gameplay)
        center_x = boundaries['right'] / 2
        distance_from_center = self.x - center_x
        center_force = -distance_from_center * 0.002
        self.dx += center_force
        
        # Check for boundary collisions
        if self.x - self.radius < boundaries['left']:
            self.x = boundaries['left'] + self.radius
            self.dx = abs(self.dx) * 0.6
        elif self.x + self.radius > boundaries['right']:
            self.x = boundaries['right'] - self.radius
            self.dx = -abs(self.dx) * 0.6
            
        # Check for pin collisions
        for pin_x, pin_y in pin_positions:
            dx = self.x - pin_x
            dy = self.y - pin_y
            distance = math.sqrt(dx * dx + dy * dy)
            min_distance = self.radius + pin_radius
            
            if distance < min_distance:
                # Calculate normal vector from pin to ball
                nx = dx / distance
                ny = dy / distance
                
                # Move ball out of pin
                overlap = min_distance - distance
                self.x += nx * overlap
                self.y += ny * overlap
                
                # Calculate relative velocity
                relative_velocity_x = self.dx
                relative_velocity_y = self.dy
                
                # Calculate impulse with slightly increased bounce
                velocity_dot_normal = (relative_velocity_x * nx + relative_velocity_y * ny)
                impulse = 1.6 * velocity_dot_normal
                self.dx -= impulse * nx * bounce_damping
                self.dy -= impulse * ny * bounce_damping
                
                # Add slightly random deflection with center bias
                random_deflection = (random.random() - 0.5) * 0.35
                if self.x < center_x:
                    random_deflection = abs(random_deflection) * 0.7  # Bias towards right
                else:
                    random_deflection = -abs(random_deflection) * 0.7  # Bias towards left
                self.dx += random_deflection
                
                # Ensure minimum velocity after bounce
                min_velocity = 1.6
                velocity = math.sqrt(self.dx * self.dx + self.dy * self.dy)
                if velocity < min_velocity:
                    scale = min_velocity / velocity
                    self.dx *= scale
                    self.dy *= scale
                    
        # Check if ball has reached multiplier zone
        if self.active:
            for i, rect in enumerate(multiplier_rects):
                if rect.collidepoint((self.x, self.y)):
                    multiplier = multipliers[i]
                    winnings = round(self.bet_amount * multiplier, 2)
                    on_win_callback(winnings)
                    self.active = False
                    break
                    
        # Return True if ball is off screen and should be removed
        return self.y > boundaries['bottom'] or not self.active

class Pin:
    def __init__(self, x, y, radius=5):
        self.x = x
        self.y = y
        self.radius = radius
        
    def draw(self, screen):
        """Draw the pin on the screen"""
        WHITE = (255, 255, 255)
        GRAY = (128, 128, 128)
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)
        # Draw a slightly smaller inner circle for 3D effect
        pygame.draw.circle(screen, GRAY, (self.x, self.y), self.radius - 2) 