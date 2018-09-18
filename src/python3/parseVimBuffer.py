#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import vim
import re
import yaml

from qiitaPyError import QiitaPyNoItem

def getArticle():
    data = {}

    pattern = re.compile("---\s*$")

    # get title, tags, and othor options
    line = 0
    if pattern.match(vim.current.buffer[0]):
        for idx, buf in enumerate(vim.current.buffer[1:]):
            if pattern.match(buf):
                line = idx + 1
                break

        if line != 0:
            data = yaml.load("\n".join(vim.current.buffer[1:line]))

        tags = []
        for item in data["tags"]:
            if type(item) is str:
                tags.append({"name": item, "versions": ["0.0.1"]})
            elif type(item) is dict:
                tags.append({"name": list(item.keys())[0], "versions": [str(list(item.values())[0])]})
            else:
                tags.append(item)
        data["tags"] = tags

    # set an article
    data["body"] = "\n".join(vim.current.buffer[line+1:])

    # set title
    if "title" not in data or type(data["title"]) is not str:
        raise QiitaPyNoItem("title")

    # set tags
    if "tags" not in data or type(data["tags"]) is not list:
        raise QiitaPyNoItem("tags")

    # set tweet
    if "tweet" not in data or type(data["tweet"]) is not bool:
        raise QiitaPyNoItem("tweet")

    return data

