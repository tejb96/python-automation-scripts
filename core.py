import subprocess
import yaml
import platform

global hwnd
hwnd = 0

with open("pybot-config.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)


def get_window_class(window_id):
    """Get the WM_CLASS of a window given its ID."""
    try:
        window_class = subprocess.check_output(['xprop', '-id', window_id, 'WM_CLASS']).strip()
        return window_class
    except subprocess.CalledProcessError as e:
        print(f"Error getting window class for ID {window_id}: {e}")
        return None


def activate_and_resize_window(data):
    """Find a window by name, activate it, and resize it."""
    try:
        # Use `xdotool search` to find window by its name
        window_ids = subprocess.check_output(['xdotool', 'search', '--name', data]).strip().split()

        for window_id in window_ids:
            window_id = window_id.decode("utf-8")
            window_class = get_window_class(window_id)

            if window_class and b"net-runelite-client-RuneLite" in window_class:
                # Activate the window
                subprocess.run(['xdotool', 'windowactivate', window_id])
                # Move and resize the window
                subprocess.run(['xdotool', 'windowmove', window_id, '0', '30'])
                subprocess.run(['xdotool', 'windowsize', window_id, '865', '830'])
                print(f"Window ID {window_id} activated and resized.")
                return

        print("Main window not found.")
    except subprocess.CalledProcessError as e:
        print(f"Error finding or manipulating window: {e}")


def get_window_geometry(data):
    """Focus the window and get its geometry, adjusting for any offsets from window manager decorations and RuneLite borders."""
    try:
        # Get the window IDs of the matching windows
        window_ids = subprocess.check_output(['xdotool', 'search', '--name', data]).strip().split()

        for window_id in window_ids:
            window_id = window_id.decode("utf-8")

            # Get the window class to verify it's the correct RuneLite window
            window_class = get_window_class(window_id)
            if window_class and b"net-runelite-client-RuneLite" in window_class:
                # Activate the window using xdotool
                subprocess.call(["xdotool", "windowactivate", window_id])

                # Call xwininfo to get the detailed window geometry
                window_info = subprocess.check_output(["xwininfo", "-id", window_id], text=True)

                # Extracting absolute upper-left position (X, Y)
                abs_x, abs_y = None, None
                for line in window_info.splitlines():
                    if line.startswith("  Absolute upper-left X:"):
                        abs_x = int(line.split(":")[1].strip())
                    elif line.startswith("  Absolute upper-left Y:"):
                        abs_y = int(line.split(":")[1].strip())

                # Extracting width and height
                width, height = None, None
                for line in window_info.splitlines():
                    if line.startswith("  Width:"):
                        width = int(line.split(":")[1].strip())
                    elif line.startswith("  Height:"):
                        height = int(line.split(":")[1].strip())

                if abs_x is None or abs_y is None or width is None or height is None:
                    print("Error: Could not extract all necessary window information.")
                    return None, None, None, None

                # Subtract 30 pixels from the width for the side border
                width -= 30

                # Output the adjusted geometry
                print("Adjusted Coordinates and size:", abs_x, abs_y, width, height)
                return abs_x, abs_y, width, height

    except subprocess.CalledProcessError as e:
        print(f"Error in subprocess: {e}")
        return None, None, None, None

        print("Main window not found.")
        return None, None, None, None
    except subprocess.CalledProcessError as e:
        print(f"Error while getting window geometry: {e}")
        return None, None, None, None

# def findWindow_runelite():  # find window name returns PID of the window
#     global hwnd
#     # Use xdotool to search and manipulate the Runelite window
#     subprocess.call(["xdotool", "search", "--name", "RuneLite", "windowfocus", "%2"])
#     subprocess.call(["xdotool", "getwindowfocus", "windowmove", "0", "0"])
#     subprocess.call(["xdotool", "getwindowfocus", "windowsize", "865", "830"])
#
#
# def findWindow_openosrs():  # find window name returns PID of the window
#     global hwnd
#     # Use xdotool to search and manipulate the OpenOSRS window
#     subprocess.call(["xdotool", "search", "--name", "OpenOSRS", "windowfocus", "%2"])
#     subprocess.call(["xdotool", "getwindowfocus", "windowmove", "0", "0"])
#     subprocess.call(["xdotool", "getwindowfocus", "windowsize", "865", "830"])
#
#
# def findWindow(data):  # find window name returns PID of the window
#     global hwnd
#     # Use xdotool to search and manipulate the window by title
#     subprocess.call(["xdotool", "search", "--name", data, "windowfocus", "%2"])
#     subprocess.call(["xdotool", "getwindowfocus", "windowmove", "0", "0"])
#     subprocess.call(["xdotool", "getwindowfocus", "windowsize", "865", "830"])
#
#
# def getWindow(data):  # find window name returns PID of the window
#     global hwnd
#     # Use xdotool to search and focus the window, then get its geometry
#     subprocess.call(["xdotool", "search", "--name", data, "windowfocus", "%2"])
#     rect = subprocess.check_output(["xdotool", "getwindowfocus", "getwindowgeometry"]).decode("utf-8")
#     rect_lines = rect.splitlines()
#     for line in rect_lines:
#         if "Geometry" in line:
#             geom = line.split()[1]
#             x, y, w, h = map(int, geom.split('x'))
#             # Adjust for client window borders
#             x, y, w, h = x + 0, y + 30, w - 50, h - 30
#             return x, y, w, h
#     return 0, 0, 865, 830  # Default if no window found


def printWindows():
    # Use xdotool to list window titles
    windows = subprocess.check_output(["xdotool", "search", "--name", ""]).decode("utf-8")
    window_ids = windows.splitlines()
    for window_id in window_ids:
        title = subprocess.check_output(["xdotool", "getwindowname", window_id]).decode("utf-8").strip()
        if title:
            print(title)


# print('Operating system:', platform.system())
# if platform.system() == 'Linux' or platform.system() == 'Darwin':  # Mac is also Unix-based, so adding 'Darwin'
#     try:
#         findWindow_Linux(data[0]['Config']['client_title'])
#     except BaseException:
#         print("Unable to find window:", data[0]['Config']['client_title'], "Please see list of window names below:")
#         printWindows()
#         pass
# else:
#     try:
#         findWindow(data[0]['Config']['client_title'])
#     except BaseException:
#         print("Unable to find window:", data[0]['Config']['client_title'], "| Please see list of window names below:")
#         printWindows()
#         pass
