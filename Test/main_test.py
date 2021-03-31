import pytest

from main import *
from ui.ui import *


def test_application_creation():
    application = Application()
    assert application is not None


def test_application_ui_creation():
    ui = UI()
    application = Application(ui)
    assert application.ui is not None
