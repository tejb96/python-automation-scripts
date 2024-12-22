import pyautogui
import time
import os
from PIL import Image

def take_screenshot_of_game_window():
    # Adjusted coordinates and size from xwininfo, excluding side border
    relative_x = 0        # X coordinate remains the same (left edge of the window)
    relative_y = 69       # Y coordinate adjusted to account for the top offset
    width = 835        # Reduced width to exclude the side border (estimate 30px each side)
    height = 830          # Height adjusted to fit the content, as done before

    # Ensure the directory exists
    os.makedirs('pyauto-images', exist_ok=True)

    # Path to save the screenshot
    screenshot_path = 'pyauto-images/game_window_screenshot.png'

    # Wait a moment to make sure the window is focused
    time.sleep(1)

    # Capture the screenshot of the game window excluding the title bar, borders, and side border
    screenshot = pyautogui.screenshot(region=(relative_x, relative_y, width, height))
    screenshot.save(screenshot_path)
    print(f"Screenshot saved as '{screenshot_path}'")

# Example usage
take_screenshot_of_game_window()
