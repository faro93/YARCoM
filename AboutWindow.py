#!/usr/bin/python3
# coding=utf-8

from tkinter import *       # pylint disable=unused-wildcard-import
from tkinter import ttk     # pylint disable=unused-wildcard-import
import tkinter.font as tkF

class AboutWindow (Tk):
    def __init__(self, parent, windowTitle, appName):
        Tk.__init__(self, parent)
        self.parent = parent
        self.title(windowTitle)
        self.appTitle = appName
        self.InitWindow()
    
    def InitWindow(self):
        self.grid()
        self.geometry('220x30')

        activeFont = tkF.Font()
        activeFamily = activeFont.actual('family')
        activeWeight = activeFont.actual('weight')
        activeSize = activeFont.actual('size')
        activeBoldFont = tkF.Font()
        activeBoldFont.configure(family=activeFamily, size=activeSize, weight='bold')
        activeBoldFamily = activeBoldFont.actual('family')
        activeBoldSize = activeBoldFont.actual('size')
        activeBoldWeight = activeBoldFont.actual('weight')
        if activeWeight == 'normal':
            activeBoldWeight = 'bold'
        else:
            activeFont.configure(weight='normal')
            activeWeight = activeFont.actual('weight')
        # print(f'1.{activeFamily}, {activeSize}, {activeWeight}')
        # print(f'2.{activeBoldFamily}, {activeBoldSize}, {activeBoldWeight}')

        appName = Label(self, text=self.appTitle, justify='left')
        appName['font'] = activeBoldFont

        aboutContent = 'from faro'
        aboutText = Label(self, text=aboutContent, justify='right')

        appName.grid(row=0, sticky='W')
        aboutText.grid(row=0, sticky='E')
        self.grid_columnconfigure(0, weight=1)
        self.resizable(FALSE, FALSE)


if __name__ == "__main__":
    windowTitle = "About..."
    appName = "YARCoM v0.1"
    aboutWindow = AboutWindow(None, windowTitle, appName)
    aboutWindow.mainloop()