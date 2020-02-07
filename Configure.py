#!/usr/bin/python3
# coding=utf-8

from tkinter import *       # pylint disable=unused-wildcard-import
from tkinter import ttk     # pylint disable=unused-wildcard-import
from LoadConfig import LoadConfig

class MainWindow (Tk):
    def __init__(self, parent, windowTitle):
        Tk.__init__(self, parent)
        self.parent = parent
        self.title(windowTitle)
        self.windowTitle = windowTitle

if __name__ == "__main__":
    config = LoadConfig('YARCoM.conf')
    equipmentList = config.LoadEquipments()
    windowTitle = "YARCoM v0.1"
    toolsList = config.getTools()
    mainWindow = MainWindow(None, windowTitle)
    mainWindow.InitWidgets(equipmentList, toolsList)
    mainWindow.mainloop()