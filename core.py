import subprocess
import yaml
import platform

global hwnd
hwnd = 0

with open("pybot-config.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)


def findWindow_Linux(data):
    # Use xdotool to search for the window by name and focus it
    subprocess.call(["xdotool", "search", "--name", data, "windowfocus", "%2"])
    subprocess.call(["xdotool", "getwindowfocus", "windowmove", "0", "0"])
    subprocess.call(["xdotool", "getwindowfocus", "windowsize", "865", "830"])


def getWindow_Linux(data):
    # Use subprocess.check_output to capture the window geometry
    try:
        # Focus the window with xdotool
        subprocess.call(["xdotool", "search", "--name", data, "windowfocus"])

        # Get the window geometry as a string
        window_output = subprocess.run(["xdotool", "getwindowfocus", "getwindowgeometry"], capture_output=True, text=True)

        # Parse the output to extract the position and size
        # Example output format: "Position: 61,161 (screen: 0)\nGeometry: 865x830"
        window_info = window_output.stdout.splitlines()  # Access stdout here

        # Print the raw output for debugging
        # print(window_info)

        # Check if we have the expected number of lines
        if len(window_info) < 2:
            print("Unexpected output format.")
            return None, None, None, None

        # Extracting position
        position = window_info[1].split(': ')[1].split(' (')[0].split(',')
        x, y = map(int, position)

        # Extracting geometry
        geometry = window_info[2].split(': ')[1].split('x')
        w, h = map(int, geometry)

        # Output
        # print(f"x: {x}, y: {y}, w: {w}, h: {h}")

        # Adjust for borders (as described in your code)
        y += 30  # Adjust for top border
        w -= 50  # Adjust for side border
        h -= 30  # Adjust for top border

        print("done")
        # Return the coordinates and size
        return x, y, w, h

    except subprocess.CalledProcessError as e:
        print(f"Error while getting window geometry: {e}")
        return None, None, None, None

def findWindow_runelite():  # find window name returns PID of the window
    global hwnd
    # Use xdotool to search and manipulate the Runelite window
    subprocess.call(["xdotool", "search", "--name", "RuneLite", "windowfocus", "%2"])
    subprocess.call(["xdotool", "getwindowfocus", "windowmove", "0", "0"])
    subprocess.call(["xdotool", "getwindowfocus", "windowsize", "865", "830"])


def findWindow_openosrs():  # find window name returns PID of the window
    global hwnd
    # Use xdotool to search and manipulate the OpenOSRS window
    subprocess.call(["xdotool", "search", "--name", "OpenOSRS", "windowfocus", "%2"])
    subprocess.call(["xdotool", "getwindowfocus", "windowmove", "0", "0"])
    subprocess.call(["xdotool", "getwindowfocus", "windowsize", "865", "830"])


def findWindow(data):  # find window name returns PID of the window
    global hwnd
    # Use xdotool to search and manipulate the window by title
    subprocess.call(["xdotool", "search", "--name", data, "windowfocus", "%2"])
    subprocess.call(["xdotool", "getwindowfocus", "windowmove", "0", "0"])
    subprocess.call(["xdotool", "getwindowfocus", "windowsize", "865", "830"])


def getWindow(data):  # find window name returns PID of the window
    global hwnd
    # Use xdotool to search and focus the window, then get its geometry
    subprocess.call(["xdotool", "search", "--name", data, "windowfocus", "%2"])
    rect = subprocess.check_output(["xdotool", "getwindowfocus", "getwindowgeometry"]).decode("utf-8")
    rect_lines = rect.splitlines()
    for line in rect_lines:
        if "Geometry" in line:
            geom = line.split()[1]
            x, y, w, h = map(int, geom.split('x'))
            # Adjust for client window borders
            x, y, w, h = x + 0, y + 30, w - 50, h - 30
            return x, y, w, h
    return 0, 0, 865, 830  # Default if no window found


def printWindows():
    # Use xdotool to list window titles
    windows = subprocess.check_output(["xdotool", "search", "--name", ""]).decode("utf-8")
    window_ids = windows.splitlines()
    for window_id in window_ids:
        title = subprocess.check_output(["xdotool", "getwindowname", window_id]).decode("utf-8").strip()
        if title:
            print(title)


print('Operating system:', platform.system())
if platform.system() == 'Linux' or platform.system() == 'Darwin':  # Mac is also Unix-based, so adding 'Darwin'
    try:
        findWindow_Linux(data[0]['Config']['client_title'])
    except BaseException:
        print("Unable to find window:", data[0]['Config']['client_title'], "Please see list of window names below:")
        printWindows()
        pass
else:
    try:
        findWindow(data[0]['Config']['client_title'])
    except BaseException:
        print("Unable to find window:", data[0]['Config']['client_title'], "| Please see list of window names below:")
        printWindows()
        pass
