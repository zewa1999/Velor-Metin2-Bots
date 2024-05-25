import math
import time
import constants
import pydirectinput as pyd
import threading
from datetime import datetime, timedelta
from window import WindowCapture
from image_processor import ImageProcessor
from captcha_detector import captcha_detector as cd

window_name = "Velor2 | Power of the Elements"
cfg_file_name = "./yolov4-tiny/yolov4-tiny-custom.cfg"
name_file = "./yolov4-tiny/obj.names"
weights_file_name = "yolov4-tiny-custom_last.weights"
is_screenshot_thread_initialized = False

wincap = WindowCapture(window_name)
improc = ImageProcessor(wincap.get_window_size(), cfg_file_name, weights_file_name, name_file)

# thread for pressing a single key continuously
key_press_thread_started = False


def press_key_continuously(key, interval=0.1):
    while True:
        pyd.keyDown('z')
        pyd.keyUp('z')
        time.sleep(interval)


def start_pressing_key(key, interval=0.1):
    global key_press_thread_started
    if not key_press_thread_started:
        thread = threading.Thread(target=press_key_continuously, args=(key, interval))
        thread.daemon = True  # This makes the thread exit when the main program exits
        thread.start()
        key_press_thread_started = True
        return thread
    else:
        print("Key press thread is already running.")
        return None


# bot actions
def press_start_metin(stone):
    wincap.set_foreground_window()
    window_w, window_h, window_x, window_y = wincap.get_window_size()
    center_x = stone['x'] + stone['w'] // 2 + 10
    center_y = stone['y'] + stone['h'] // 2 + 0
    click_x = int(window_x + center_x)
    click_y = int(window_y + center_y)

    pyd.moveTo(click_x, click_y)
    pyd.leftClick(click_x, click_y)


def break_stones(stones):
    wincap.set_foreground_window()
    window_w, window_h, window_x, window_y = wincap.get_window_size()

    for stone in stones:
        center_x = stone['x'] + stone['w'] // 2 + 15
        center_y = stone['y'] + stone['h'] // 2 + 30
        click_x = int(window_x + center_x)
        click_y = int(window_y + center_y)

        add_metin_in_queue(click_x, click_y)

    time.sleep(constants.METIN_STONE_BREAK_TIME_SECONDS)


def add_metin_in_queue(click_x, click_y):
    pyd.moveTo(click_x, click_y)
    pyd.keyDown('shiftleft')
    pyd.rightClick(click_x, click_y)
    pyd.keyUp('shiftleft')


def press_camera_rotate_key():
    wincap.set_foreground_window()
    pyd.keyDown('q')
    time.sleep(2)
    pyd.keyUp('q')


def get_closest_metin():
    window_w, window_h, window_x, window_y = wincap.get_window_size()
    center_x = window_w // 2
    center_y = window_h // 2

    distances = []

    for coordinate in coordinates:
        distance = math.sqrt((center_x - coordinate['x']) ** 2 + (center_y - coordinate['y']) ** 2)
        distances.append((distance, coordinate))

    distances.sort(key=lambda x: x[0])

    return [dist[1] for dist in distances[:10]]


# biologist methods
def deliver_biologist_item():
    window_w, window_h, window_x, window_y = wincap.get_window_size()
    biologist_shop_coordinates = (275 + window_x, 241 + window_y)
    item_coordinate = (495 + window_x, 91 + window_y)
    give_button = (395 + window_x, 273 + window_y)

    wincap.set_foreground_window()
    time.sleep(1)

    pyd.keyDown('f7')
    time.sleep(1)
    pyd.keyUp('f7')

    #go to shop
    # pyd.leftClick(biologist_shop_coordinates[0], biologist_shop_coordinates[1])
    # time.sleep(0.5)
    #
    # #buy item to give to biologist
    # pyd.rightClick(item_coordinate[0], item_coordinate[1])
    # time.sleep(0.5)

    #press give button
    pyd.leftClick(give_button[0], give_button[1])
    time.sleep(1)

    pyd.keyDown('esc')
    time.sleep(1)
    pyd.keyUp('esc')

    pyd.keyDown('esc')
    time.sleep(1)
    pyd.keyUp('esc')

    pyd.keyDown('esc')
    time.sleep(1)
    pyd.keyUp('esc')

    pyd.keyDown('u')
    time.sleep(1)
    pyd.keyUp('u')

# captcha methods

def is_captcha_available():
    for coordinate in coordinates:
        if coordinate['class_name'] == 'stopButton':
            return True
    return False


def press_captcha_start_button():
    window_w, window_h, window_x, window_y = wincap.get_window_size()
    center_x = 400
    center_y = 350
    click_x = int(window_x + center_x)
    click_y = int(window_y + center_y)

    pyd.leftClick(click_x, click_y)
    time.sleep(1)


def run_captcha_script():
    ss = wincap.get_screenshot()
    cd.press_captcha_item(ss)
# main function


biologist_time = datetime.now().replace(minute=0, second=0, microsecond=0)
while True:

    ss = wincap.get_screenshot()
    coordinates = improc.proccess_image(ss)
    press_start_metin(coordinates[0])
    time.sleep(5)

    while is_captcha_available():
        press_captcha_start_button()
        run_captcha_script()
        ss = wincap.get_screenshot()
        coordinates = improc.proccess_image(ss)

        
    while len(coordinates) == 0:
        press_camera_rotate_key()
        ss = wincap.get_screenshot()
        coordinates = improc.proccess_image(ss)
        time.sleep(2)

    thread = start_pressing_key('z', 0.1)
    ss = wincap.get_screenshot()
    coordinates = improc.proccess_image(ss)
    target_coordinates = get_closest_metin()
    break_stones(target_coordinates)
    press_camera_rotate_key()

    current_time = datetime.now()
    if current_time >= biologist_time:
        deliver_biologist_item()
        biologist_time = (biologist_time + timedelta(hours=1))

