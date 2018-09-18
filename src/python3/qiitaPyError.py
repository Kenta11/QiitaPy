#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import sys

class QiitaPyCommandError(Exception):
    def __init__(self, command = ""):
        sys.stderr.write("ERROR: The command {} doesn't exist.".format(command))

class QiitaPyNoItem(Exception):
    def __init__(self, item = "item"):
        sys.stderr.write("ERROR: There is no {}.".format(item))

