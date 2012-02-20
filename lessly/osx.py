#!/usr/bin/env python
# -*- coding: utf-8 -*-

import plistlib
import site
site.addsitedir('/System/Library/Frameworks/Python.framework/Versions/2.6/Extras/lib/python')

import appscript, objc, PyObjCTools, Foundation, ScriptingBridge
from Foundation import *
from ScriptingBridge import *


def getApp(identifier):
    return SBApplication.applicationWithBundleIdentifier_(identifier)


iTunes = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
library = iTunes.sources()[0].libraryPlaylists()[0]

del site # remove site from __all__
