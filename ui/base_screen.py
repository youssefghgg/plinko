import pygame

class BaseScreen:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.hovered_button = None
        self.buttons = {}
        
        # Common colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 255)
        self.DARK_BLUE = (0, 70, 178)
        self.GREEN = (0, 180, 0)
        self.RED = (255, 0, 0)
        self.GRAY = (128, 128, 128)
        self.GOLD = (255, 215, 0)
        
        # Common fonts
        self.title_font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 36)
        self.coin_font = pygame.font.Font(None, 40)
        
    def update_button_positions(self):
        """Update button positions based on screen size"""
        pass
        
    def draw_button(self, screen, button_name, button_rect, text, outline=False):
        """Draw a button with text"""
        color = self.DARK_BLUE if self.hovered_button == button_name else self.BLUE
        
        # Draw button shadow (3D effect)
        shadow_rect = pygame.Rect(button_rect.left + 3, button_rect.top + 3, 
                                  button_rect.width, button_rect.height)
        pygame.draw.rect(screen, (0, 50, 100), shadow_rect, border_radius=10)
        
        # Draw main button
        pygame.draw.rect(screen, color, button_rect, border_radius=10)
        
        if outline:
            # Draw outline
            pygame.draw.rect(screen, self.WHITE, button_rect, border_radius=10, width=2)
            
        # Draw button text
        text_surface = self.button_font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
        
        # Store button for click detection
        self.buttons[button_name] = button_rect
        
    def draw_gradient_background(self, screen):
        """Draw a gradient background based on dark mode setting"""
        height = self.settings_manager.get_setting('height')
        width = self.settings_manager.get_setting('width')
        
        if self.settings_manager.get_setting('dark_mode'):
            for y in range(height):
                r = int(25 + (y / height) * 20)
                g = int(25 + (y / height) * 20)
                b = int(45 + (y / height) * 20)
                pygame.draw.line(screen, (r, g, b), (0, y), (width, y))
        else:
            for y in range(height):
                r = int(100 + (y / height) * 155)
                g = int(150 + (y / height) * 105)
                b = int(255 - (y / height) * 105)
                pygame.draw.line(screen, (r, g, b), (0, y), (width, y))
                
    def update_hover_state(self, pos):
        """Update which button is being hovered"""
        self.hovered_button = None
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                self.hovered_button = button_name
                break
                
    def handle_click(self, pos):
        """Handle mouse clicks on buttons"""
        pass
        
    def draw(self, screen):
        """Draw the screen"""
        pass
        
    def update(self):
        """Update screen state"""
        pass 