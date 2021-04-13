from ui.ui import *
from threading import Thread


class Application:

    def __init__(self, ui=None):
        self.ui = ui
        self.running = False
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
