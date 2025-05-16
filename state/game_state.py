import time

class GameState:
    """Manages the game state across different screens"""
    
    def __init__(self):
        # Financial state
        self.coins = 0  # Starting with 0 coins instead of 100
        
        # Skins and items
        self.active_ball_skin = "default"  # Default ball skin
        self.purchased_skins = ["default"]  # Start with default skin
        
        # Special effects
        self.lucky_charm_active = False
        self.lucky_charm_end_time = 0
        
    def add_coins(self, amount):
        """Add coins to the player's balance"""
        self.coins = round(self.coins + amount, 2)
        return self.coins
        
    def subtract_coins(self, amount):
        """Subtract coins from the player's balance if possible"""
        if amount <= self.coins:
            self.coins = round(self.coins - amount, 2)
            return True
        return False
    
    def set_active_skin(self, skin_name):
        """Set the active ball skin"""
        if skin_name in self.purchased_skins:
            self.active_ball_skin = skin_name
            return True
        return False
        
    def purchase_skin(self, skin_name, cost):
        """Purchase a new skin if the player has enough coins"""
        if skin_name not in self.purchased_skins and self.subtract_coins(cost):
            self.purchased_skins.append(skin_name)
            return True
        return False
        
    def activate_lucky_charm(self, duration=1200):
        """Activate the lucky charm effect for the specified duration (seconds)"""
        self.lucky_charm_active = True
        self.lucky_charm_end_time = time.time() + duration
        
    def check_lucky_charm(self):
        """Check if the lucky charm is still active and return remaining time"""
        if self.lucky_charm_active:
            remaining = self.lucky_charm_end_time - time.time()
            if remaining <= 0:
                self.lucky_charm_active = False
                return 0
            return remaining
        return 0
        
    def get_lucky_charm_minutes_seconds(self):
        """Get the lucky charm remaining time in minutes:seconds format"""
        remaining = self.check_lucky_charm()
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        return minutes, seconds 