#!/usr/bin/python3
# coding=utf-8


from MainWindow import MainWindow
from LoadConfig import LoadConfig
from tkinter import Tk


class YARCoM():
    def __init__(self):
        self.confFile = 'YARCoM.conf'
        self.appName = "YARCoM"
        self.appVersion = "v0.7"
        self.appAuthor = "faro"
        self.windowTitle = self.getTitle()
        self.mainWindow = MainWindow(None, self.windowTitle)
        self.config = LoadConfig(self.confFile)
        self.equipmentsList = self.config.LoadEquipments()
        self.toolsList = self.config.getTools()
        self.mainWindow.InitWidgets(self.equipmentsList, self.toolsList)
        self.mainWindow.mainloop()

    def getTitle(self):
        return (self.appName+' '+self.appVersion)


if __name__ == "__main__":
    YARCoM()
