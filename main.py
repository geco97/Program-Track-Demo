# Import necessary libraries
import os  # For interacting with the operating system
import time  # For tracking time intervals
import json  # For saving/loading data in JSON format
import psutil  # For accessing process information
import win32gui  # For interacting with Windows GUI elements
import win32process  # For retrieving process IDs from window handles
import pygame  # For creating a graphical user interface
from collections import defaultdict  # For handling default dictionary behavior

# Define constants
HISTORY_FILE = "history.json"  # File to store program usage history
FOCUS_MODE = False  # Flag to enable/disable focus mode (initially off)
BLOCKED_APPS = {"YouTube", "Facebook", "Netflix", "Twitter"}  # Set of apps blocked in focus mode
WHITE = (255, 255, 255)  # White color for UI text
BLACK = (0, 0, 0)  # Black color for UI background
RED = (220, 20, 60)  # Red color for alerts
DARK_GRAY = (50, 50, 50)  # Dark gray color for UI background

# Function to display a notification message
def notify_user(message):
    """Display a notification message using the 'msg' command."""
    os.system(f"msg * {message}")

# Function to get the title of the currently active window
def get_active_window():
    """Retrieve the name of the currently active program."""
    hwnd = win32gui.GetForegroundWindow()  # Get the handle of the active window
    if hwnd:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)  # Get the process ID of the active window
        try:
            proc = psutil.Process(pid)  # Get the process object
            return proc.name()  # Return the process name
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return "Unknown"  # Return "Unknown" if the process cannot be accessed
    return "Unknown"  # Return "Unknown" if no active window is found

# Class to track active programs and their usage time
class ProcessTracker:
    """Tracks active programs and their usage time."""
    
    def __init__(self):
        """Initialize the ProcessTracker with an empty usage data dictionary."""
        self.usage_data = defaultdict(lambda: {"duration": 0})  # Default dictionary to store program durations
        self.current_program = None  # Currently active program
        self.last_switch_time = time.time()  # Timestamp of the last program switch
        self.load_history()  # Load existing usage history from file
    
    def update(self):
        """Update the active program tracking."""
        global FOCUS_MODE  # Access the global FOCUS_MODE variable
        active_program = get_active_window()  # Get the currently active program
        current_time = time.time()  # Get the current timestamp
        
        # Focus Mode: Block distractions
        if FOCUS_MODE and active_program in BLOCKED_APPS:
            notify_user(f"Focus Mode: {active_program} is blocked!")  # Notify the user about blocked apps
            return  # Do not track blocked apps during focus mode
        
        # Track program usage
        if active_program != self.current_program:  # If the active program has changed
            if self.current_program:  # If there was a previously active program
                self.usage_data[self.current_program]["duration"] += current_time - self.last_switch_time  # Update its duration
                self.save_history()  # Save the updated usage data
            self.current_program = active_program  # Update the current program
            self.last_switch_time = current_time  # Update the last switch time
    
    def save_history(self):
        """Save the usage history to a file."""
        with open(HISTORY_FILE, "w") as f:  # Open the history file in write mode
            json.dump(self.usage_data, f, indent=4)  # Save the usage data as JSON
    
    def load_history(self):
        """Load usage history from file."""
        try:
            with open(HISTORY_FILE, "r") as f:  # Open the history file in read mode
                self.usage_data.update(json.load(f))  # Load and update the usage data
        except (FileNotFoundError, json.JSONDecodeError):  # Handle missing or corrupted files
            pass  # If the file doesn't exist or is invalid, do nothing
    
    def reset_history(self):
        """Reset the tracking history."""
        self.usage_data.clear()  # Clear the usage data
        self.save_history()  # Save the cleared data to the file

# Class to create a simple pygame-based UI for displaying active program tracking
class Stopwatch:
    """Simple pygame-based UI for displaying active program tracking."""
    
    def __init__(self):
        """Initialize the pygame UI."""
        pygame.init()  # Initialize pygame
        self.screen = pygame.display.set_mode((500, 350))  # Create a 500x350 window
        pygame.display.set_caption("Program Tracker")  # Set the window title
        self.font = pygame.font.Font(None, 30)  # Set the font for text rendering
        self.tracker = ProcessTracker()  # Initialize the ProcessTracker instance
        self.loop()  # Start the main loop
    
    def draw_text(self, text, position, color=WHITE):
        """Render and display text on the screen."""
        rendered_text = self.font.render(text, True, color)  # Render the text
        self.screen.blit(rendered_text, position)  # Display the rendered text at the specified position
    
    def toggle_focus_mode(self):
        """Toggle focus mode on/off."""
        global FOCUS_MODE  # Access the global FOCUS_MODE variable
        FOCUS_MODE = not FOCUS_MODE  # Toggle the focus mode flag
        print(f"Focus Mode {'ON' if FOCUS_MODE else 'OFF'}")  # Print the current focus mode status
    
    def loop(self):
        """Main loop for updating program tracking and UI."""
        while True:
            self.screen.fill(DARK_GRAY)  # Fill the screen with dark gray
            for event in pygame.event.get():  # Handle events
                if event.type == pygame.QUIT:  # If the user closes the window
                    self.tracker.save_history()  # Save the usage data
                    pygame.quit()  # Quit pygame
                    return  # Exit the program
                elif event.type == pygame.KEYDOWN:  # If a key is pressed
                    if event.key == pygame.K_r:  # If 'R' is pressed
                        self.tracker.reset_history()  # Reset the usage history
                    elif event.key == pygame.K_q:  # If 'Q' is pressed
                        self.tracker.save_history()  # Save the usage data
                        pygame.quit()  # Quit pygame
                        return  # Exit the program
                    elif event.key == pygame.K_f:  # If 'F' is pressed
                        self.toggle_focus_mode()  # Toggle focus mode
            
            self.tracker.update()  # Update the program tracking
            self.update_display()  # Update the UI display
            pygame.display.flip()  # Refresh the display
            pygame.time.delay(500)  # Wait for 500ms before the next iteration
    
    def update_display(self):
        """Display active program and tracking info."""
        self.draw_text(f"Active: {self.tracker.current_program}", (20, 50))  # Display the currently active program
        
        # Sort and display the top 5 programs by usage duration
        sorted_programs = sorted(self.tracker.usage_data.items(), key=lambda x: x[1]["duration"], reverse=True)[:5]
        y_offset = 100  # Vertical offset for displaying program usage
        for name, data in sorted_programs:
            mins = int(data["duration"] // 60)  # Convert seconds to minutes
            self.draw_text(f"{name}: {mins} min", (20, y_offset))  # Display program name and usage time
            y_offset += 30  # Increment the vertical offset
        
        # Show Focus Mode status
        self.draw_text(f"Focus Mode: {'ON' if FOCUS_MODE else 'OFF'}", (20, 10), RED if FOCUS_MODE else WHITE)
        
        # Show footer with commands
        pygame.draw.rect(self.screen, BLACK, (0, 300, 500, 50))  # Draw a black rectangle for the footer
        self.draw_text("Commands: R | Q | F ", (20, 320))  # Display available commands

# Entry point of the program
if __name__ == "__main__":
    Stopwatch()  # Start the program tracker