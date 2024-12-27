import datetime
from threading import Thread
import core
import yaml

import functions
from functions import Image_count, invent_enabled
from functions import image_Rec_clicker
from functions import screen_Image
from functions import release_drop_item
from functions import drop_item
from functions import Image_to_Text
from functions import invent_crop
from functions import resizeImage
from PIL import ImageGrab
from functions import find_Object_precise

from functions import random_combat
from functions import random_quests
from functions import random_skills
from functions import random_inventory
from functions import random_breaks

import numpy as np
import cv2
import time
import random
import pyautogui

global hwnd
global iflag
global icoord
iflag = False
global newTime_break
newTime_break = False
global timer
global timer_break
global ibreak
import slyautomation_title


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
    b = random.uniform(20, 250)
    print('pausing for ' + str(b) + ' seconds')
    time.sleep(b)
    newTime_break = True


options = {0: random_inventory,
           1: random_combat,
           2: random_skills,
           3: random_quests,
           4: random_pause}


def Miner_Image_quick():
    left = 150
    top = 150
    right = 600
    bottom = 750

    im = ImageGrab.grab(bbox=(left, top, right, bottom))
    im.save('images/miner_img.png', 'png')


def Miner_Image():
    screen_Image(150, 150, 600, 750, 'images/miner_img.png')


# def drop_ore(ore_type):
#     global actions
#     actions = "drop ore."
#     invent_crop()
#     drop_item()
#     if ore_type == 5:
#         image_Rec_clicker(r'clay_ore.png', 'dropping item', threshold=0.8, playarea=False)
#
#     if ore_type== 3:
#         image_Rec_clicker(r'iron_ore.png', 'dropping item', threshold=0.8, playarea=False)
#
#     # image_Rec_clicker(r'copper_ore.png', 'dropping item', threshold=0.8, playarea=False)
#     #
#     # image_Rec_clicker(r'coal_ore.png', 'dropping item', threshold=0.8, playarea=False)
#     #
#     # image_Rec_clicker(r'tin_ore.png', 'dropping item', threshold=0.8, playarea=False)
#     release_drop_item()
#     # print("dropping ore done")
#     return "drop ore done"


