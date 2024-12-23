import pyautogui
import time
import os


def take_screenshot_of_game_window():
    # Adjusted coordinates and size from xwininfo, excluding side border
    # x = 0        # X coordinate remains the same (left edge of the window)
    # y = 69       # Y coordinate adjusted to account for the top offset
    # w = 835        # Reduced width to exclude the side border (estimate 30px each side)
    # h = 830          # Height adjusted to fit the content, as done before

    # x=350
    # y=425
    # w=100
    # h=100

    # x = 212
    # y = 790
    # w = 96
    # h = 69

    #these are to check the inv ss dimensions:
    x = 630
    y = 552
    w = 200
    h = 275

    # Ensure the directory exists
    os.makedirs('pyauto-images', exist_ok=True)

    # Path to save the screenshot
    screenshot_path = 'pyauto-images/game_window_screenshot.png'

    # Wait a moment to make sure the window is focused
    time.sleep(1)

    # Capture the screenshot of the game window excluding the title bar, borders, and side border
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    screenshot.save(screenshot_path)
    print(f"Screenshot saved as '{screenshot_path}'")

# Example usage
take_screenshot_of_game_window()
