import pytest
from ui.ui import *


def test_application_creation():
    ui = UI()
    assert ui is not None


def test_getting_monitor_coordinates():
    ui = UI()
    ui.initialize()
    expected = {'left': 880, 'top': 440, 'width': 160, 'height': 160}
    assert expected == ui.get_monitor_coordinates()

# No idea how to do tests regarding the creation of an app
