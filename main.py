from ui.ui import *


class Application:

    def __init__(self, ui=None):
        self.ui = ui

    def run(self):
        self.ui.initialize()                #Code works, but requires a new threat to run




def main():
    ui = UI()
    application = Application(ui)
    application.run()


if __name__ == '__main__':
    main()
