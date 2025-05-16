import random
import math

class BallPhysics:
    """Handles the physics calculations for balls in the Plinko game"""
    
    def __init__(self):
        # Physics constants
        self.gravity = 0.3  # Slightly reduced gravity for better control
        self.bounce_damping = 0.7  # More bouncy
        self.max_vertical_speed = 5.5  # Slightly lower max speed
        self.collision_cooldown = 3
        self.elasticity = 0.75  # Elasticity of collisions
        
    def update_position(self, ball, pin_positions, boundaries, pin_radius=5):
        """Update ball position and handle collisions with pins and boundaries"""
        # Store original state to check if a collision occurred
        collision_occurred = False
        
        # Apply gravity with subtle randomness (simulates air resistance)
        gravity_jitter = random.uniform(-0.02, 0.02)
        ball.dy += self.gravity + gravity_jitter
        
        # Cap maximum vertical speed
        if ball.dy > self.max_vertical_speed:
            ball.dy = self.max_vertical_speed
        
        # Add subtle horizontal drag
        if abs(ball.dx) > 0.1:
            ball.dx *= 0.99
            
        # Calculate intended new position
        intended_x = ball.x + ball.dx
        intended_y = ball.y + ball.dy
        
        # Check for pin collisions before moving
        for pin_x, pin_y in pin_positions:
            dx = intended_x - pin_x
            dy = intended_y - pin_y
            distance = math.sqrt(dx * dx + dy * dy)
            min_distance = ball.radius + pin_radius
            
            # Pre-emptive collision detection to prevent clipping
            if distance < min_distance and ball.last_collision_time > self.collision_cooldown:
                collision_occurred = True
                ball.last_collision_time = 0
                
                # Calculate normal vector from pin to ball
                nx = dx / max(distance, 0.1)  # Avoid division by zero
                ny = dy / max(distance, 0.1)
                
                # Calculate impact velocity
                impact_velocity = math.sqrt(ball.dx * ball.dx + ball.dy * ball.dy)
                
                # Move out of collision
                overlap = min_distance - distance
                intended_x += nx * overlap * 1.05  # Slightly higher to prevent sticking
                intended_y += ny * overlap * 1.05
                
                # Calculate new velocities based on bounce
                dot_product = ball.dx * nx + ball.dy * ny
                ball.dx -= 2 * dot_product * nx * self.bounce_damping
                ball.dy -= 2 * dot_product * ny * self.bounce_damping
                
                # Add impact-based random deflection (harder impacts have more randomness)
                deflection_scale = min(0.3, impact_velocity * 0.04)
                random_deflection = random.uniform(-deflection_scale, deflection_scale)
                ball.dx += random_deflection
                
                # Add visual feedback for collisions
                ball.collision_flash = 10  # Frames of collision visual feedback
        
        # Update ball position
        ball.x = intended_x
        ball.y = intended_y
        
        # Apply extremely subtle center bias (increases with distance from center)
        center_x = (boundaries['left'] + boundaries['right']) / 2
        distance_from_center = ball.x - center_x
        
        # Make bias stronger when further from center, weaker when near center
        distance_factor = min(1.0, abs(distance_from_center) / 100)
        center_force = -distance_from_center * 0.0004 * distance_factor
        ball.dx += center_force
        
        # Check for boundary collisions with proper bounce physics
        if ball.x - ball.radius < boundaries['left']:
            # Left wall collision
            ball.x = boundaries['left'] + ball.radius
            ball.dx = abs(ball.dx) * self.elasticity
            collision_occurred = True
            ball.collision_flash = 5  # Shorter flash for wall collisions
        elif ball.x + ball.radius > boundaries['right']:
            # Right wall collision
            ball.x = boundaries['right'] - ball.radius
            ball.dx = -abs(ball.dx) * self.elasticity
            collision_occurred = True
            ball.collision_flash = 5  # Shorter flash for wall collisions
            
        # Add a tiny amount of randomness for natural-looking motion
        ball.dx += random.uniform(-0.01, 0.01)
        
        # Update collision cooldown
        if not collision_occurred:
            ball.last_collision_time += 1
            
        # Update collision flash (for visual feedback)
        if hasattr(ball, 'collision_flash') and ball.collision_flash > 0:
            ball.collision_flash -= 1
            
        return collision_occurred 