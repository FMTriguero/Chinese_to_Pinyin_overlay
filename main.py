from ui.ui import *
from Camera.camera import Camera
from ocr.ocr_main import Ocr

from threading import Thread

import keyboard
import time
import asyncio
import sys


class Application:

    def __init__(self, ui=None, camera=None, ocr=None):
        self.ui = ui
        self.camera = camera
        self.ocr = ocr
        self.running = True
        self.exit_code = None

    def run(self):
        thread = Thread(target=self.loop_ui, daemon=True)
        thread.start()
        exit_code = self.ui.initialize()
        print("Finishing")
        self.running = False
        sys.exit(exit_code)

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
            print("getting results")
            results = asyncio.run(self.ocr.get_results(image))
            print("updating ui")
            self.ui.update(results)
            print("press enter to reset window")
            keyboard.wait("enter")
            self.ui.reset()
            print("reset")
            time.sleep(0.1)


def main():
    ui = UI()
    camera = Camera()
    ocr = Ocr()
    application = Application(ui, camera, ocr)
    application.run()


if __name__ == '__main__':
    main()
