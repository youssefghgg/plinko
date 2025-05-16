import pygame
from ui.base_screen import BaseScreen

class Dashboard:
    def __init__(self, settings_manager, on_drop_ball, coins):
        self.settings_manager = settings_manager
        self.on_drop_ball = on_drop_ball
        self.coins = coins
        self.amount = 0.0  # Bet amount
        
        # Dashboard state
        self.dashboard_width = 200
        self.dashboard_extended = False
        self.dashboard_x = -self.dashboard_width
        self.dashboard_buttons = {}
        self.hovered_button = None
        
        # Risk options and state
        self.risks = ["Easy (2%)", "Medium (15%)", "Hard (40%)"]
        self.selected_risk = 0
        self.is_dropdown_open = False
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 255)
        self.DARK_BLUE = (0, 70, 178)
        self.GOLD = (255, 215, 0)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 28)
        
    def update(self):
        """Update dashboard animation"""
        target_x = 0 if self.dashboard_extended else -self.dashboard_width
        self.dashboard_x += (target_x - self.dashboard_x) * 0.2
        
    def update_coins(self, coins):
        """Update coin balance"""
        self.coins = coins
        
    def draw(self, screen):
        """Draw the dashboard"""
        # Draw dashboard background with shadow
        shadow_rect = pygame.Rect(self.dashboard_x + 3, 3, self.dashboard_width, self.settings_manager.get_setting('height'))
        pygame.draw.rect(screen, (0, 20, 60), shadow_rect)
        
        dashboard_rect = pygame.Rect(self.dashboard_x, 0, self.dashboard_width, self.settings_manager.get_setting('height'))
        pygame.draw.rect(screen, self.DARK_BLUE, dashboard_rect)
        
        # Draw toggle button
        toggle_button = pygame.Rect(self.dashboard_x + self.dashboard_width,
                                    self.settings_manager.get_setting('height') // 2 - 50, 20, 100)
        pygame.draw.rect(screen,
                        (0, 50, 150) if self.hovered_button == 'toggle' else self.BLUE,
                        toggle_button, border_radius=5)
        pygame.draw.polygon(screen, self.WHITE,
                           [(toggle_button.centerx - 5, toggle_button.centery - 10),
                            (toggle_button.centerx + 5, toggle_button.centery),
                            (toggle_button.centerx - 5, toggle_button.centery + 10)])
        self.dashboard_buttons['toggle'] = toggle_button
        
        # Only draw controls if dashboard is somewhat visible
        if self.dashboard_x > -self.dashboard_width + 20:
            # Draw title
            title_text = self.title_font.render("Dashboard", True, self.WHITE)
            title_rect = title_text.get_rect(center=(self.dashboard_x + self.dashboard_width // 2, 30))
            screen.blit(title_text, title_rect)
            
            # Draw balance
            balance_label = self.button_font.render("Balance:", True, self.WHITE)
            screen.blit(balance_label, (self.dashboard_x + 15, 70))
            
            balance_value = self.button_font.render(f"{self.coins:.1f}", True, self.GOLD)
            screen.blit(balance_value, (self.dashboard_x + 15, 100))
            
            # Draw amount label
            amount_label = self.button_font.render("Bet Amount:", True, self.WHITE)
            screen.blit(amount_label, (self.dashboard_x + 15, 140))
            
            # Draw amount box
            amount_box = pygame.Rect(self.dashboard_x + 15, 170, 100, 40)
            pygame.draw.rect(screen,
                           (220, 220, 220) if self.hovered_button == 'amount' else self.WHITE,
                           amount_box, border_radius=5)
            
            # Draw coin symbol in amount box
            coin_amount_x = amount_box.left + 25
            coin_amount_y = amount_box.centery
            pygame.draw.circle(screen, self.GOLD, (coin_amount_x, coin_amount_y), 10)
            pygame.draw.circle(screen, (200, 170, 0), (coin_amount_x, coin_amount_y), 8)
            
            # Draw bet amount
            amount_text = self.button_font.render(f"{self.amount:.1f}", True, self.BLACK)
            amount_rect = amount_text.get_rect(midleft=(coin_amount_x + 15, amount_box.centery))
            screen.blit(amount_text, amount_rect)
            self.dashboard_buttons['amount'] = amount_box
            
            # Draw amount adjustment buttons
            button_size = 30
            spacing = 5
            
            # Half (÷2) button
            half_button = pygame.Rect(self.dashboard_x + 120, 170, button_size, button_size)
            pygame.draw.rect(screen,
                           self.DARK_BLUE if self.hovered_button == 'half' else self.BLUE,
                           half_button, border_radius=5)
            half_text = self.button_font.render("÷2", True, self.WHITE)
            half_rect = half_text.get_rect(center=half_button.center)
            screen.blit(half_text, half_rect)
            self.dashboard_buttons['half'] = half_button
            
            # Double (×2) button
            double_button = pygame.Rect(self.dashboard_x + 155, 170, button_size, button_size)
            pygame.draw.rect(screen,
                           self.DARK_BLUE if self.hovered_button == 'double' else self.BLUE,
                           double_button, border_radius=5)
            double_text = self.button_font.render("×2", True, self.WHITE)
            double_rect = double_text.get_rect(center=double_button.center)
            screen.blit(double_text, double_rect)
            self.dashboard_buttons['double'] = double_button
            
            # Decrease button
            decrease_button = pygame.Rect(self.dashboard_x + 120, 205, button_size, button_size)
            pygame.draw.rect(screen,
                           self.DARK_BLUE if self.hovered_button == 'decrease' else self.BLUE,
                           decrease_button, border_radius=5)
            decrease_text = self.button_font.render("-", True, self.WHITE)
            decrease_rect = decrease_text.get_rect(center=decrease_button.center)
            screen.blit(decrease_text, decrease_rect)
            self.dashboard_buttons['decrease'] = decrease_button
            
            # Increase button
            increase_button = pygame.Rect(self.dashboard_x + 155, 205, button_size, button_size)
            pygame.draw.rect(screen,
                           self.DARK_BLUE if self.hovered_button == 'increase' else self.BLUE,
                           increase_button, border_radius=5)
            increase_text = self.button_font.render("+", True, self.WHITE)
            increase_rect = increase_text.get_rect(center=increase_button.center)
            screen.blit(increase_text, increase_rect)
            self.dashboard_buttons['increase'] = increase_button
            
            # Draw Risk label
            risk_label = self.button_font.render("Risk:", True, self.WHITE)
            screen.blit(risk_label, (self.dashboard_x + 15, 250))
            
            # Draw Risk combobox
            risk_box = pygame.Rect(self.dashboard_x + 15, 280, 170, 40)
            pygame.draw.rect(screen,
                           (220, 220, 220) if self.hovered_button == 'risk' else self.WHITE,
                           risk_box, border_radius=5)
            risk_text = self.button_font.render(self.risks[self.selected_risk], True, self.BLACK)
            risk_rect = risk_text.get_rect(midleft=(risk_box.left + 10, risk_box.centery))
            screen.blit(risk_text, risk_rect)
            self.dashboard_buttons['risk'] = risk_box
            
            # Draw dropdown arrow
            pygame.draw.polygon(screen, self.BLACK,
                               [(risk_box.right - 25, risk_box.centery - 5),
                                (risk_box.right - 15, risk_box.centery + 5),
                                (risk_box.right - 5, risk_box.centery - 5)])
                                
            # Draw dropdown if open
            if self.is_dropdown_open:
                dropdown_height = len(self.risks) * 40
                dropdown_rect = pygame.Rect(risk_box.left, risk_box.bottom,
                                           risk_box.width, dropdown_height)
                pygame.draw.rect(screen, self.WHITE, dropdown_rect)
                
                for i, risk in enumerate(self.risks):
                    item_rect = pygame.Rect(dropdown_rect.left, dropdown_rect.top + i * 40,
                                           dropdown_rect.width, 40)
                    if i == self.selected_risk or self.hovered_button == f'risk_{i}':
                        pygame.draw.rect(screen, self.BLUE, item_rect)
                    risk_text = self.button_font.render(risk, True,
                                                      self.WHITE if i == self.selected_risk or
                                                                    self.hovered_button == f'risk_{i}' else self.BLACK)
                    text_rect = risk_text.get_rect(midleft=(item_rect.left + 10, item_rect.centery))
                    screen.blit(risk_text, text_rect)
                    self.dashboard_buttons[f'risk_{i}'] = item_rect
                    
            # Draw Drop Ball button
            button_y = self.settings_manager.get_setting('height') - 100
            drop_button = pygame.Rect(self.dashboard_x + 15, button_y, 170, 50)
            pygame.draw.rect(screen, (0, 40, 100), pygame.Rect(drop_button.left+3, drop_button.top+3, 
                                                           drop_button.width, drop_button.height), border_radius=10)
            pygame.draw.rect(screen,
                           self.DARK_BLUE if self.hovered_button == 'drop_ball' else self.BLUE,
                           drop_button, border_radius=10)
            button_text = self.title_font.render("Drop Ball", True, self.WHITE)
            text_rect = button_text.get_rect(center=drop_button.center)
            screen.blit(button_text, text_rect)
            self.dashboard_buttons['drop_ball'] = drop_button
            
    def update_hover_state(self, pos):
        """Update which button is being hovered"""
        self.hovered_button = None
        for button_name, button_rect in self.dashboard_buttons.items():
            if button_rect.collidepoint(pos):
                self.hovered_button = button_name
                break
                
    def handle_click(self, pos):
        """Handle mouse clicks on dashboard buttons"""
        # Update hover state first
        self.update_hover_state(pos)
        
        # Check if any button was clicked
        for button_name, button_rect in self.dashboard_buttons.items():
            if button_rect.collidepoint(pos):
                if button_name == 'toggle':
                    self.dashboard_extended = not self.dashboard_extended
                elif button_name == 'increase':
                    new_amount = round(self.amount + 0.1, 1)
                    self.amount = min(new_amount, float(self.coins))
                elif button_name == 'decrease':
                    new_amount = round(self.amount - 0.1, 1)
                    self.amount = max(0, new_amount)
                elif button_name == 'double':
                    new_amount = round(self.amount * 2, 1)
                    self.amount = min(new_amount, float(self.coins))
                elif button_name == 'half':
                    self.amount = round(self.amount / 2, 1)
                elif button_name == 'risk':
                    self.is_dropdown_open = not self.is_dropdown_open
                elif button_name.startswith('risk_'):
                    self.selected_risk = int(button_name.split('_')[1])
                    self.is_dropdown_open = False
                elif button_name == 'drop_ball':
                    self.on_drop_ball(self.amount)
                return True
        return False 