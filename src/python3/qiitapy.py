#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import sys
import os
import vim
from getpass import getpass

from qiita_v2.client import QiitaClient

from qiitaPyError import QiitaPyCommandError
from parseVimBuffer import getArticle

POST_SUCCESS    = 200
GET_SUCCESS     = 200

config_file_path = os.path.expanduser("~/.qiita-py.yaml")
client = None
window_name = "Qiita-articles"

def qiitaPy(command, option):
    if command == "config":
        qiitaPyConfig()
    elif command == "post":
        qiitaPyPost()
    elif command == "edit":
        qiitaPyEdit()
    elif command == "list":
        print(option)
        if len(option) > 0:
            name = option[0]
            page = int(option[1]) if len(option) > 1 else 1
            qiitaPyList(name = name, page = page)
        else:
            sys.stderr.write("List needs user name.\n")
    elif command == "delete":
        qiitaPyDelete()
    else:
        raise QiitaPyCommandError(command)

def qiitaPyConfig():
    # create new tab and open the config file
    vim.command("tabnew " + config_file_path)
    
    # if not written in current buffer, write "ACCESS_TOKEN: "
    if vim.current.buffer[0] == "":
        vim.current.buffer[0] = "ACCESS_TOKEN: "

def qiitaPyPost():
    # get an article from current buffer
    data = getArticle()

    # set parameters
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

    # send the article
    client = qiitaPyGetClient()
    response = client.create_item(params)

    # check status code
    if response.status == POST_SUCCESS:
        print("Posting success!")

def qiitaPyEdit():
    print("Under Construction...")

def qiitaPyList(name = "", page = 1):
    # if page < 1, send exception
    if page < 1:
        raise QiitaPyPageError(page)

    # move to a message window
    buf_id = -1
    for buf in vim.buffers:
        if os.path.basename(buf.name) == window_name:
            buf_id = buf.number
            break

    win_id = -1
    for win in vim.windows:
        if win.buffer.number == buf_id:
            win_id = win.number
            break

    if win_id != -1:
        if win_id != vim.current.window.number:
            vim.command("exe {} 'wincmd w'".format(win_id))
    else:
        vim.command("exe 'silent noautocmd vsplit {}'".format(window_name))
    vim.current.buffer.options["modifiable"] = True

    # get an article list
    print("Getting articles...")

    params = {\
        "page": page,\
        "per_page": 20\
    }

    client = qiitaPyGetClient()
    response = client.list_user_items(name, params)

    if response.status == GET_SUCCESS:
        print("Getting success!")
    else:
        sys.stderr.write("ERROR: status code {}".format(response.status))
        return

    # show the list
    print("Listing articles...")
    # title_list = [item["title"] for item in response.to_json()]
    title_list = ["aaa", "bbb", "ccc"]
    vim.current.buffer[0] = "page: {}".format(page)
    vim.current.buffer[:] = ["{}: {}".format(idx, title) for idx, title in enumerate(title_list)]

    vim.current.buffer.options["modifiable"] = False
    vim.current.buffer.options["modified"] = False

def qiitaPyDelete():
    print("Under Construction...")

def qiitaPyGetClient():
    global client
    if client is None:
        client = QiitaClient(config_file = config_file_path)
    return client
