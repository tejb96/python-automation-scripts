import json
from threading import Thread
import numpy as np
import subprocess
import cv2
import pyautogui
import random
import time
import os
import datetime
import pytesseract
import requests
import simplejson
import yaml
from PIL import Image, ImageGrab

import functions
from functions import Image_count
from functions import image_Rec_clicker
from functions import release_drop_item
from functions import drop_item
from functions import invent_crop
from functions import Image_Rec_single
from functions import skill_lvl_up
from functions import spaces
from functions import mini_map_image
from functions import random_combat
from functions import random_quests
from functions import random_skills
from functions import random_inventory
from functions import random_breaks
from functions import find_Object
from functions import xp_gain_check
import core

global hwnd
global iflag
global icoord
iflag = False
global newTime_break
newTime_break = False
global timer
global timer_break
global ibreak

global ex, ibreak, coords, cutting_text, time_left, powerlist, actions, t_end, wood_count, clue_count, invent_count, s_spot
s = requests.session()


class bcolors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR


def gfindWindow(data):
    core.activate_and_resize_window(data)


with open("pybot-config.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

try:
    gfindWindow(data[0]['Config']['client_title'])
except BaseException:
    print("Unable to find window:", data[0]['Config']['client_title'], "| Please see list of window names below:")
    core.printWindows()
    pass

x_win, y_win, w_win, h_win = core.get_window_geometry(data[0]['Config']['client_title'])
print(x_win,y_win,w_win,h_win)

def random_break(start, c):
    global newTime_break
    startTime = time.time()
    # 1200 = 20 minutes
    a = random.randrange(0, 4)
    if startTime - start > c:
        options[a]()
        newTime_break = True


def randomizer(timer_breaks, ibreaks):
    global newTime_break
    global timer_break
    global ibreak
    random_break(timer_breaks, ibreaks)
    if newTime_break == True:
        timer_break = timer()
        ibreak = random.randrange(600, 2000)
        newTime_break = False

    # b = random.uniform(4, 5)


def timer():
    startTime = time.time()
    return startTime


def random_pause():
    global actions
    b = random.uniform(20, 250)
    actions = 'pausing for ' + str(b) + ' seconds'
    time.sleep(b)
    newTime_break = True


iflag = False

options = {0: random_inventory,
           1: random_combat,
           2: random_skills,
           3: random_quests,
           4: random_pause}


# def get_live_info():
#     '''Returns specific live information from the game client via the Status Socket plugin.'''
#     try:
#         f = open('live_data.json', "r+")
#         data = json.load(f)
#         print("get_live_info",data)
#         f.close()
#         return data
#     except:
#         pass
#
#
# def update_pose():
#     c = s.get("http://localhost:8080/events", stream=True)
#     data = simplejson.loads(c.text)
#     print("update_pose",data)
#     pose = data['animation pose']
#     return pose
#
#
# def update_animation():
#     c = s.get("http://localhost:8080/events", stream=True)
#     data = simplejson.loads(c.text)
#     # print(data)
#     animation = data['animation']
#     return animation


# def moveAcross(move):
#     global s_spot
#     if move != 0:
#         if s_spot != 'firespot_draynor_willow':
#             random_breaks(0.1, 3)
#             x = random.randrange(20, 40)
#             y = random.randrange(-5, 5)
#             b = random.uniform(0.1, 0.7)
#             pyautogui.moveTo(743 + x, 110 + y, duration=b)
#             b = random.uniform(0.01, 0.3)
#             pyautogui.click(duration=b, button='left')
#             random_breaks(3, 5)
#             if move > 1:
#                 x = random.randrange(20, 40)
#                 y = random.randrange(-5, 5)
#                 b = random.uniform(0.1, 0.7)
#                 pyautogui.moveTo(743 + x, 110 + y, duration=b)
#                 b = random.uniform(0.01, 0.3)
#                 pyautogui.click(duration=b, button='left')
#                 random_breaks(3, 5)


# def drop_wood(type):
#     global actions
#     actions = "dropping wood"
#     invent_crop()
#     drop_item()
#     image_Rec_clicker(type + '_icon.png', 'dropping item', 5, 5, 0.9, 'left', 10, False)
#     release_drop_item()
#     return "dropping done"


# def firespot(spot):
#     firespots = ['firespot_varrock_wood', 'firespot_draynor_willow', 'firespot_draynor_oak'
#         , 'firespot_farador_oak', 'firespot_draynor_wood', 'firespot_lumbridge_wood']
#
#     xy_firespots = [[45, 55], [50, 40], [30, 35], [25, 20], [25, 20], [-15, -5]]
#     x = xy_firespots[firespots.index(spot)][0]
#     y = xy_firespots[firespots.index(spot)][1]
#     mini_map_image(spot + '.png', x, y, 0.7, 'left', 15, 0)


def invent_enabled():
    return Image_count('inventory_enabled.png', threshold=0.99)


def bank_spot():
    functions.find_Object_precise(1, 0, 0, 860, 775)


def deposit_bank_items(type):
    global actions
    bank = Image_count('bank_deposit.png', 0.75)
    if bank > 0:
        functions.deposit_all_Bank()
        random_breaks(0.3, 0.5)
        functions.exit_bank()
        if type == 'willow':
            mini_map_image('draynor_bank_spot.png', 0, 75, 0.7, 'left', 10, 10)
            return bank
        if type == 'oak':
            mini_map_image('draynor_bank_spot.png', 45, 40, 0.7, 'left', 10, 10)
            return bank
        mini_map_image('draynor_bank_spot.png', 45, 40, 0.7, 'left', 10, 10)
        return bank
    else:
        actions = "bank not found"
        mini_map_image('draynor_bank_spot.png', 45, 40, 0.8, 'left', 10, 10)
        random_breaks(5, 10)
        bank_spot()
        random_breaks(5, 7)
        return bank


def change_brown_black():
    # Load the aerial image and convert to HSV colourspace
    image = cv2.imread('images/textshot.png')
    # hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # define the list of boundaries
    # BGR
    # Define lower and uppper limits of what we call "brown"
    brown_lo = np.array([0, 0, 0])
    brown_hi = np.array([60, 80, 85])

    # Mask image to only select browns
    mask = cv2.inRange(image, brown_lo, brown_hi)

    # Change image to red where we found brown
    image[mask > 0] = (0, 0, 0)

    cv2.imwrite('images/textshot.png', image)


def resize_quick():
    left = x_win+5
    top = y_win+23
    w = 130
    h = 20

    screenshot_path='images/screen_resize.png'
    screenshot = pyautogui.screenshot(region=(left, top, w, h))
    screenshot.save(screenshot_path)
    print(f"Screenshot saved as '{screenshot_path}'")

def resizeImage():
    resize_quick()
    png = 'images/screen_resize.png'
    im = Image.open(png)
    # saves new cropped image
    width, height = im.size
    new_size = (width * 4, height * 4)
    im1 = im.resize(new_size)
    im1.save('images/textshot.png')


def Image_to_Text(preprocess, image, parse_config='--psm 7'):
    resizeImage()
    change_brown_black()
    # construct the argument parse and parse the arguments
    image = cv2.imread('images/' + image)
    image = cv2.bitwise_not(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # check to see if we should apply thresholding to preprocess the
    # image
    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # make a check to see if median blurring should be done to remove
    # noise
    if preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)

    if preprocess == 'adaptive':
        gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    with Image.open(filename) as im:
        text = pytesseract.image_to_string(im, config=parse_config)
    os.remove(filename)
    print("line 289",text)
    return text


def doFireMaking(type):
    global invent_count, wood_count, actions, clue_count
    wood_burned = 0

    # Continue until we have enough wood
    while wood_count > 0:
        actions = 'Burning Wood'
        clue_count = Image_count('clue_nest.png')
        wood_count = Image_count(type + '_icon.png')
        invent_count = wood_count + clue_count

        # Simulate the random breaks
        random_breaks(0.1, 2)

        # Light the fire first (only the first time)
        if wood_burned == 0:  # Check if it's the first time lighting a fire
            walk_here=False
            if not walk_here:
                walk_here = functions.find_Image('images/walk_here.png', 0, 100, 800, 700)
            random_breaks(1, 4)
            Image_Rec_single('tinderbox.png', 'lighting fire', 2, 2, 0.9, 'left', 8, False)
            random_breaks(0.5, 1)
            Image_Rec_single(type + '_icon.png', 'lighting fire', 5, 5, 0.9, 'left', 8, False)
            c = random.uniform(0.9, 2)
            time.sleep(c)
            fire = False
            time_start = time.time()
            time_end = 0

            wood_burned += 1

        # Now, continue to add logs to the fire (this part will be done after fire is lit)
        actions = 'Adding logs to fire'

        if wood_count > 0 and wood_burned==1:  # Check if there are any logs available
            # print("Adding log to fire")  # Debugging log
            log_selected=False
            while not log_selected:
                log_selected=Image_Rec_single(type + '_icon.png', 'lighting fire', 5, 5, 0.9, 'left', 8, False)
                # print('line331',log_selected)
            time.sleep(10)
            # Click on the fire to trigger the log prompt (ensure the image is being found correctly)
            # print('Running find image for fire')  # Debugging log
            found = False
            while not found:
                found = functions.find_Image('images/fire.png', 5, 100, 550, 525)



            # Randomly click anywhere in the prompt area (x=212, y=790, w=96, h=69)
            time.sleep(3)
            prompt_area_x = random.randint(212, 212 + 96)
            prompt_area_y = random.randint(790, 790 + 69)
            # pyautogui.click(prompt_area_x, prompt_area_y)
            pyautogui.moveTo(prompt_area_x, prompt_area_y, duration=random.uniform(0.1, 0.9))
            pyautogui.click(duration=random.uniform(0.01, 0.05))
            print("Log added")  # Debugging log

            time.sleep(2)  # Adjust time to ensure actions have enough time to process

            # Reduce the number of logs in the inventory

            actions = f'Added log {wood_burned} to fire'

        # Wait between actions to mimic human behavior (prevents bot detection)
        # random_breaks(0.1, 1)
        done=random.randint(70,90)
        time.sleep(done)
        wood_count=0
        # Break if no more wood is available
        if wood_count <= 0:
            if skill_lvl_up() != 0:
                actions = 'leveled up...'
                random_breaks(0.2, 3)
                pyautogui.press('space')
                random_breaks(0.1, 3)
                pyautogui.press('space')
                a = random.randrange(0, 2)
                # print(a)
                spaces(a)
            else:
                break

    actions = 'Finished Adding Logs to Fire'


# def doBanking(type):
#     global actions
#     invent = invent_enabled()
#     if invent == 0:
#         actions = 'open inventory'
#         pyautogui.press('esc')
#     mini_map_image('draynor_bank_spot.png', 10, 40, 0.8, 'left', 10, 10)
#     time.sleep(1)
#     if plugins_enabled:
#         waitforaction(808)
#     else:
#         random_breaks(9.5, 11)
#     random_breaks(0, 2)
#     bank_spot()
#     time.sleep(1)
#     if plugins_enabled:
#         waitforaction(808)
#     else:
#         random_breaks(2, 5)
#     random_breaks(0, 2)
#     bank = deposit_bank_items(type)
#     time.sleep(1)
#     if plugins_enabled:
#         waitforaction(808)
#     else:
#         random_breaks(9.5, 11)
#     random_breaks(0, 2)
#     while bank == 0:
#         bank = deposit_bank_items(type)
#     random_breaks(0, 1)


# def waitforaction(num):
#     global actions
#     get_live_info()
#     pose = update_pose()
#     while pose != num:
#         time.sleep(0.1)
#         actions = "moving - " + str(pose)
#         pose = update_pose()


def doCutting(cutting, color, Take_Human_Break):
    global cutting_text, actions, coords
    cutting=cutting.strip().lower()

    if skill_lvl_up() != 0:
        actions = 'leveled up...'
        random_breaks(0.2, 3)
        pyautogui.press('space')
        random_breaks(0.1, 3)
        pyautogui.press('space')
        a = random.randrange(0, 2)
        # print(a)
        spaces(a)

    elif cutting != 'woodcutting' and cutting != 'uoodcutting' and cutting != 'voodcutting' and cutting != 'joodcuttine' and cutting != 'foodcuttir' and cutting != 'foodcuttin' and cutting != 'joodcuttinc' or cutting == 'NOT woodcutting'or cutting== 'Not woodcutting' or cutting == 'not woodcutting':
        cutting_text = 'Not Cutting'
        random_breaks(0.2, 3)
        coords = find_Object(color, 0, 100, 800, 700)

    cutting_text = cutting
    if coords:
        print("sleeping for 38s")
        click_tree=random.randrange(38,65)
        time.sleep(click_tree)
    else:
        time.sleep(2)

    if Take_Human_Break:
        c = random.triangular(0.1, 5, 0.5)
        time.sleep(c)


def timer_countdown():
    global Run_Duration_hours
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    # print(t_end)
    final = round((60 * 60 * Run_Duration_hours) / 1)
    # print(final)
    for i in range(final):
        # the exact output you're looking for:
        print(bcolors.OK + f'\r[%-10s] %d%%' % ('=' * round((i / final) * 10), round((i / final) * 100)),
              f'time left: {(t_end - time.time()) / 60 :.2f} mins | coords: {coords} | status: {cutting_text} | wood: {wood_count} | clues: {clue_count} | {actions}',
              end='')
        time.sleep(1)
        if ex:
            exit()


def count_items():
    global Run_Duration_hours
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    while time.time() < t_end:
        global wood_type, powerlist, wood_count, mined_text, clue_count, ex
        wood_count = int(Image_count(wood_type + '_icon.png'))
        clue_count = int(Image_count('clue_nest.png'))
        time.sleep(0.1)
        if ex:
            exit()


def print_progress(time_left, coords, cutting_text, wood_count, clue_count, actions):
    print(bcolors.OK +
          f'\rtime left: {time_left} | coords: {coords} | status: {cutting_text} | wood: {int(wood_count)} '
          f'| clues: {int(clue_count)} | {actions}',
          end='')


def powercutter(color=0, type='wood', action_taken='none', spot='', Take_Human_Break=False,
                Run_Duration_hours=6):
    global ex, ibreak, coords, cutting_text, time_left, powerlist, actions, t_end, wood_count, clue_count, invent_count, s_spot
    s_spot = spot
    powerlist = ['wood', 'oak', 'willow', 'maple', 'yew', 'magic', 'red']
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    wood_type = type
    print('Will break in: %.2f' % (ibreak / 60) + ' minutes |', "Wood Type Selected:", wood_type, "| Action Taken:",
          action_taken)
    t1 = Thread(target=timer_countdown)
    t1.start()
    date_time = datetime.datetime.fromtimestamp(t_end)
    # print(date_time)
    if action_taken == 'bank':
        if int(Image_count('tinderbox.png')) > 0:
            print('\n' + bcolors.FAIL + 'Tinderbox found, remove from inventory to bank wood \n')
            ex = True
            exit()
    if action_taken == 'firemake':
        inv = 26
        if spot == '':
            print(
                '\n' + bcolors.FAIL + ' ↓ Pick Below, No firespot selected, add firespot to spot value and restart script \n' +
                'firespot_varrock_wood \nfirespot_draynor_willow \nfirespot_draynor_oak' +
                '\nfirespot_farador_oak \nfirespot_draynor_wood \nfirespot_lumbridge_wood')
            ex = True
            exit()
        if int(Image_count('tinderbox.png')) == 0:
            print('\n' + bcolors.FAIL + 'No Tinderbox found, add to inventory in the first slot \n')
            ex = True
            exit()
    else:
        inv = 27
    while time.time() < t_end:
        actions = 'None'
        randomizer(timer_break, ibreak)
        invent = functions.invent_enabled()
        if invent == 0:
            actions = 'opening inventory'
            pyautogui.press('esc')
        # invent_crop()
        clue_count = Image_count('clue_nest.png')
        wood_count = Image_count(type + '_icon.png')
        invent_count = wood_count + clue_count
        # print("wood: ", invent_count)
        if invent_count > inv:
            if action_taken == 'firemake':
                doFireMaking(type)
            # if action_taken == 'bank':
            #     doBanking(type)
            random_breaks(0.2, 5)
            # drop_wood(type)
            random_breaks(0.2, 5)
        cutting_text = Image_to_Text('thresh', 'textshot.png')
        # print(cutting_text)
        doCutting(cutting_text, color, Take_Human_Break)




ex = False
coords = (0, 0)
actions = 'None'
cutting_text = 'Not Cutting'
time_left = 0
s_spot = ''
# -------------------------------

invent_count = 0
wood_type = 'wood'
wood_count = 0
bird_count = 0
clue_count = 0
# -------------------------------


if __name__ == "__main__":
    x_start = random.randrange(100, 450)
    y_start = random.randrange(200, 500)
    pyautogui.click(x_start, y_start, button='right')

    ibreak = random.randrange(60, 121)
    timer_break = timer()
    # ----- OBJECT MARKER COLOR ------
    red = 0
    yellow = 2
    green = 1
    purple = 3
    blue = 4
    plugins_enabled = False
    # ----- LIST OF WOOD TYPES --------
    powerlist = ['wood', 'oak', 'willow', 'maple', 'yew', 'magic', 'red']

    # --------- CHANGE TO RUN FOR AMOUNT OF HOURS ----------------
    Run_Duration_hours = 0.5

    # ---------- CHOOSE ACTION TAKEN ------------
    woodcut_and_firemake = 'firemake'  # only works at draynor cuts and deposits wood at bank, make sure to pick firespot

    bank_and_woodcut = 'bank'  # only works at draynor cuts and deposits wood at bank

    just_woodcut = 'woodcut'  # woodcutting only drops wood on full inventory

    firespots = ['firespot_varrock_wood', 'firespot_draynor_willow', 'firespot_draynor_oak'
        , 'firespot_draynor_wood', 'firespot_lumbridge_wood']

    powercutter(red, 'willow', action_taken=woodcut_and_firemake,
                spot='firespot_draynor_willow',
                Take_Human_Break=True, Run_Duration_hours=Run_Duration_hours)