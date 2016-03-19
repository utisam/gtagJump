# -*- coding:utf-8 -*-

from gtagJump.PythonNavigator import PythonNavigator
from gtagJump.GtagsNavigator import GtagsNavigator
from gtagJump.EtagsNavigator import EtagsNavigator

navigator = [
    PythonNavigator(),
    GtagsNavigator(),
    EtagsNavigator()
]

keyJumpDef = "F3"
keyJumpRef = "F4"
keyJumpBack = "<Alt>b"
keyJumpNext = "<Alt>n"

historymax = 100

