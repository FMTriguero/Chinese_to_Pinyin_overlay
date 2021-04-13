from ui.ui import *

from threading import Thread

import mss
import keyboard


class Camera:
    def __init__(self):
        self.bounds = []
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]

        self.image = None

    def set_bounds(self, bounds):
        self.bounds = bounds

    def take_screenshot(self):
        self.image = self.sct.grab(self.monitor)


class Application:

    def __init__(self, ui=None):
        self.ui = ui
        self.running = True
        self.exit_code = None

    def run(self):
        thread = Thread(target=self.loop_ui, daemon=True)
        thread.start()
        self.ui.initialize()

    def loop_ui(self):
        while self.running:
            input("wait")


def main():
    ui = UI()
    application = Application(ui)
    application.run()


if __name__ == '__main__':
    main()
