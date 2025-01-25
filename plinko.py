import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont


class PlinkoGame:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Plinko Game")
        self.root.geometry("800x600")  # Default size

        # Variables for theme
        self.is_dark_mode = False

        # Create and configure styles
        self.create_styles()

        # Create background frame with gradient effect
        self.background_frame = tk.Frame(self.root)
        self.background_frame.pack(fill='both', expand=True)
        self.create_gradient()

        # Create title frame
        self.create_title()

        # Create main frame for buttons
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Create buttons
        self.create_buttons()

        # Apply initial theme
        self.apply_theme()

    def create_buttons(self):
        # Create a frame for button container with spacing
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        # Button configurations
        button_configs = [
            ("Start Game", self.start_game, '#4CAF50'),  # Green
            ("Settings", self.open_settings, '#2196F3'),  # Blue
            ("Quit", self.root.quit, '#f44336')  # Red
        ]

    def create_styles(self):
        self.style = ttk.Style()

        # Configure button style
        self.style.configure('Custom.TButton',
                             padding=(20, 10),
                             font=('Helvetica', 14, 'bold'),
                             borderwidth=3,
                             relief='raised')

    def create_gradient(self):
        # Create canvas for gradient background
        self.canvas = tk.Canvas(self.background_frame, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        # Create gradient
        self.update_gradient()

        # Bind resize event
        self.root.bind('<Configure>', lambda e: self.update_gradient())

    def update_gradient(self):
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Clear previous gradient
        self.canvas.delete("gradient")

        # Create new gradient
        for i in range(height):
            # Calculate color for current line
            if self.is_dark_mode:
                r = int(25 + (i / height) * 20)
                g = int(25 + (i / height) * 20)
                b = int(45 + (i / height) * 20)
            else:
                r = int(100 + (i / height) * 155)
                g = int(150 + (i / height) * 105)
                b = int(255 - (i / height) * 105)

            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color, tags="gradient")

    def create_title(self):
        # Create title frame
        title_frame = ttk.Frame(self.root)
        title_frame.place(relx=0.5, rely=0.15, anchor='center')

        # Create canvas for arched text
        canvas_width = 400
        canvas_height = 150
        title_canvas = tk.Canvas(title_frame,
                                 width=canvas_width,
                                 height=canvas_height,
                                 highlightthickness=0,
                                 bd=0)
        title_canvas.pack()

    def update_title_bg(event=None):
        # Get the current background color from gradient
        if self.is_dark_mode:
            bg_color = '#2d2d2d'
        else:
            bg_color = '#f0f0f0'
        title_canvas.configure(bg=bg_color)

        # Clear previous text
        title_canvas.delete('all')

        # Create arched text
        text = "PLINKO!"
        font_size = 48
        title_font = tkfont.Font(family='Helvetica', size=font_size, weight='bold')

        # Calculate positions for each letter
        center_x = canvas_width // 2
        base_y = canvas_height // 2
        spacing = 30  # Adjust spacing between letters
        arch_height = 30  # Adjust the height of the arch

        # Calculate total width of text for centering
        total_width = (len(text) - 1) * spacing
        start_x = center_x - (total_width // 2)

        # Draw each letter with vertical offset based on position
        for i, letter in enumerate(text):
            x = start_x + (i * spacing)
            # Calculate y offset using a parabolic function
            rel_pos = (x - center_x) / (total_width / 2)  # Position relative to center (-1 to 1)
            y_offset = arch_height * (rel_pos ** 2)  # Parabolic arch
            y = base_y - arch_height + y_offset

            title_canvas.create_text(x, y,
                                     text=letter,
                                     font=title_font,
                                     fill=fg_color if self.is_dark_mode else 'black')

        # Add subtitle
        subtitle_font = tkfont.Font(family='Helvetica', size=14, weight='normal', slant='italic')
        title_canvas.create_text(center_x, base_y + 40,
                                 text="Test your luck!",
                                 font=subtitle_font,
                                 fill=fg_color if self.is_dark_mode else 'black')
        # Bind the update function to the canvas
        title_canvas.bind('<Configure>', update_title_bg)
        self.root.bind('<Configure>', update_title_bg)

        # Store the update function for theme changes
        self._update_title = update_title_bg

    def on_enter(self, button, color):
        button.config(bg=color, fg='white')

    def on_leave(self, button):
        if self.is_dark_mode:
            button.config(bg='#404040', fg='white')
        else:
            button.config(bg='#f0f0f0', fg='black')

    def start_game(self):
        # Placeholder for future implementation
        pass

    def open_settings(self):
        # Create settings window
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)  # Make window modal

        # Create frame for settings
        settings_frame = ttk.Frame(settings_window, padding="20")
        settings_frame.pack(expand=True)

        # Window size settings
        size_label = ttk.Label(settings_frame, text="Window Size:")
        size_label.pack(pady=5)

        # Size options
        sizes = ["800x600", "1024x768", "1280x720"]
        size_var = tk.StringVar(value=self.root.geometry().split("+")[0])

        for size in sizes:
            ttk.Radiobutton(
                settings_frame,
                text=size,
                value=size,
                variable=size_var,
                command=lambda s=size: self.change_size(s)
            ).pack()

        # Dark mode toggle
        dark_mode_var = tk.BooleanVar(value=self.is_dark_mode)
        dark_mode_check = ttk.Checkbutton(
            settings_frame,
            text="Dark Mode",
            variable=dark_mode_var,
            command=lambda: self.toggle_dark_mode(dark_mode_var.get())
        )
        dark_mode_check.pack(pady=20)

    def change_size(self, size):
        self.root.geometry(size)

    def toggle_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_theme()

    def apply_theme(self):
        bg_color = '#2d2d2d' if self.is_dark_mode else '#f0f0f0'
        fg_color = 'white' if self.is_dark_mode else 'black'

        # Update root background
        self.root.configure(bg=bg_color)

        # Update gradient
        self.update_gradient()

        # Update title
        if hasattr(self, '_update_title'):
            self._update_title()

        # Force redraw of all rounded buttons
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ttk.Frame):  # Button frame
                for button in widget.winfo_children():
                    if isinstance(button, tk.Canvas):  # RoundedButton
                        button._draw_button()

    def run(self):
        self.root.mainloop()

    # Custom rounded button style
    class RoundedButton(tk.Canvas):
        def __init__(self, parent, text, command, color, **kwargs):
            super().__init__(parent, **kwargs)
            self.color = color
            self.command = command
            self.text = text

            # Bind events
            self.bind('<Button-1>', self._on_click)
            self.bind('<Enter>', self._on_enter)
            self.bind('<Leave>', self._on_leave)

            self._draw_button()

        def _draw_button(self, state='normal'):
            self.delete('all')
            width = self.winfo_width()
            height = self.winfo_height()

            # Colors based on state
            if state == 'normal':
                bg_color = '#f0f0f0' if not game.is_dark_mode else '#404040'
                text_color = 'black' if not game.is_dark_mode else 'white'
            elif state == 'hover':
                bg_color = self.color
                text_color = 'white'

            # Create rounded rectangle
            radius = height // 2
            self.create_oval(0, 0, height, height, fill=bg_color, outline='')
            self.create_oval(width - height, 0, width, height, fill=bg_color, outline='')
            self.create_rectangle(height // 2, 0, width - height // 2, height, fill=bg_color, outline='')

            # Add text
            font = ('Helvetica', 14, 'bold')
            self.create_text(width // 2, height // 2, text=self.text,
                             font=font, fill=text_color)

        def _on_click(self, event):
            if self.command:
                self.command()

        def _on_enter(self, event):
            self._draw_button('hover')

        def _on_leave(self, event):
            self._draw_button('normal')

    # Create buttons
    for text, command, color in button_configs:
        btn = RoundedButton(button_frame, text=text, command=command, color=color,
                            width=200, height=40, highlightthickness=0, bd=0)
        btn.pack(pady=10)


# Create and run the game
if __name__ == "__main__":
    game = PlinkoGame()
    game.run()