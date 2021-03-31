from ui.ui import *


class Application:

    def __init__(self, ui=None):
        self.ui = ui

    def run(self):
        return


def main():
    ui = UI()
    application = Application(ui)


if __name__ == '__main__':
    main()