def findarea_single(ore, cropx, cropy):
    Miner_Image_quick()
    image = cv2.imread(r"images/miner_img.png")

    # B, G, R
    # --------------------- ADD OBJECTS -------------------
    tin = ([103, 86, 65], [145, 133, 128])
    copper = ([35, 70, 120], [65, 110, 170])
    coal = ([20, 30, 30], [30, 50, 50])
    iron = ([15, 20, 40], [25, 40, 70])
    iron2 = ([17, 20, 42], [25, 38, 70])
    clay = ([50, 105, 145], [60, 125, 165])
    red = ([0, 0, 180], [80, 80, 255])
    green = ([0, 180, 0], [80, 255, 80])
    amber = ([0, 160, 160], [80, 255, 255])
    # --------------------- ADD OBJECTS -------------------
    ore_list = [tin, copper, coal, iron, iron2, clay, red, green, amber]
    boundaries = [ore_list[ore]]
    # loop over the boundaries
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)
        ret, thresh = cv2.threshold(mask, 40, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        # find the biggest countour (c) by the area
        c = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(c)
        x = random.randrange(x + 5, x + max(w - 5, 6)) + cropx  # 950,960
        # print('x: ', x)
        y = random.randrange(y + 5, y + max(h - 5, 6)) + cropy  # 490,500
        # print('y: ', y)
        b = random.uniform(0.1, 0.3)
        pyautogui.moveTo(x, y, duration=b)
        b = random.uniform(0.07, 0.11)
        pyautogui.click(duration=b)
        return (x, y)


def count_gems():
    return Image_count('gem_icon.png')


def count_geo():
    return Image_count('geo_icon.png')


def count_gems2():
    return Image_count('gem_icon2.png')


def inv_count(name):
    return Image_count(name + '_ore.png')


def timer_countdown():
    global Run_Duration_hours
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    # print(t_end)
    final = round((60 * 60 * Run_Duration_hours) / 1)
    # print(final)
    for i in range(final):
        # the exact output you're looking for:
        print(bcolors.OK + f'\r[%-10s] %d%%' % ('=' * round((i / final) * 10), round((i / final) * 100)),
              f'time left: {(t_end - time.time()) / 60 :.2f} mins | coords: {spot} | status: {mined_text} | ore: {ore_count} | gems: {gem_count} | clues: {clue_count} | {actions}',
              end='')
        time.sleep(1)

def determine_position_to_bank():
    global ore_count, gem_count, clue_count, actions
    if ore_count + gem_count + clue_count < 27:
        return 4
    if functions.mini_map_bool('port_sarim_spot_water.png', 0.85):
        actions = 'player located @ step 2'
        return 2
    if functions.mini_map_bool('port_sarim_jewl.png', 0.85):
        actions = 'player located @ step 1'
        return 1
    if functions.mini_map_bool('rim_mine_spot1.png', 0.85):
        actions = 'player located @ step 0'
        return 0
    else:
        return 0

def determine_position_to_clay():
    global ore_count, gem_count, clue_count, actions
    gem_count = int(count_gems() + count_gems2())
    ore_count = int(inv_count('clay'))
    clue_count = int(count_geo())
    if ore_count + gem_count + clue_count > 27:
        return 6
    if functions.mini_map_bool('clay_deposit_spot1.png', 0.85):
        actions = 'player located @ step 1 Spot 5 _1'
        return 0
    if functions.mini_map_bool('clay_deposit_spot4.png', 0.85):
        actions = 'player located @ step 1 Spot 5 _4'
        return 0
    if functions.mini_map_bool('clay_deposit_spot5.png', 0.85):
        actions = 'player located @ step 1 Spot 5 _5'
        return 1
    if functions.mini_map_bool('clay_deposit_spot3.png', 0.85):
        actions = 'player located @ step 1 Spot 5 _3'
        return 1
    if functions.mini_map_bool('clay_deposit_spot2.png', 0.85):
        actions = 'player located @ step 1 Spot 5 _2'
        return 1
    if functions.mini_map_bool('port_sarim_spot_water.png', 0.85):
        actions = 'player located @ step 2'
        return 2
    if functions.mini_map_bool('port_sarim_jewl.png', 0.85):
        actions = 'player located @ step 3'
        return 3
    if functions.mini_map_bool('rim_mine_spot1.png', 0.85):
        actions = 'player located @ step 4'
        return 5
    if functions.mini_map_bool('bank_deposit.png', 0.85):
        actions = 'player located @ step 0'
        return 0
    else:
        return 0

def find_banker():
    find_Object_precise(0, 0, 0, 700, 800)  # red

def depositbox():
    global actions
    if functions.Image_count('bank_deposit.png', 0.8, 0, 0, 700, 800) > 0:
        b = random.uniform(0.1, 0.65)
        x = random.randrange(370, 390)  # 950,960
        y = random.randrange(440, 460)  # 490,500
        pyautogui.moveTo(x, y, duration=b)
        b = random.uniform(0.01, 0.1)
        pyautogui.click(duration=b)
        actions = 'successful deposit...'
        c = random.uniform(0.1, 1)
        time.sleep(c)
        gem_count = int(count_gems() + count_gems2())
        ore_count = int(inv_count('clay'))
        clue_count = int(count_geo())
        total_invent = gem_count + ore_count + clue_count
        if total_invent > 0:
            return False
        return True
    actions = 'deposit box not found...'
    return False

def rim_minetobank():
    global actions
    step = 0
    step = determine_position_to_bank()
    c = random.uniform(14, 15)
    x = 60
    y = 25
    if step == 0:
        while functions.mini_map_image('rim_mine_spot1.png', x, y, 0.8, 'left') != True:
            actions = 'finding 1st step to bank'
        time.sleep(c)
        actions = '1st step to bank'
        step = 1

    c = random.uniform(9, 10)
    x = 10
    y = 1
    if step == 1:
        # while functions.mini_map_image('port-sarim-step2.png', x, y, 0.8, 'left') != True:
        pyautogui.click(duration=2)
        actions = 'finding 2nd step to bank'
        time.sleep(c)
        actions = '2nd step to bank'
        step=2

    c = random.uniform(9, 10)
    x = 50
    y = -25

    if step == 2:
        # while functions.mini_map_image('port_sarim_spot_water.png', x, y, 0.8, 'left') != True:
        #     actions = "finding 4th step to bank"
        rx=random.uniform(0.1,0.9)
        pyautogui.click(815+rx,125+rx)
        time.sleep(c)
        actions = '4th step to bank'
        step = 3

    if step == 3:
        b = random.uniform(0.175, 0.677)
        x = random.randrange(750, 755)
        #print('x: ', x)
        y = random.randrange(175, 180)
        #print('y: ', y)
        c = random.uniform(10, 12)
        pyautogui.click(x, y, 1, duration=b, button='left')
        time.sleep(c)
        actions = '5th step to bank'
        b = random.uniform(0.175, 0.677)
        x = random.randrange(750, 755)  # 1755,1765
        #print('x: ', x)
        y = random.randrange(140, 145)  # 175,185
        #print('y: ', y)
        c = random.uniform(9, 10)
        pyautogui.click(x, y, 1, duration=b, button='left')
        actions = 'last step to bank'
        time.sleep(c)
        c = random.uniform(2.1, 3)
        find_banker()
        actions = 'finding deposit box'
        time.sleep(c)
        while not depositbox():
            c = random.uniform(2.1, 3)
            find_banker()
            actions = 'finding deposit box'
            time.sleep(c)
        actions = 'finished deposit end of function'
        c = random.uniform(1, 5)
        time.sleep(c)
        step = 4

def count_items():
    global Run_Duration_hours
    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    while time.time() < t_end:
        global ore, powerlist, ore_count, mined_text, gem_count, clue_count
        gem_count = int(count_gems() + count_gems2())
        ore_count = int(inv_count(powerlist[ore]))
        clue_count = int(count_geo())
        time.sleep(0.1)


def print_progress(time_left, spot, mined_text, powerlist, ore, actions):
    print(bcolors.OK +
          f'\rtime left: {time_left} | coords: {spot} | status: {mined_text} | ore: {int(inv_count(powerlist[ore]))} | gems: {int(count_gems() + count_gems2())} | clues: {int(count_geo())} | {actions}',
          end='')


def powerminer_text(ore, num, Take_Human_Break=False, Run_Duration_hours=5):
    global spot, mined_text, time_left, powerlist, actions, powerlist, t_end, gem_count, ore_count, clue_count

    powerlist = ['tin', 'copper', 'coal', 'iron', 'gold', 'clay', 'red', 'green', 'amber']
    print("Will break in: %.2f" % (ibreak / 60) + " minutes |", "Mine Ore Selected:", powerlist[ore])
    t1 = Thread(target=timer_countdown)
    t1.start()
    spot = (0, 0)
    actions = 'None'
    mined_text = 'Not Mining'

    t_end = time.time() + (60 * 60 * Run_Duration_hours)
    while time.time() < t_end:
        invent = invent_enabled()
        if invent == 0:
            actions = 'opening inventory'
            pyautogui.press('esc')
        time_left = str(datetime.timedelta(seconds=round(t_end - time.time(), 0)))
        actions = 'None'
        randomizer(timer_break, ibreak)
        r = random.uniform(0.1, 5)
        gem_count = int(count_gems() + count_gems2())
        ore_count = int(inv_count(powerlist[ore]))
        clue_count = int(count_geo())
        # inventory = int(inv_count(powerlist[ore])) + int(count_gems()) + int(count_gems2()) + int(count_geo())
        inventory = gem_count + ore_count + clue_count
        # print_progress(time_left, spot, mined_text, powerlist, ore, actions)
        if inventory > 27:
            rim_minetobank()
        mined_text = Image_to_Text('thresh', 'textshot.png')
        print('260',mined_text)
        # print_progress(time_left, spot, mined_text, powerlist, ore, actions)
        if mined_text.strip().lower() != 'mining' and mined_text != 'Mininq' or mined_text == 'NOT mining':
            # mined_text = 'Not Mining'
            # print_progress(time_left, spot, mined_text, powerlist, ore, actions)
            # random_breaks(0.05, 0.1)
            spot = findarea_single(num, 150, 150)
            if Take_Human_Break:
                c = random.triangular(0.05, 6, 0.5)
                time.sleep(c)
        else:
            mined_text = 'Mining'
        # print_progress(time_left, spot, mined_text, powerlist, ore, actions)


spot = (0, 0)
actions = 'None'
mined_text = 'Not Mining'
time_left = 0

# -------------------------------

powerlist = ['tin', 'copper', 'coal', 'iron', 'gold', 'clay', 'red', 'green', 'amber']

ore_count = 0
gem_count = 0
clue_count = 0
# -------------------------------

if __name__ == "__main__":
    x = random.randrange(100, 250)
    y = random.randrange(400, 500)
    pyautogui.click(x, y, button='right')
    ibreak = random.randrange(300, 2000)
    timer_break = timer()

    # ----- ORE -------
    tin = 0
    copper = 1
    coal = 2
    iron = 3
    gold = 4
    clay = 5

    # ----- OBJECT MARKER COLOR ------
    red = 6
    green = 7
    amber = 8

    # --------- CHANGE TO RUN FOR AMOUNT OF HOURS ----------------
    Run_Duration_hours = 1

    # | ore | marker color | take break | how long to run for in hours
    powerminer_text(iron, red, Take_Human_Break=True, Run_Duration_hours=Run_Duration_hours)

    # os.system('shutdown -s -f')