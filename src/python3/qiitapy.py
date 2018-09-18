#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import sys
import os
from getpass import getpass

from qiita_v2.client import QiitaClient

from qiitaPyError import QiitaPyCommandError
from parseVimBuffer import getArticle

POST_SUCCESS = 201

config_file_path = os.path.expanduser("~/.qiita-py.yaml")
client = None

def qiitaPy(command):
    if command == "config":
        qiitaPyConfig()
    elif command == "post":
        qiitaPyPost()
    elif command == "edit":
        qiitaPyEdit()
    elif command == "list":
        qiitaPyList()
    elif command == "delete":
        qiitaPyDelete()
    else:
        raise QiitaPyCommandError(command)

def qiitaPyConfig():
    vim.command("tabnew " + config_file_path)
    
    if vim.current.buffer[0] == "":
        vim.current.buffer[0] = "ACCESS_TOKEN: "

def qiitaPyPost():
    data = getArticle()

    params = {\
        "body": data["body"],\
        "coediting": False,\
        "gist": False,\
        "group_url_name": "null",\
        "private": False,\
        "tags": data["tags"],\
        "title": data["title"],\
        "tweet": data["tweet"]\
    }

    client = qiitaPyGetClient()
    response = client.create_item(params)

    if response.status == POST_SUCCESS:
        print("Posting success!")

def qiitaPyEdit():
    print("Under Construction...")

def qiitaPyList():
    print("Under Construction...")

def qiitaPyDelete():
    print("Under Construction...")


def qiitaPyGetClient():
    global client
    return QiitaClient(config_file = config_file_path) if client is None else client
