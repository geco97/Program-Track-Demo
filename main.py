import os
import time
import json
import psutil
import win32gui
import win32process
import pygame
from collections import defaultdict

HISTORY_FILE = "history.json"
FOCUS_MODE = False  # Enable/disable focus mode
BLOCKED_APPS = {"YouTube", "Facebook", "Netflix", "Twitter"}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
DARK_GRAY = (50, 50, 50)


def notify_user(message):
    """Display a notification message."""
    os.system(f"msg * {message}")


def get_active_window():
    """Get the title of the currently active window."""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        try:
            proc = psutil.Process(pid)
            return proc.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return "Unknown"
    return "Unknown"


class ProcessTracker:
    """Tracks active programs and their usage time."""
    
    def __init__(self):
        self.usage_data = defaultdict(lambda: {"duration": 0})
        self.current_program = None
        self.last_switch_time = time.time()
        self.load_history()

    def update(self):
        """Update the active program tracking."""
        global FOCUS_MODE
        active_program = get_active_window()
        current_time = time.time()

        # Focus Mode: Block distractions
        if FOCUS_MODE and active_program in BLOCKED_APPS:
            notify_user(f"Focus Mode: {active_program} is blocked!")
            return

        # Track program usage
        if active_program != self.current_program:
            if self.current_program:
                self.usage_data[self.current_program]["duration"] += current_time - self.last_switch_time
                self.save_history()

            self.current_program = active_program
            self.last_switch_time = current_time

    def save_history(self):
        """Save the usage history to a file."""
        with open(HISTORY_FILE, "w") as f:
            json.dump(self.usage_data, f, indent=4)

    def load_history(self):
        """Load usage history from file."""
        try:
            with open(HISTORY_FILE, "r") as f:
                self.usage_data.update(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def reset_history(self):
        """Reset the tracking history."""
        self.usage_data.clear()
        self.save_history()


class Stopwatch:
    """Simple pygame-based UI for displaying active program tracking."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 350))
        pygame.display.set_caption("Program Tracker")
        self.font = pygame.font.Font(None, 30)
        self.tracker = ProcessTracker()
        self.loop()

    def draw_text(self, text, position, color=WHITE):
        """Render and display text on the screen."""
        self.screen.blit(self.font.render(text, True, color), position)

    def toggle_focus_mode(self):
        """Toggle focus mode on/off."""
        global FOCUS_MODE
        FOCUS_MODE = not FOCUS_MODE
        print(f"Focus Mode {'ON' if FOCUS_MODE else 'OFF'}")

    def loop(self):
        """Main loop for updating program tracking and UI."""
        while True:
            self.screen.fill(DARK_GRAY)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.tracker.save_history()
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.tracker.reset_history()
                    elif event.key == pygame.K_q:
                        self.tracker.save_history()
                        pygame.quit()
                        return
                    elif event.key == pygame.K_f:
                        self.toggle_focus_mode()

            self.tracker.update()
            self.update_display()
            pygame.display.flip()
            pygame.time.delay(500)

    def update_display(self):
        """Display active program and tracking info."""
        self.draw_text(f"Active: {self.tracker.current_program}", (20, 50))
        
        sorted_programs = sorted(self.tracker.usage_data.items(), key=lambda x: x[1]["duration"], reverse=True)[:5]
        y_offset = 100
        for name, data in sorted_programs:
            mins = int(data["duration"] // 60)
            self.draw_text(f"{name}: {mins} min", (20, y_offset))
            y_offset += 30

        # Show Focus Mode status
        self.draw_text(f"Focus Mode: {'ON' if FOCUS_MODE else 'OFF'}", (20, 10), RED if FOCUS_MODE else WHITE)

        # Show footer with commands
        pygame.draw.rect(self.screen, BLACK, (0, 300, 500, 50))
        self.draw_text("Commands: R | Q | F ", (20, 320))


if __name__ == "__main__":
    Stopwatch()
