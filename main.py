from ui.ui import *
from Camera.camera import Camera

from threading import Thread

import keyboard

import time


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
