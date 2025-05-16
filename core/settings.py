import json
import os

class SettingsManager:
    def __init__(self):
        self.settings = self.load_settings()
        
    def load_settings(self):
        """Load settings from file or create default settings"""
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Default settings
            default_settings = {
                'width': 800,
                'height': 600,
                'dark_mode': False,
                'volume': 0.5,
                'fullscreen': False
            }
            self.save_settings(default_settings)
            return default_settings
            
    def save_settings(self, settings=None):
        """Save settings to file"""
        if settings is None:
            settings = self.settings
        else:
            self.settings = settings
            
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
            
    def get_setting(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
        
    def set_setting(self, key, value):
        """Set a setting value and save"""
        self.settings[key] = value
        self.save_settings()
        
    def toggle_dark_mode(self):
        """Toggle dark mode setting"""
        self.settings['dark_mode'] = not self.settings['dark_mode']
        self.save_settings()
        
    def set_window_size(self, width, height):
        """Set window size and save settings"""
        self.settings['width'] = width
        self.settings['height'] = height
        self.save_settings()
        
    def get_window_size(self):
        """Get current window size"""
        return (self.settings['width'], self.settings['height']) 