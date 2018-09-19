#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import sys

class QiitaPyCommandError(Exception):
    def __init__(self, command = ""):
        sys.stderr.write("ERROR: The command {} doesn't exist.\n".format(command))

class QiitaPyNoItem(Exception):
    def __init__(self, item = "item"):
        sys.stderr.write("ERROR: There is no {}.\n".format(item))

class QiitaPyPageError(Exception):
    def __init__(self, page):
        sys.stderr.write("ERROR: page {} is illegal.\n".format(page))

