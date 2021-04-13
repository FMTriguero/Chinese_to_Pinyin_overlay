import pytest
from ui.ui import *
from main import Application


def test_application_creation():
    ui = UI()
    assert ui is not None


def test_getting_monitor_coordinates():
    ui = UI()
    application = Application(ui)
    application.run()
    expected = {'left': 880, 'top': 440, 'width': 160, 'height': 160}
    assert expected == application.ui.get_monitor_coordinates()

# No idea how to do tests regarding the creation of an app or multi thread applications (test works, but need to close)
