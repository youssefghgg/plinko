import pygame
import math
import random

class Ball:
    def __init__(self, x, y, radius, color, bet_amount):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dx = random.uniform(-0.3, 0.3)  # Start with small random horizontal movement
        self.dy = 0
        self.bet_amount = bet_amount  # Store bet amount with the ball
        self.active = True
        self.last_collision_time = 0  # Prevent multiple collisions with same pin

    def draw(self, screen):
        """Draw the ball on the screen"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Draw a slightly smaller inner circle for 3D effect
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
            
        pygame.draw.circle(screen, inner_color, (int(self.x), int(self.y)), self.radius - 2)

    def update(self, pin_positions, boundaries, multipliers, multiplier_rects, on_win_callback):
        """Update ball position and handle collisions"""
        gravity = 0.35  # Reduced gravity for slower fall
        bounce_damping = 0.65  # Reduced for less bouncy balls
        pin_radius = 5
        collision_cooldown = 3  # Reduced collision cooldown
        
        # Update velocity with gravity
        self.dy += gravity
        
        # Cap maximum vertical speed to prevent clipping through pins
        max_vertical_speed = 6
        if self.dy > max_vertical_speed:
            self.dy = max_vertical_speed
            
        # Calculate intended new position
        intended_x = self.x + self.dx
        intended_y = self.y + self.dy
        
        # Check for pin collisions at intended position before moving
        collision_occurred = False
        for pin_x, pin_y in pin_positions:
            dx = intended_x - pin_x
            dy = intended_y - pin_y
            distance = math.sqrt(dx * dx + dy * dy)
            min_distance = self.radius + pin_radius
            
            # Pre-emptive collision detection to prevent clipping
            if distance < min_distance and self.last_collision_time > collision_cooldown:
                collision_occurred = True
                self.last_collision_time = 0
                
                # Calculate normal vector from pin to ball
                nx = dx / max(distance, 0.1)  # Avoid division by zero
                ny = dy / max(distance, 0.1)
                
                # Move out of collision
                overlap = min_distance - distance
                intended_x += nx * overlap * 1.05  # Slightly higher to prevent sticking
                intended_y += ny * overlap * 1.05
                
                # Calculate new velocities based on bounce
                dot_product = self.dx * nx + self.dy * ny
                self.dx -= 2 * dot_product * nx * bounce_damping
                self.dy -= 2 * dot_product * ny * bounce_damping
                
                # Add very minimal random deflection (significantly reduced)
                random_deflection = random.uniform(-0.15, 0.15)  # Reduced from -0.4, 0.4
                self.dx += random_deflection
                
        # Update position after potential collision corrections
        self.x = intended_x
        self.y = intended_y
        
        # Add extremely subtle center bias - barely noticeable
        center_x = (boundaries['left'] + boundaries['right']) / 2
        distance_from_center = self.x - center_x
        
        # Make bias stronger when further from center, weaker when near center
        distance_factor = min(1.0, abs(distance_from_center) / 100)  # Scale with distance
        center_force = -distance_from_center * 0.0003 * distance_factor  # Drastically reduced from 0.0008
        
        # Very subtle middle-biased physics
        self.dx += center_force
        
        # Check for boundary collisions
        if self.x - self.radius < boundaries['left']:
            self.x = boundaries['left'] + self.radius
            self.dx = abs(self.dx) * 0.7  # Reduced rebound
        elif self.x + self.radius > boundaries['right']:
            self.x = boundaries['right'] - self.radius
            self.dx = -abs(self.dx) * 0.7  # Reduced rebound
            
        # Add a tiny amount of randomness
        self.dx += random.uniform(-0.01, 0.01)  # Further reduced randomness (from -0.02, 0.02)
        
        # Increment collision cooldown if no collision occurred
        if not collision_occurred:
            self.last_collision_time += 1
                    
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