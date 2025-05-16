import pygame
from ui.base_screen import BaseScreen

class ShopScreen(BaseScreen):
    def __init__(self, settings_manager, on_back, coins):
        super().__init__(settings_manager)
        
        # Callback function
        self.on_back = on_back
        
        # Player coins
        self.coins = coins
        
        # Available items
        self.items = [
            {"name": "100 Coins", "price": 0.99, "coins": 100, "id": "coins_100"},
            {"name": "500 Coins", "price": 3.99, "coins": 500, "id": "coins_500"},
            {"name": "1000 Coins", "price": 7.99, "coins": 1000, "id": "coins_1000"},
            {"name": "5000 Coins", "price": 34.99, "coins": 5000, "id": "coins_5000"},
            {"name": "Gold Ball", "price": 500, "id": "ball_gold", "description": "A shiny gold ball"},
            {"name": "Rainbow Ball", "price": 1000, "id": "ball_rainbow", "description": "Color-changing ball"},
            {"name": "Lucky Charm", "price": 2000, "id": "charm_luck", "description": "Slightly increases your odds"}
        ]
        
        # Shop state
        self.selected_item = None
        self.scroll_offset = 0
        self.max_scroll = max(0, len(self.items) - 3)  # Show 3 items at a time
        
        self.update_button_positions()
        
    def update_button_positions(self):
        """Update button positions based on screen size"""
        width = self.settings_manager.get_setting('width')
        height = self.settings_manager.get_setting('height')
        
        # Navigation buttons
        self.buttons = {
            'back': pygame.Rect(width // 2 - 100, height - 80, 200, 50),
            'scroll_up': pygame.Rect(width - 60, 160, 40, 40),
            'scroll_down': pygame.Rect(width - 60, height - 160, 40, 40)
        }
        
        # Item buttons
        item_width = 300
        item_height = 100
        item_spacing = 20
        start_y = 180
        
        # Clear previous item buttons
        for i in range(len(self.items)):
            if f'item_{i}' in self.buttons:
                del self.buttons[f'item_{i}']
                
        # Add visible item buttons
        for i in range(self.scroll_offset, min(self.scroll_offset + 3, len(self.items))):
            item_y = start_y + (i - self.scroll_offset) * (item_height + item_spacing)
            self.buttons[f'item_{i}'] = pygame.Rect(width // 2 - item_width // 2, item_y, item_width, item_height)
            
    def update_coins(self, coins):
        """Update coin balance"""
        self.coins = coins
        
    def draw(self, screen):
        """Draw the shop screen"""
        # Draw background
        self.draw_gradient_background(screen)
        
        # Draw title
        title_color = self.WHITE if self.settings_manager.get_setting('dark_mode') else self.BLACK
        title = self.title_font.render("Shop", True, title_color)
        title_rect = title.get_rect(center=(self.settings_manager.get_setting('width') // 2, 100))
        screen.blit(title, title_rect)
        
        # Draw coins
        width = self.settings_manager.get_setting('width')
        coin_bg = pygame.Rect(width - 170, 20, 150, 40)
        pygame.draw.rect(screen, (0, 50, 100), pygame.Rect(coin_bg.left+3, coin_bg.top+3, 
                                                           coin_bg.width, coin_bg.height), border_radius=10)
        pygame.draw.rect(screen, self.BLUE, coin_bg, border_radius=10)
        
        # Draw coin icon
        coin_x = coin_bg.left + 20
        coin_y = coin_bg.centery
        pygame.draw.circle(screen, self.GOLD, (coin_x, coin_y), 15)
        pygame.draw.circle(screen, (200, 170, 0), (coin_x, coin_y), 12)
        
        # Draw coin amount
        coin_text = self.coin_font.render(str(self.coins), True, self.WHITE)
        coin_rect = coin_text.get_rect(midleft=(coin_x + 20, coin_y))
        screen.blit(coin_text, coin_rect)
        
        # Draw scroll buttons if needed
        if self.max_scroll > 0:
            self.draw_button(screen, 'scroll_up', self.buttons['scroll_up'], "▲")
            self.draw_button(screen, 'scroll_down', self.buttons['scroll_down'], "▼")
            
        # Draw items
        for i in range(self.scroll_offset, min(self.scroll_offset + 3, len(self.items))):
            item = self.items[i]
            button_name = f'item_{i}'
            
            # Draw item button with special coloring if selected
            color = self.DARK_BLUE if self.hovered_button == button_name else self.BLUE
            if self.selected_item == i:
                color = (0, 150, 0)  # Green when selected
                
            # Draw item shadow
            shadow_rect = pygame.Rect(self.buttons[button_name].left + 3, self.buttons[button_name].top + 3,
                                      self.buttons[button_name].width, self.buttons[button_name].height)
            pygame.draw.rect(screen, (0, 50, 100), shadow_rect, border_radius=10)
            
            # Draw item background
            pygame.draw.rect(screen, color, self.buttons[button_name], border_radius=10)
            
            # Draw item border
            pygame.draw.rect(screen, self.WHITE, self.buttons[button_name], border_radius=10, width=2)
            
            # Draw item name
            name_text = self.button_font.render(item["name"], True, self.WHITE)
            name_rect = name_text.get_rect(midtop=(self.buttons[button_name].centerx, self.buttons[button_name].top + 15))
            screen.blit(name_text, name_rect)
            
            # Draw price or description
            if "coins" in item:  # Coin purchase
                price_text = self.button_font.render(f"${item['price']:.2f}", True, self.GOLD)
                price_rect = price_text.get_rect(midbottom=(self.buttons[button_name].centerx, self.buttons[button_name].bottom - 15))
                screen.blit(price_text, price_rect)
            else:  # Item purchase
                price_text = self.button_font.render(f"{item['price']} coins", True, self.GOLD)
                price_rect = price_text.get_rect(midbottom=(self.buttons[button_name].centerx, self.buttons[button_name].bottom - 15))
                screen.blit(price_text, price_rect)
                
                if "description" in item:
                    desc_text = pygame.font.Font(None, 24).render(item["description"], True, self.WHITE)
                    desc_rect = desc_text.get_rect(midtop=(self.buttons[button_name].centerx, name_rect.bottom + 5))
                    screen.blit(desc_text, desc_rect)
        
        # Draw back button
        self.draw_button(screen, 'back', self.buttons['back'], "Back")
        
    def handle_click(self, pos):
        """Handle mouse clicks on shop elements"""
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                if button_name == 'back':
                    return self.on_back()
                elif button_name == 'scroll_up' and self.scroll_offset > 0:
                    self.scroll_offset -= 1
                    self.update_button_positions()
                elif button_name == 'scroll_down' and self.scroll_offset < self.max_scroll:
                    self.scroll_offset += 1
                    self.update_button_positions()
                elif button_name.startswith('item_'):
                    item_index = int(button_name.split('_')[1])
                    item = self.items[item_index]
                    
                    # Handle item selection or purchase
                    if "coins" in item:  # Real money purchase
                        # Here we would launch a payment processor
                        # For now, let's just add the coins (simulate purchase)
                        self.coins += item["coins"]
                        # Return None as we don't want to change the state
                        return {"add_coins": item["coins"]}
                    elif self.coins >= item["price"]:  # In-game purchase
                        # Process item purchase
                        self.coins -= item["price"]
                        # Return None as we don't want to change the state
                        return {"purchase_item": item["id"], "cost": item["price"]}
                        
        return None  # No state change 