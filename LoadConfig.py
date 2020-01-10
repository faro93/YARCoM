#!/usr/bin/python3
# coding=utf-8

from pathlib import *
import json
import os
import subprocess

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
        if self.configuration != False:
            root = dict()
            order = list()
            for self.file in self.configuration['files']:
                if Path(self.file).is_file():
                    with open(self.file) as fp:
                        tree = json.load(fp)
                        order = self.MergeDict(root, tree, order)
                        fp.close()
        else:
            print("No configuration loaded.")
        return root

    def MergeDict(self, dict1, dict2, order):
        for index in dict2['ORDER']:
            order.append(index)
        dict1.update(dict2)
        dict1['ORDER'] = order
        return order

    def getTools(self):
        if self.configuration != False:
            tools = self.configuration['tools']
            for tool in sorted(tools):
                if not os.path.exists(tools[tool]['bin']):
                    print("Erasing tool \"{}\" : does not exist".format(tools[tool]['name']))
                    del (tools[tool])
        return tools

if __name__ == "__main__":
    conf = LoadConfig('YARCoM.conf')
    root = conf.LoadEquipments()
    toolList = conf.getTools()
    # print(root)
    print(toolList)
