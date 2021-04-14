from ui.ui import *

from threading import Thread
from PIL import Image

import mss
import keyboard
import numpy as np
import time


class Camera:
    def __init__(self):
        self.bounds = []
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]

    def take_screenshot(self):
        screenshot = self.sct.grab(self.monitor)
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


class Application:

    def __init__(self, ui=None, camera=None):
        self.ui = ui
        self.camera = camera
        self.running = True
        self.exit_code = None

    def run(self):
        thread = Thread(target=self.loop_ui, daemon=True)
        thread.start()
        self.ui.initialize()

    def loop_ui(self):
        time.sleep(1)
        print("Set the bounds of the screen, press space once done")
        keyboard.wait("space")
        self.camera.bounds = self.ui.get_monitor_bounds()
        print(self.camera.bounds)

        while self.running:
            print("press enter to take screenshot")
            keyboard.wait("enter")
            image = self.camera.get_numpy_screenshot()


def main():
    ui = UI()
    camera = Camera()
    application = Application(ui, camera)
    application.run()


if __name__ == '__main__':
    main()
