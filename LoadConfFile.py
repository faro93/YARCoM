#!/usr/bin/python3
# coding=utf-8

from pathlib import *
import json


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

    def equipments(self):
        if self.configuration != False:
            root = dict()
            for self.file in self.configuration['files']:
                if Path(self.file).is_file():
                    with open(self.file) as fp:
                        tree = json.load(fp)
                        root.update(tree)
                        fp.close()
        else:
            print("No configuration loaded.")
        return root

    def tools(self):
        pass
    # with open('VOIP.json') as fp:
    #     self.root = json.load(fp)
    #     fp.close()


if __name__ == "__main__":
    app = LoadConfig('YARCoM.conf')
    root = app.equipments()
    print(root)
