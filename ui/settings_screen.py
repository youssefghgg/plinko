import pygame
from .base_screen import BaseScreen

class SettingsScreen(BaseScreen):
    def __init__(self, settings_manager, on_back):
        super().__init__(settings_manager)
        
        # Callback function
        self.on_back = on_back
        
        # Window size options
        self.window_sizes = ["800x600", "1024x768", "1280x720"]
        
        # Initialize selected size index
        width = self.settings_manager.get_setting('width')
        height = self.settings_manager.get_setting('height')
        current_size = f"{width}x{height}"
        
        try:
            self.selected_size_index = self.window_sizes.index(current_size)
        except ValueError:
            # If current size is not in the list, default to first size
            self.selected_size_index = 0
            
        self.update_button_positions()
        
    def update_button_positions(self):
        """Update button positions based on screen size"""
        width = self.settings_manager.get_setting('width')
        height = self.settings_manager.get_setting('height')
        
        # Settings buttons
        self.buttons = {
            'size_left': pygame.Rect(width // 2 - 150, 200, 30, 30),
            'size_right': pygame.Rect(width // 2 + 120, 200, 30, 30),
            'dark_mode': pygame.Rect(width // 2 - 100, 300, 200, 50),
            'volume_down': pygame.Rect(width // 2 - 150, 400, 30, 30),
            'volume_up': pygame.Rect(width // 2 + 120, 400, 30, 30),
            'back': pygame.Rect(width // 2 - 100, 500, 200, 50)
        }
        
    def apply_window_size(self, size_str):
        """Apply the selected window size"""
        width, height = map(int, size_str.split('x'))
        self.settings_manager.set_window_size(width, height)
        
        # Resize the display
        pygame.display.set_mode((width, height))
        
        # Update button positions for new size
        self.update_button_positions()
        
    def draw(self, screen):
        """Draw the settings screen"""
        # Draw background
        self.draw_gradient_background(screen)
        
        # Draw title
        title_color = self.WHITE if self.settings_manager.get_setting('dark_mode') else self.BLACK
        title = self.title_font.render("Settings", True, title_color)
        title_rect = title.get_rect(center=(self.settings_manager.get_setting('width') // 2, 100))
        screen.blit(title, title_rect)
        
        # Draw window size selector
        text_color = self.WHITE if self.settings_manager.get_setting('dark_mode') else self.BLACK
        size_text = self.button_font.render("Window Size:", True, text_color)
        size_rect = size_text.get_rect(center=(self.settings_manager.get_setting('width') // 2, 170))
        screen.blit(size_text, size_rect)
        
        # Draw arrow buttons
        self.draw_button(screen, 'size_left', self.buttons['size_left'], "<")
        self.draw_button(screen, 'size_right', self.buttons['size_right'], ">")
        
        # Draw current size
        current_size = self.window_sizes[self.selected_size_index]
        size_value = self.button_font.render(current_size, True, text_color)
        size_value_rect = size_value.get_rect(center=(self.settings_manager.get_setting('width') // 2, 215))
        screen.blit(size_value, size_value_rect)
        
        # Draw dark mode toggle
        dark_mode = self.settings_manager.get_setting('dark_mode')
        dark_mode_text = f"Dark Mode: {'On' if dark_mode else 'Off'}"
        self.draw_button(screen, 'dark_mode', self.buttons['dark_mode'], dark_mode_text)
        
        # Draw volume control
        volume_text = self.button_font.render("Volume:", True, text_color)
        volume_rect = volume_text.get_rect(center=(self.settings_manager.get_setting('width') // 2, 370))
        screen.blit(volume_text, volume_rect)
        
        # Draw volume buttons
        self.draw_button(screen, 'volume_down', self.buttons['volume_down'], "-")
        self.draw_button(screen, 'volume_up', self.buttons['volume_up'], "+")
        
        # Draw volume level
        volume = self.settings_manager.get_setting('volume', 0.5)
        volume_percent = int(volume * 100)
        volume_value = self.button_font.render(f"{volume_percent}%", True, text_color)
        volume_value_rect = volume_value.get_rect(center=(self.settings_manager.get_setting('width') // 2, 415))
        screen.blit(volume_value, volume_value_rect)
        
        # Draw visual volume bar
        bar_width = 200
        bar_height = 20
        bar_x = self.settings_manager.get_setting('width') // 2 - bar_width // 2
        bar_y = 450
        
        # Draw background bar
        pygame.draw.rect(screen, self.GRAY, pygame.Rect(bar_x, bar_y, bar_width, bar_height), border_radius=5)
        
        # Draw filled portion
        filled_width = int(bar_width * volume)
        pygame.draw.rect(screen, self.BLUE, pygame.Rect(bar_x, bar_y, filled_width, bar_height), border_radius=5)
        
        # Draw back button
        self.draw_button(screen, 'back', self.buttons['back'], "Back")
        
    def handle_click(self, pos):
        """Handle mouse clicks on settings buttons"""
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                if button_name == 'back':
                    return self.on_back()
                elif button_name == 'dark_mode':
                    self.settings_manager.toggle_dark_mode()
                elif button_name == 'size_left':
                    self.selected_size_index = (self.selected_size_index - 1) % len(self.window_sizes)
                    self.apply_window_size(self.window_sizes[self.selected_size_index])
                elif button_name == 'size_right':
                    self.selected_size_index = (self.selected_size_index + 1) % len(self.window_sizes)
                    self.apply_window_size(self.window_sizes[self.selected_size_index])
                elif button_name == 'volume_down':
                    volume = max(0, self.settings_manager.get_setting('volume', 0.5) - 0.1)
                    self.settings_manager.set_setting('volume', round(volume, 1))
                elif button_name == 'volume_up':
                    volume = min(1.0, self.settings_manager.get_setting('volume', 0.5) + 0.1)
                    self.settings_manager.set_setting('volume', round(volume, 1))
                    
        return None  # No state change 