import pytest
from ui.ui import *


def test_application_creation():
    ui = UI()
    assert ui is not None
