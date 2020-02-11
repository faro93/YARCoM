#!/usr/bin/python3
# coding=utf-8

from tkinter import *       # pylint disable=unused-wildcard-import
from tkinter import ttk     # pylint disable=unused-wildcard-import
from LoadConfig import LoadConfig

class FilesWindow (Tk):
    def __init__(self, parent, windowTitle, appName):
        Tk.__init__(self, parent)
        self.parent = parent
        self.title(windowTitle)
        self.appTitle = appName
        self.InitWindow()

    def InitWindow(self):
        self.grid()
        self.geometry('500x400')

if __name__ == "__main__":
    windowTitle = "Files ..."
    appName = "YARCoM v0.1"
    config = LoadConfig('YARCoM.conf')
    filesWindow = FilesWindow(None, windowTitle, appName)
    equipmentList = config.LoadEquipments()
    toolsList = config.getTools()
    filesWindow.mainloop()