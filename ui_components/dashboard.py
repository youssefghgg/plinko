import pygame

class Dashboard:
    """Dashboard UI component for controlling the game"""
    
    def __init__(self, settings_manager, on_drop_ball, game_state):
        self.settings_manager = settings_manager
        self.on_drop_ball = on_drop_ball
        self.game_state = game_state
        self.amount = 0.0  # Bet amount
        
        # Dashboard state
        self.dashboard_extended = True  # Always show dashboard
        self.dashboard_y = 0  # Position from bottom
        self.dashboard_buttons = {}
        self.hovered_button = None
        
        # Risk options and state
        self.risks = ["Easy (2%)", "Medium (15%)", "Hard (40%)"]
        self.risk_values = [0.02, 0.15, 0.40]  # Corresponding risk values
        self.selected_risk = 0
        self.is_dropdown_open = False
        
        # Preset bet amounts
        self.preset_amounts = [0.1, 0.5, 1.0, 5.0, 10.0]
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 120, 255)
        self.DARK_BLUE = (0, 80, 180)
        self.GOLD = (255, 215, 0)
        self.GRAY = (60, 60, 60)
        self.LIGHT_GRAY = (200, 200, 200)
        self.GREEN = (50, 200, 100)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 32)
        self.button_font = pygame.font.Font(None, 28)
        self.coin_font = pygame.font.Font(None, 24)
        
    def update(self):
        """Update dashboard animation"""
        pass  # No longer need animation since dashboard is always visible
        
    def draw(self, screen):
        """Draw the dashboard"""
        width = self.settings_manager.get_setting('width')
        height = self.settings_manager.get_setting('height')
        dark_mode = self.settings_manager.get_setting('dark_mode', False)
        
        # Dashboard is now a bottom panel, moved up by 30px
        dashboard_height = 120
        dashboard_y = height - dashboard_height - 30  # Moved up by 30px
        
        # Fill background
        bg_color = (25, 30, 40) if dark_mode else (30, 40, 80)
        dashboard_rect = pygame.Rect(0, dashboard_y, width, dashboard_height)
        pygame.draw.rect(screen, bg_color, dashboard_rect)
        
        # Add subtle top border
        border_color = (60, 70, 90) if dark_mode else (60, 100, 180)
        pygame.draw.line(screen, border_color, (0, dashboard_y), (width, dashboard_y), 2)
        
        # Draw balance section (left side)
        balance_x = 20
        balance_y = dashboard_y + 25
        
        # Balance label with icon
        balance_icon = "💰"  # Money bag emoji
        balance_label_text = f"{balance_icon} BALANCE"
        balance_label = self.coin_font.render(balance_label_text, True, self.LIGHT_GRAY)
        screen.blit(balance_label, (balance_x, balance_y))
        
        # Balance value with coin icon
        balance_value_y = balance_y + 30
        
        # Draw coin icon
        coin_size = 20
        pygame.draw.circle(screen, self.GOLD, (balance_x + coin_size//2, balance_value_y + coin_size//2), coin_size//2)
        
        # Draw balance value
        balance_text = self.button_font.render(f"{self.game_state.coins:.1f}", True, self.WHITE)
        screen.blit(balance_text, (balance_x + coin_size + 10, balance_value_y))
        
        # Draw risk selector (center)
        risk_x = width // 2 - 100
        risk_y = dashboard_y + 25
        
        # Risk label with icon
        risk_icon = "⚡"  # Lightning bolt emoji for risk
        risk_label_text = f"{risk_icon} RISK LEVEL"
        risk_label = self.coin_font.render(risk_label_text, True, self.LIGHT_GRAY)
        screen.blit(risk_label, (risk_x, risk_y))
        
        # Risk selector
        risk_bg = pygame.Rect(risk_x, risk_y + 30, 200, 40)
        pygame.draw.rect(screen, self.GRAY, risk_bg, border_radius=5)
        
        # Risk selection
        risk_text = self.button_font.render(self.risks[self.selected_risk], True, self.WHITE)
        risk_text_rect = risk_text.get_rect(center=(risk_bg.centerx, risk_bg.centery))
        screen.blit(risk_text, risk_text_rect)
        
        # Risk arrow indicators
        # Left arrow
        arrow_padding = 15
        left_arrow = [(risk_bg.left + arrow_padding, risk_bg.centery),
                     (risk_bg.left + arrow_padding*2, risk_bg.centery - arrow_padding//2),
                     (risk_bg.left + arrow_padding*2, risk_bg.centery + arrow_padding//2)]
        pygame.draw.polygon(screen, self.WHITE, left_arrow)
        self.dashboard_buttons['risk_prev'] = pygame.Rect(risk_bg.left, risk_bg.top, 40, risk_bg.height)
        
        # Right arrow
        right_arrow = [(risk_bg.right - arrow_padding, risk_bg.centery),
                      (risk_bg.right - arrow_padding*2, risk_bg.centery - arrow_padding//2),
                      (risk_bg.right - arrow_padding*2, risk_bg.centery + arrow_padding//2)]
        pygame.draw.polygon(screen, self.WHITE, right_arrow)
        self.dashboard_buttons['risk_next'] = pygame.Rect(risk_bg.right - 40, risk_bg.top, 40, risk_bg.height)
        
        # Draw bet controls (right side)
        bet_x = width - 300
        bet_y = dashboard_y + 25
        
        # Draw bet label with icon
        bet_icon = "🎯"  # Target emoji for betting
        bet_label_text = f"{bet_icon} BET AMOUNT"
        bet_label = self.coin_font.render(bet_label_text, True, self.LIGHT_GRAY)
        screen.blit(bet_label, (bet_x, bet_y))
        
        # Draw bet amount input
        bet_input_width = 120  # Reduced width for better spacing
        bet_amount_bg = pygame.Rect(bet_x, bet_y + 30, bet_input_width, 40)
        
        # Add a hint of color if amount is valid
        if self.amount > 0 and self.amount <= self.game_state.coins:
            input_color = (70, 80, 90) if dark_mode else (40, 70, 120)
        else:
            input_color = (90, 50, 50) if dark_mode else (120, 40, 40)  # Red tint if invalid
            
        pygame.draw.rect(screen, input_color, bet_amount_bg, border_radius=5)
        
        # Draw amount with coin icon
        coin_x = bet_amount_bg.left + 15
        coin_y = bet_amount_bg.centery
        pygame.draw.circle(screen, self.GOLD, (coin_x, coin_y), 10)
        pygame.draw.circle(screen, (200, 170, 0), (coin_x, coin_y), 8)
        
        # Amount text
        amount_text = self.button_font.render(f"{self.amount:.1f}", True, self.WHITE)
        amount_rect = amount_text.get_rect(midleft=(coin_x + 20, bet_amount_bg.centery))
        screen.blit(amount_text, amount_rect)
        self.dashboard_buttons['amount'] = bet_amount_bg
        
        # Draw bet adjustment buttons with better styling
        button_size = 32
        button_spacing = 10
        
        # Decrease button (-)
        decrease_button = pygame.Rect(bet_x + bet_input_width + button_spacing, bet_y + 30, button_size, button_size)
        decrease_bg = self.DARK_BLUE if self.hovered_button == 'decrease' else self.BLUE
        pygame.draw.rect(screen, decrease_bg, decrease_button, border_radius=5)
        decrease_text = self.button_font.render("-", True, self.WHITE)
        decrease_rect = decrease_text.get_rect(center=decrease_button.center)
        screen.blit(decrease_text, decrease_rect)
        self.dashboard_buttons['decrease'] = decrease_button
        
        # Increase button (+)
        increase_button = pygame.Rect(decrease_button.right + button_spacing, bet_y + 30, button_size, button_size)
        increase_bg = self.DARK_BLUE if self.hovered_button == 'increase' else self.BLUE
        pygame.draw.rect(screen, increase_bg, increase_button, border_radius=5)
        increase_text = self.button_font.render("+", True, self.WHITE)
        increase_rect = increase_text.get_rect(center=increase_button.center)
        screen.blit(increase_text, increase_rect)
        self.dashboard_buttons['increase'] = increase_button
        
        # MAX button
        max_button = pygame.Rect(increase_button.right + button_spacing, bet_y + 30, 60, button_size)
        max_bg_color = (0, 140, 120) if self.hovered_button == 'max' else (0, 120, 100)
        pygame.draw.rect(screen, max_bg_color, max_button, border_radius=5)
        max_text = self.button_font.render("MAX", True, self.WHITE)
        max_text_rect = max_text.get_rect(center=max_button.center)
        screen.blit(max_text, max_text_rect)
        self.dashboard_buttons['max'] = max_button
        
        # Draw preset bet amounts
        preset_width = 55
        preset_height = 30
        preset_y = bet_amount_bg.bottom + 10
        
        for i, amount in enumerate(self.preset_amounts):
            preset_x = bet_x + i * (preset_width + 5)
            preset_rect = pygame.Rect(preset_x, preset_y, preset_width, preset_height)
            
            # Highlight selected preset or on hover
            if abs(self.amount - amount) < 0.01 or self.hovered_button == f'preset_{i}':
                pygame.draw.rect(screen, self.GREEN, preset_rect, border_radius=5)
            else:
                pygame.draw.rect(screen, self.GRAY, preset_rect, border_radius=5)
                
            # Preset text
            preset_text = self.coin_font.render(f"{amount:.1f}", True, self.WHITE)
            preset_text_rect = preset_text.get_rect(center=preset_rect.center)
            screen.blit(preset_text, preset_text_rect)
            self.dashboard_buttons[f'preset_{i}'] = preset_rect
        
        # Draw play button - large and centered at bottom
        play_button_width = 180
        play_button_height = 50
        play_button = pygame.Rect(width//2 - play_button_width//2, 
                                 height - play_button_height - 45,  # Update position to match moved dashboard
                                 play_button_width, play_button_height)
        
        # Draw shadow for play button
        shadow_offset = 3
        shadow_rect = pygame.Rect(play_button.left + shadow_offset, 
                                 play_button.top + shadow_offset,
                                 play_button.width, play_button.height)
        pygame.draw.rect(screen, (0, 100, 50) if dark_mode else (0, 120, 60), 
                        shadow_rect, border_radius=8)
        
        # Determine button color based on hover and if bet is valid
        if self.amount > 0 and self.amount <= self.game_state.coins:
            play_color = (0, 180, 80) if self.hovered_button == 'drop_ball' else (0, 160, 70)
        else:
            play_color = (80, 80, 80)  # Disabled gray
        
        pygame.draw.rect(screen, play_color, play_button, border_radius=8)
        
        # Draw play text
        play_text = self.title_font.render("DROP BALL", True, self.WHITE)
        play_text_rect = play_text.get_rect(center=play_button.center)
        screen.blit(play_text, play_text_rect)
        self.dashboard_buttons['drop_ball'] = play_button
            
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
                if button_name == 'increase':
                    new_amount = round(self.amount + 0.1, 1)
                    self.amount = min(new_amount, float(self.game_state.coins))
                    return True
                elif button_name == 'decrease':
                    new_amount = round(self.amount - 0.1, 1)
                    self.amount = max(0, new_amount)
                    return True
                elif button_name == 'max':
                    # Set bet to max amount (player's entire balance)
                    self.amount = float(self.game_state.coins)
                    return True
                elif button_name == 'risk_prev':
                    self.selected_risk = (self.selected_risk - 1) % len(self.risks)
                    return True
                elif button_name == 'risk_next':
                    self.selected_risk = (self.selected_risk + 1) % len(self.risks)
                    return True
                elif button_name.startswith('preset_'):
                    preset_index = int(button_name.split('_')[1])
                    if preset_index < len(self.preset_amounts):
                        preset_amount = self.preset_amounts[preset_index]
                        self.amount = min(preset_amount, float(self.game_state.coins))
                    return True
                elif button_name == 'drop_ball':
                    # Ensure the coin balance updates properly
                    if self.amount > 0 and self.amount <= self.game_state.coins:
                        self.on_drop_ball(self.amount)
                    return True
                
        return False  # No button clicked 