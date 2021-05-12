from PIL import Image

import mss
import numpy as np


class Camera:
    def __init__(self):
        self.bounds = {}
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]

    def take_screenshot(self):
        screenshot = self.sct.grab(self.bounds)
        return screenshot

    def transform_screenshot_to_np(self, screenshot):
        screenshot = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        image = screenshot.resize((screenshot.size[0], screenshot.size[1]))
        np_image = np.asarray(image.convert("RGB"))
        return np_image

    def get_numpy_screenshot(self):
        screenshot = self.take_screenshot()
        np_screenshot = self.transform_screenshot_to_np(screenshot)
        return np_screenshot
