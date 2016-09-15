# -*- coding:utf-8 -*-

from gtagJump.PythonJediNavigator import PythonJediNavigator
from gtagJump.GtagsNavigator import GtagsNavigator
from gtagJump.EtagsNavigator import EtagsNavigator
from gtagJump.PythonSymtableNavigator import PythonSymtableNavigator

navigator = [
    PythonJediNavigator(),
    GtagsNavigator(),
    EtagsNavigator(),
    PythonSymtableNavigator(),
]

keyJumpDef = "F3"
keyJumpRef = "F4"
keyJumpBack = "<Alt>b"
keyJumpNext = "<Alt>n"

historymax = 100
