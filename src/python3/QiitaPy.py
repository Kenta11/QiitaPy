#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import sys
import os
import vim
import yaml

from qiita_v2.client import QiitaClient

from qiitaPyError import QiitaPyCommandError
from parseVimBuffer import getArticle

GET_SUCCESS     = 200
UPDATE_SUCCESS  = 200
POST_SUCCESS    = 201

config_file_path = os.path.expanduser("~/.qiita-py.yaml")
client = None
window_name = "Qiita-articles"
USER_NAME = None
"""
key: pseudo-id
item: {title, body, id, tags}
"""
article_dict = {}

def qiitaPy(command, option = []):
    if command == "config":
        qiitaPyConfig()
    elif command == "post":
        qiitaPyPost(option[0] if len(option) else "")
    elif command == "list":
        name = None
        global USER_NAME
        if option != []:
            name = option[0]
        elif not USER_NAME:
            name = USER_NAME
        else:
            f = open(config_file_path, "r")
            config = yaml.load(f)

            if "USER_NAME" in config:
                name = config["USER_NAME"]
            else:
                sys.stderr.write("name is needed.\n")
                return

            f.close()

        page = int(option[1]) if len(option) > 1 else 1

        qiitaPyList(name = name, page = page)
    elif command == "edit":
        page = -1
        try:
            page = int(option[0])
        except IndexError:
            sys.stderr.write("pseudo_id is needed.\n")
            return
        except ValueError:
            sys.stderr.write("Argument must be an integer")
            return

        qiitaPyEdit(page)
    elif command == "template":
        qiitaPyTemplate()
    else:
        raise QiitaPyCommandError(command)

def qiitaPyConfig():
    # create new tab and open the config file
    vim.command("tabnew " + config_file_path)
    
    # if not written in current buffer, write "ACCESS_TOKEN: "
    if vim.current.buffer[0] == "":
        vim.current.buffer[:] = ["ACCESS_TOKEN: ", "USER_NAME: "]

def qiitaPyPost(mode = ""):
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

    client = qiitaPyGetClient()

    if mode == "new":
        # send the article
        response = client.create_item(params)
        # check status code
        if response.status == POST_SUCCESS:
            print("Posting success!")
    else:
        pseudo_id = -1
        try:
            vim.command("let qiitaPy#pseudo_id = input('pseudo article id: ')")
            pseudo_id = int(vim.eval("qiitaPy#pseudo_id"))
        except ValueError:
            sys.stderr.write("ERROR: Enter pseudo id in the article list")
            return
            
        article_id = "-1"
        global article_dict
        for key in article_dict.keys():
            if key == pseudo_id :
                ret = vim.command("old title: {} ?<y/n>".format(article_dict[key]["title"]))
                if ret == "y":
                    article_id = article_dict[key]["article_id"]
                    break
                elif ret == "n":
                    sys.stderr.write("Posting was failed.")
                    return
                else:
                    sys.stderr.write("Enter 'y' or 'n'.")
                    return
        else:
            sys.stderr.write("pseudo-id {} was not found.".format(pseudo_id))
            return

        # update the article
        response = client.update_item(article_id, params)

        # check status code
        if response.status == UPDATE_SUCCESS:
            print("Posting success!")
            article_dict[pseudo_id] = {"title": params["title"], "body": params["body"], "article_id": article_id, "tags": params["tags"]}

def qiitaPyEdit(page):
    # check pseudo_id in article_dict
    global article_dict
    if page not in article_dict.keys():
        sys.stderr.write("pseudo_id {} was not found in the list.".format(page))
        return

    # move to window with new buffer
    if not vim.current.buffer.options["modified"]:
        vim.command("enew")
    elif vim.current.buffer.name != "" or\
       len(vim.current.buffer) != 1 or\
       vim.current.buffer.options["modified"]:
           vim.command("tabnew")

    # display the article
    ## params
    vim.current.buffer[0] = "---"

    ### title
    vim.current.buffer.append("title: {}".format(article_dict[page]["title"]))

    ### tags
    vim.current.buffer.append("tags:")
    for tag in article_dict[page]["tags"]:
        vim.current.buffer.append(\
            "    - {}: {}".format(tag["name"], tag["versions"] if tag["versions"] != [] else "")\
        )

    vim.current.buffer.append("---")

    ## body
    for line in article_dict[page]["body"].split("\n"):
        vim.current.buffer.append(line)

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

    global article_dict
    article_dict = {}
    for idx, item in enumerate(response.to_json()):
        article_dict[(page - 1) * 20 + idx + 1] = {\
            "title":      item["title"],\
            "body":       item["body"],\
            "article_id": item["id"],\
            "tags":       item["tags"]\
        }

    # show the list
    print("Listing articles...")
    title_list = [item["title"] for item in response.to_json()]
    window_width = 0
    for win in vim.windows:
        window_width += win.width
    vim.current.window.width = window_width / 4
    vim.current.buffer[0] = "page: {}".format(page)
    vim.current.buffer.append("pseudo_id: title")
    vim.current.buffer.append("")
    vim.current.buffer[2:] = ["{}: {}".format((page - 1) * 20 + idx + 1, title) for idx, title in enumerate(title_list)]

    vim.current.buffer.options["modifiable"] = False
    vim.current.buffer.options["modified"] = False
    vim.current.buffer.options["buftype"] = b"nofile"

    vim.command("let b:QiitaPy= ''")

    # move to window which one before
    vim.command("wincmd l")

def qiitaPyTemplate():
    # move to window with new buffer
    if not vim.current.buffer.options["modified"]:
        vim.command("enew")
    elif vim.current.buffer.name != "" or\
       len(vim.current.buffer) != 1 or\
       vim.current.buffer.options["modified"]:
           vim.command("tabnew")

    # generate template
    article_template = []
    article_template.append("---")

    ## title
    article_template.append("title: ")

    ## tags
    article_template.append("tags:")
    article_template.append("    - ")

    article_template.append("---")

    ## body
    article_template.append("")

    vim.current.buffer[:] = article_template

def qiitaPyGetClient():
    global client
    if client is None:
        client = QiitaClient(config_file = config_file_path)
    return client
