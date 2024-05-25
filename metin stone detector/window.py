import numpy as np
import win32gui, win32ui, win32con


class WindowCapture:
    w = 0
    h = 0
    x = 0
    y = 0
    hwnd = None

    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]
        self.x, self.y = window_rect[:2]

        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

    def get_screenshot(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[..., :3]
        img = np.ascontiguousarray(img)

        return img

    def get_window_size(self):
        return self.w, self.h, self.x, self.y

    def set_foreground_window(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)  # Ensure the window is visible
        win32gui.SetForegroundWindow(self.hwnd)

    def crop_captcha_image(self, img, pos_x, pos_y, width, height):
        # Ensure the coordinates and dimensions are within the bounds of the image
        max_y, max_x = img.shape[:2]

        if pos_x + width > max_x or pos_y + height > max_y:
            raise ValueError("The cropping dimensions exceed the image boundaries.")

        cropped_image = img[pos_y: pos_y + height, pos_x: pos_x + width]

        return cropped_image