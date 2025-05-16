import pygame
import sys
from core.settings import SettingsManager
from ui.menu_screen import MenuScreen
from ui.settings_screen import SettingsScreen
from ui.shop_screen import ShopScreen
from ui.game_screen import GameScreen

class PlinkoGame:
    def __init__(self):
        pygame.init()
        
        # Game states
        self.MENU = "menu"
        self.PLAYING = "playing"
        self.SETTINGS = "settings"
        self.SHOP = "shop"
        
        # Initialize settings manager
        self.settings_manager = SettingsManager()
        
        # Set up display
        width, height = self.settings_manager.get_window_size()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Plinko Game")
        
        # Initialize coins
        self.coins = 100
        
        # Create game screens
        self.create_screens()
        
        # Set initial state
        self.current_state = self.MENU
        
        # Clock for framerate control
        self.clock = pygame.time.Clock()
        
    def create_screens(self):
        """Create all game screens"""
        self.screens = {
            self.MENU: MenuScreen(
                self.settings_manager,
                self.on_start_game,
                self.on_open_settings,
                self.on_open_shop,
                self.on_quit
            ),
            self.SETTINGS: SettingsScreen(
                self.settings_manager,
                self.on_back_to_menu
            ),
            self.SHOP: ShopScreen(
                self.settings_manager,
                self.on_back_to_menu,
                self.coins
            ),
            self.PLAYING: GameScreen(
                self.settings_manager,
                self.on_back_to_menu,
                self.on_open_shop
            )
        }
        
        # Set initial coins
        self.screens[self.MENU].coins = self.coins
        self.screens[self.PLAYING].coins = self.coins
        
    def update_screens(self):
        """Update screen properties that might have changed"""
        # Make sure all screens have the latest coin value
        for screen_name, screen in self.screens.items():
            if hasattr(screen, 'coins'):
                screen.coins = self.coins
            if hasattr(screen, 'update_coins'):
                screen.update_coins(self.coins)
                
    def on_start_game(self):
        """Handle start game action"""
        self.current_state = self.PLAYING
        
    def on_open_settings(self):
        """Handle open settings action"""
        self.current_state = self.SETTINGS
        
    def on_open_shop(self):
        """Handle open shop action"""
        # Make sure shop has current coins
        self.screens[self.SHOP].update_coins(self.coins)
        self.current_state = self.SHOP
        
    def on_back_to_menu(self):
        """Handle back to menu action"""
        self.current_state = self.MENU
        
    def on_quit(self):
        """Handle quit action"""
        pygame.quit()
        sys.exit()
        
    def process_events(self):
        """Process pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.on_quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Pass click to current screen
                pos = pygame.mouse.get_pos()
                result = self.screens[self.current_state].handle_click(pos)
                
                # Handle special results
                if isinstance(result, dict):
                    # Handle coin transactions
                    if 'add_coins' in result:
                        self.coins += result['add_coins']
                        self.update_screens()
                    elif 'purchase_item' in result:
                        self.coins -= result['cost']
                        # Process item purchase (would store in player inventory)
                        self.update_screens()
                elif result is not None:
                    # State change requested by screen
                    self.current_state = result
            elif event.type == pygame.MOUSEMOTION:
                # Update hover state
                pos = pygame.mouse.get_pos()
                self.screens[self.current_state].update_hover_state(pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_state != self.MENU:
                        self.current_state = self.MENU
                    else:
                        # Ask for confirmation before quitting
                        # For now, just quit directly
                        self.on_quit()
                        
    def run(self):
        """Main game loop"""
        running = True
        while running:
            # Process events
            self.process_events()
            
            # Update current screen
            self.screens[self.current_state].update()
            
            # Draw current screen
            self.screens[self.current_state].draw(self.screen)
            
            # Update display
            pygame.display.flip()
            
            # Cap framerate
            self.clock.tick(60) 