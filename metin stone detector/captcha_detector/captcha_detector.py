import time
import pydirectinput as pyd
import easyocr
import re
from image_processor import ImageProcessor
from window import WindowCapture
import os

# read image
window_name = "Velor2 | Power of the Elements"

wincap = WindowCapture(window_name)
improc = ImageProcessor

list_of_items = ["bow", "armor", "bracelet", "earrings", "bell", "helmet", "necklace", "chest", "fan", "shoes", "sword",
                 "shield", "daggers"]
text_pos_x = 315
text_pos_y = 245
text_width = 190
text_height = 15


def get_item_name(img):
    cropped_img = wincap.crop_captcha_image(img, text_pos_x, text_pos_y, text_width, text_height)
    reader = easyocr.Reader(['en'], gpu=False)
    text_ = reader.readtext(cropped_img)

    detected_texts = [text for (_, text, _) in text_]

    pattern = r'\w+'
    words = re.findall(pattern, detected_texts[0])

    return words[-1]


def press_captcha_item(img):
    initialize_captcha_processor()
    item_name = get_item_name(img)
    coordinates = improc.proccess_image(img)
    window_w, window_h, window_x, window_y = wincap.get_window_size()

    for coordinate in coordinates:
        if coordinate['class_name'] == item_name:
            center_x = coordinate['x'] + coordinate['w'] // 2 + 10
            center_y = coordinate['y'] + coordinate['h'] // 2 + 10
            click_x = int(window_x + center_x)
            click_y = int(window_y + center_y)

            pyd.moveTo(click_x, click_y)
            pyd.leftClick(click_x, click_y)
            time.sleep(1)


def initialize_captcha_processor():
    global improc

    cwd = os.getcwd()
    cfg_file_name_path = os.path.abspath(os.path.join(cwd, 'captcha_detector', 'yolov4-tiny', 'yolov4-tiny-custom.cfg'))
    names_file_path = os.path.abspath(os.path.join(cwd, 'captcha_detector', 'yolov4-tiny', 'obj.names'))

    weights_file_name_path = os.path.abspath(os.path.join(cwd, 'captcha_detector', 'yolov4-tiny-custom_last.weights'))

    improc = ImageProcessor(wincap.get_window_size(), cfg_file_name_path, weights_file_name_path, names_file_path)
