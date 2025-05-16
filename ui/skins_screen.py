import pygame
import random
from .base_screen import BaseScreen

class SkinsScreen(BaseScreen):
    def __init__(self, settings_manager, on_back, purchased_skins, active_skin, on_skin_selected):
        super().__init__(settings_manager)
        
        # Callback functions
        self.on_back = on_back
        self.on_skin_selected = on_skin_selected
        
        # Skins data
        self.purchased_skins = purchased_skins
        self.active_skin = active_skin
        
        # All available skins with their properties
        self.available_skins = {
            "default": {
                "name": "Default",
                "color": (170, 108, 57),  # Gold
                "description": "The classic gold Plinko ball."
            },
            "gold": {
                "name": "Gold Premium",
                "color": (255, 235, 0),  # Brighter gold
                "description": "A premium gold ball with enhanced shine."
            },
            "rainbow": {
                "name": "Rainbow",
                "color": None,  # Special handling for rainbow color
                "description": "A colorful ball that changes colors."
            }
        }
        
        # Preview animation variables
        self.preview_balls = []
        self.animation_timer = 0
        
        # Initialize the selected skin index
        self.selected_skin_index = 0
        
        # Create some preview balls for the currently selected skin
        self.create_preview_balls()
        
        # Initialize buttons and UI elements
        self.update_button_positions()
        
    def create_preview_balls(self):
        """Create some animated balls to preview the skin"""
        self.preview_balls = []
        width = self.settings_manager.get_setting('width')
        height = self.settings_manager.get_setting('height')
        
        center_x = width // 2
        center_y = height // 3
        
        # Create 5 preview balls
        for i in range(5):
            # Get current selected skin, not active skin
            current_skin_key = list(self.available_skins.keys())[self.selected_skin_index]
            color = self.get_skin_color(current_skin_key)
            
            # Create a ball with random position around the center
            angle = random.uniform(0, 6.28)  # Random angle (0-2π)
            distance = random.uniform(20, 80)  # Random distance from center
            x = center_x + distance * pygame.math.Vector2(1, 0).rotate_rad(angle).x
            y = center_y + distance * pygame.math.Vector2(1, 0).rotate_rad(angle).y
            
            # Random velocity
            dx = random.uniform(-1, 1)
            dy = random.uniform(-1, 1)
            
            self.preview_balls.append({
                "x": x,
                "y": y,
                "dx": dx,
                "dy": dy,
                "radius": random.uniform(8, 12),
                "color": color
            })
    
    def get_skin_color(self, skin_name):
        """Get the color for a skin, handling special cases like rainbow"""
        if skin_name == "rainbow":
            # Generate a random color for rainbow
            return (
                random.randint(150, 255),
                random.randint(150, 255),
                random.randint(150, 255)
            )
        else:
            # Get default color for the skin
            skin_data = self.available_skins.get(skin_name, self.available_skins["default"])
            return skin_data["color"]
    
    def update_button_positions(self):
        """Update button positions based on screen size"""
        width, height = self.settings_manager.get_window_size()
        
        # Navigation buttons
        self.buttons = {
            'back': pygame.Rect(20, 20, 100, 40),
            'prev_skin': pygame.Rect(width // 2 - 180, height // 2 + 80, 80, 40),
            'select_skin': pygame.Rect(width // 2 - 75, (height // 2)+30 + 50, 150, 40),
            'next_skin': pygame.Rect(width // 2 + 100, height // 2 + 80, 80, 40)
        }
    
    def update(self):
        """Update animations and state"""
        # Update animation timer
        self.animation_timer += 0.03
        
        # Update preview balls
        width = self.settings_manager.get_setting('width')
        height = self.settings_manager.get_setting('height')
        
        # Update all preview balls
        for ball in self.preview_balls:
            # Update position
            ball["x"] += ball["dx"]
            ball["y"] += ball["dy"]
            
            # Add a small spin effect
            ball["dx"] += pygame.math.Vector2(ball["dx"], ball["dy"]).rotate(90).normalize().x * 0.05
            ball["dy"] += pygame.math.Vector2(ball["dx"], ball["dy"]).rotate(90).normalize().y * 0.05
            
            # Limit velocity
            velocity = pygame.math.Vector2(ball["dx"], ball["dy"]).length()
            if velocity > 2:
                ball["dx"] *= 2 / velocity
                ball["dy"] *= 2 / velocity
            
            # Bounce off edges
            if ball["x"] - ball["radius"] < 0 or ball["x"] + ball["radius"] > width:
                ball["dx"] *= -0.9
            if ball["y"] - ball["radius"] < 0 or ball["y"] + ball["radius"] > height:
                ball["dy"] *= -0.9
            
            # Update rainbow colors continuously
            if self.active_skin == "rainbow":
                ball["color"] = self.get_skin_color("rainbow")
        
    def draw(self, screen):
        """Draw the skins screen"""
        # Draw background
        self.draw_gradient_background(screen)
        
        width = self.settings_manager.get_setting('width')
        height = self.settings_manager.get_setting('height')
        
        # Draw title
        title_color = self.WHITE if self.settings_manager.get_setting('dark_mode') else self.BLACK
        title = self.title_font.render("Ball Skins", True, title_color)
        title_rect = title.get_rect(center=(width // 2, 60))
        screen.blit(title, title_rect)
        
        # Draw back button
        self.draw_button(screen, 'back', self.buttons['back'], "Back")
        
        # Get the current skin in the selection
        available_skin_keys = list(self.available_skins.keys())
        current_skin_key = available_skin_keys[self.selected_skin_index % len(available_skin_keys)]
        current_skin = self.available_skins[current_skin_key]
        
        # Draw preview balls
        for ball in self.preview_balls:
            pygame.draw.circle(screen, ball["color"], (int(ball["x"]), int(ball["y"])), int(ball["radius"]))
            # Draw inner highlight for 3D effect
            inner_color = (255, 255, 255) if self.active_skin == "rainbow" else (220, 190, 0)
            pygame.draw.circle(screen, inner_color, (int(ball["x"] - ball["radius"]/5), 
                                                    int(ball["y"] - ball["radius"]/5)), 
                               int(ball["radius"]/3))
        
        # Draw skin name
        skin_name = current_skin["name"]
        name_text = self.title_font.render(skin_name, True, title_color)
        name_rect = name_text.get_rect(center=(width // 2, height // 2 - 20))
        screen.blit(name_text, name_rect)
        
        # Draw skin description
        desc_text = self.button_font.render(current_skin["description"], True, title_color)
        desc_rect = desc_text.get_rect(center=(width // 2, height // 2 + 20))
        screen.blit(desc_text, desc_rect)
        
        # Draw navigation buttons
        self.draw_button(screen, 'prev_skin', self.buttons['prev_skin'], "<")
        
        # Draw select button with different color if already active
        select_color = self.GREEN if current_skin_key == self.active_skin else self.BLUE
        select_text = "Selected" if current_skin_key == self.active_skin else "Select"
        
        # Check if skin is purchased
        if current_skin_key not in self.purchased_skins:
            select_color = self.GRAY
            select_text = "Locked"
            
        pygame.draw.rect(screen, select_color, self.buttons['select_skin'], border_radius=10)
        select_text_surf = self.button_font.render(select_text, True, self.WHITE)
        select_text_rect = select_text_surf.get_rect(center=self.buttons['select_skin'].center)
        screen.blit(select_text_surf, select_text_rect)
        
        self.draw_button(screen, 'next_skin', self.buttons['next_skin'], ">")
        
    def handle_click(self, pos):
        """Handle mouse clicks"""
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                if button_name == 'back':
                    return self.on_back()
                elif button_name == 'prev_skin':
                    # Just change the selected index, don't change the active skin yet
                    self.selected_skin_index = (self.selected_skin_index - 1) % len(self.available_skins)
                    # Update preview balls for the currently viewed skin (not active)
                    current_skin_key = list(self.available_skins.keys())[self.selected_skin_index]
                    self.update_preview_balls(current_skin_key)
                elif button_name == 'next_skin':
                    # Just change the selected index, don't change the active skin yet
                    self.selected_skin_index = (self.selected_skin_index + 1) % len(self.available_skins)
                    # Update preview balls for the currently viewed skin (not active)
                    current_skin_key = list(self.available_skins.keys())[self.selected_skin_index]
                    self.update_preview_balls(current_skin_key)
                elif button_name == 'select_skin':
                    # Get the current skin
                    current_skin_key = list(self.available_skins.keys())[self.selected_skin_index]
                    
                    # Check if skin is purchased
                    if current_skin_key in self.purchased_skins:
                        # Select this skin and update game state
                        self.active_skin = current_skin_key
                        self.on_skin_selected(current_skin_key)
                        
                return None  # Stay on this screen
                    
        return None  # No button clicked
        
    def update_preview_balls(self, skin_key):
        """Update preview balls to show the specified skin"""
        # Update all balls with the new skin color
        for ball in self.preview_balls:
            ball["color"] = self.get_skin_color(skin_key) 