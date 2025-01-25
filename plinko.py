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

        for text, command, color in button_configs:
            btn = tk.Button(button_frame,
                            text=text,
                            command=command,
                            font=('Helvetica', 14, 'bold'),
                            width=15,
                            bd=0,
                            relief='raised',
                            pady=10,
                            cursor='hand2')  # Hand cursor on hover
            btn.pack(pady=10)

            # Bind hover effects
            btn.bind('<Enter>', lambda e, b=btn, c=color: self.on_enter(b, c))
            btn.bind('<Leave>', lambda e, b=btn: self.on_leave(b))

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

        # Create main title with system background color
        title_font = tkfont.Font(family='Helvetica', size=48, weight='bold')
        title_label = tk.Label(title_frame,
                               text="PLINKO!",
                               font=title_font,
                               bg=self.root.cget('bg'))  # Use system background color
        title_label.pack()

        # Create subtitle
        subtitle_font = tkfont.Font(family='Helvetica', size=14, weight='normal', slant='italic')
        subtitle_label = tk.Label(title_frame,
                                  text="Test your luck!",
                                  font=subtitle_font,
                                  bg=self.root.cget('bg'))  # Use system background color
        subtitle_label.pack(pady=10)

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

        # Update all labels
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(fg=fg_color, bg=bg_color)

        # Update buttons
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(
                    bg='#404040' if self.is_dark_mode else '#f0f0f0',
                    fg=fg_color,
                    activebackground='#505050' if self.is_dark_mode else '#e0e0e0',
                    activeforeground=fg_color
                )

        # Update gradient
        self.update_gradient()

    def run(self):
        self.root.mainloop()


# Create and run the game
if __name__ == "__main__":
    game = PlinkoGame()
    game.run()