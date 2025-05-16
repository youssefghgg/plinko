import pygame
import sys
from core.settings import SettingsManager
from state.game_state import GameState
from ui.menu_screen import MenuScreen
from ui_components.game_screen import GameScreen
from ui.shop_screen import ShopScreen

class PlinkoGame:
    """Main game class that manages screens and game flow"""
    
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Initialize settings
        self.settings_manager = SettingsManager()
        self.width = self.settings_manager.get_setting('width')
        self.height = self.settings_manager.get_setting('height')
        
        # Create screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Plinko")
        
        # Set up the clock
        self.clock = pygame.time.Clock()
        
        # Initialize game state
        self.game_state = GameState()
        
        # Current screen
        self.current_screen = None
        self.show_menu()
    
    def show_menu(self):
        """Show the main menu screen"""
        self.current_screen = MenuScreen(
            self.settings_manager,
            on_start=self.start_game,
            on_settings=self.show_settings,
            on_shop=self.show_shop,
            on_quit=self.quit_game,
            on_skins=self.show_skins
        )
        
    def start_game(self):
        """Start the game"""
        self.current_screen = GameScreen(
            self.settings_manager, 
            self.game_state,
            on_back=self.show_menu, 
            on_shop=self.show_shop
        )
    
    def show_settings(self):
        """Show settings screen"""
        from ui.settings_screen import SettingsScreen
        self.current_screen = SettingsScreen(self.settings_manager, on_back=self.show_menu)
    
    def show_shop(self):
        """Show shop screen"""
        self.current_screen = ShopScreen(
            self.settings_manager, 
            on_back=self.show_menu, 
            coins=self.game_state.coins,
            purchased_skins=self.game_state.purchased_skins
        )
    
    def show_skins(self):
        """Show skins selection screen"""
        from ui.skins_screen import SkinsScreen
        self.current_screen = SkinsScreen(
            self.settings_manager,
            on_back=self.show_menu,
            purchased_skins=self.game_state.purchased_skins,
            active_skin=self.game_state.active_ball_skin,
            on_skin_selected=self.set_active_skin
        )
    
    def set_active_skin(self, skin_name):
        """Set the active ball skin"""
        self.game_state.set_active_skin(skin_name)
    
    def quit_game(self):
        """Quit the game"""
        pygame.quit()
        sys.exit()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    if self.current_screen and hasattr(self.current_screen, 'update_hover_state'):
                        self.current_screen.update_hover_state(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_screen and hasattr(self.current_screen, 'handle_click'):
                        result = self.current_screen.handle_click(event.pos)
                        
                        if result and not isinstance(result, bool):
                            # Process shop purchases
                            if isinstance(result, dict):
                                # Handle coin purchases
                                if "add_coins" in result:
                                    self.game_state.add_coins(result["add_coins"])
                                    
                                # Handle item purchases
                                if "purchase_item" in result:
                                    # Process the purchase in game state
                                    if "effect" in result:
                                        if result["effect"] == "change_skin" and "skin" in result:
                                            # Purchase a new skin
                                            self.game_state.purchase_skin(result["skin"], result["cost"])
                                        elif result["effect"] == "lucky_charm" and "duration" in result:
                                            # Activate lucky charm
                                            self.game_state.subtract_coins(result["cost"])
                                            self.game_state.activate_lucky_charm(result["duration"])
                                
                                # Refresh the current screen with updated game state
                                if isinstance(self.current_screen, ShopScreen):
                                    self.current_screen.update_coins(self.game_state.coins)
                                    self.current_screen.purchased_skins = self.game_state.purchased_skins
                            # If a screen object is returned, switch to it
                            elif hasattr(result, 'draw'):
                                self.current_screen = result
            
            # Update
            if self.current_screen and hasattr(self.current_screen, 'update'):
                self.current_screen.update()
            
            # Render
            self.screen.fill((0, 0, 0))  # Clear screen
            if self.current_screen and hasattr(self.current_screen, 'draw'):
                self.current_screen.draw(self.screen)
            
            # Flip display
            pygame.display.flip()
            
            # Cap the frame rate
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PlinkoGame()
    game.run() 