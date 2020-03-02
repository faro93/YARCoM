#!/usr/bin/python3
# coding=utf-8

from pathlib import *
from urllib.parse import urlparse
import json
import os
import subprocess
import logging
import requests
import sys
import re
from tkinter import messagebox


class LoadConfig ():
    def __init__(self, file):
        self.configurationFile = file
        if Path(self.configurationFile).is_file():
            with open(self.configurationFile) as cf:
                self.configuration = json.load(cf)
                cf.close()
                print("Configuration file "+file+" loaded.")
        else:
            print("File "+file+" does not exists")
            self.configuration = False

    def LoadEquipments(self):
        # Prevent InsecureRequestWarning message from being displayed
        logging.captureWarnings(True)

        root = dict()
        order = list()
        for file in self.configuration['files']:
            # print(f'1.file={file}')
            tree = dict()
            if re.match(r'http', file[1]):
                tree = self.openURL(file[1], file[2])
                # print(f'2.tree={json.dumps(tree, indent=3)}')
            else:
                tree = self.openLocal(file[1])
                # print(f'3.tree={json.dumps(tree, indent=3)}')
            if 'ORDER' in tree:
                order = self.MergeDict(root, tree, order)
            else:
                messagebox.showwarning(
                    "YARCoM warning", "JSON file "+str(file)+" has no ORDER list")
        # print(f'4.tree={json.dumps(tree, indent=3)}')
        return root

    def openURL(self, file, proxy=True):
        tree = dict()
        mystring = str()
        p = urlparse(file)
        mystring += p.netloc

        if proxy == False:
            if not 'NO_PROXY' in os.environ:
                os.environ['NO_PROXY'] = mystring
            else:
                s = os.environ['NO_PROXY']
                l = s.split(';')
                if not myString in l:
                    os.environ['NO_PROXY'] += ';' + myString

        try:
            r = requests.get(file, verify=False)
        except requests.exceptions.ConnectionError as ce:
            messagebox.showwarning(
                "YARCoM warning", "Unable to load file "+str(file)+"\n"+str(ce))
            tree['ORDER'] = dict()
            return tree
        except requests.exceptions.ConnectionRefusedError as cre:
            messagebox.showwarning(
                "YARCoM warning", "Unable to load file "+str(file)+"\n"+str(cre))
            tree['ORDER'] = dict()
            return tree

        if r.reason == 'OK':
            tree = json.loads(r.content)
            return tree

    def openLocal(self, file):
        tree = dict()
        if Path(file).is_file():
            with open(file) as fp:
                tree = json.load(fp)
                fp.close()
        else:
            messagebox.showwarning(
                "YARCoM warning", "Unable to load file "+str(file))
        return tree

    def MergeDict(self, dict1, dict2, order):
        for index in dict2['ORDER']:
            order.append(index)
        dict1.update(dict2)
        dict1['ORDER'] = order
        return order

    def getTools(self):
        if self.configuration != False:
            delList = list()
            tools = self.configuration['tools']
            for tool in self.configuration['tools']:
                if not os.path.exists(tool[1]):
                    # print("Erasing tool \"{}\" : does not exist".format(tools[tool]['name']))
                    messagebox.showwarning("YARCoM warning", "Erasing tool "+str(tool[0]) +
                                           " :\ndoes not exist")
                    delList.append(tool)
            for tool in delList:
                tools.remove(tool)
        return tools

    # def confTools(self, myDict):
    #     pass

    # def confEquipmentsFiles(self, myList):
    #     pass


if __name__ == "__main__":
    conf = LoadConfig('YARCoM.conf')
    root = conf.LoadEquipments()
    toolList = conf.getTools()
    print(f'{json.dumps(root, indent=4)}')
    print(f'{json.dumps(toolList, indent=4)}')
