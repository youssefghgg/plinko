import tkinter as tk
from tkinter import ttk


class PlinkoGame:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Plinko Game")
        self.root.geometry("800x600")  # Default size

        # Variables for theme
        self.is_dark_mode = False

        # Configure style for buttons
        self.style = ttk.Style()
        self.style.configure('Custom.TButton',
                             padding=10,
                             font=('Helvetica', 12))

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(expand=True)

        # Create buttons
        self.create_buttons()

        # Apply initial theme
        self.apply_theme()

    def create_buttons(self):
        # Start Game button
        self.start_button = ttk.Button(
            self.main_frame,
            text="Start Game",
            style='Custom.TButton',
            command=self.start_game
        )
        self.start_button.pack(pady=10)

        # Settings button
        self.settings_button = ttk.Button(
            self.main_frame,
            text="Settings",
            style='Custom.TButton',
            command=self.open_settings
        )
        self.settings_button.pack(pady=10)

        # Quit button
        self.quit_button = ttk.Button(
            self.main_frame,
            text="Quit",
            style='Custom.TButton',
            command=self.root.quit
        )
        self.quit_button.pack(pady=10)

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
        if self.is_dark_mode:
            # Dark theme colors
            self.root.configure(bg='#2d2d2d')
            self.main_frame.configure(style='Dark.TFrame')
            self.style.configure('Dark.TFrame', background='#2d2d2d')
            self.style.configure('Custom.TButton',
                                 background='#404040',
                                 foreground='white')
        else:
            # Light theme colors
            self.root.configure(bg='#f0f0f0')
            self.main_frame.configure(style='Light.TFrame')
            self.style.configure('Light.TFrame', background='#f0f0f0')
            self.style.configure('Custom.TButton',
                                 background='#e0e0e0',
                                 foreground='black')

    def run(self):
        self.root.mainloop()


# Create and run the game
if __name__ == "__main__":
    game = PlinkoGame()
    game.run()