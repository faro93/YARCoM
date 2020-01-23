#!/usr/bin/python3
# coding=utf-8

from tkinter import *       # pylint disable=unused-wildcard-import
from tkinter import ttk     # pylint disable=unused-wildcard-import
import tkinter.font as tkF

class HelpWindow (Tk):
    def __init__(self, parent, windowTitle, appName):
        Tk.__init__(self, parent)
        self.parent = parent
        self.title(windowTitle)
        self.appTitle = appName
        self.InitWindow()
    
    def InitWindow(self):
        self.grid()
        appName = Label(self, text=self.appTitle)
        self.geometry('300x200')
        # lab1 = Label(self, text="label 1,\navec un saut de ligne")
        # lab2 = Label(self, text="label 2")
        # lab3 = Label(self, text="label 3, sans saut de ligne")
        # lab4 = Label(self, text="label 4")
        # lab5 = Label(self, text="Le dernier label : le label 5\nAvec un saut de ligne")
        # lab1.grid(row=0, column=0, sticky='W')
        # lab2.grid(row=0, column=1, sticky='E')
        # lab3.grid(row=1, column=0, sticky='E')
        # lab4.grid(row=1, column=1, sticky='W')
        # lab5.grid(row=2, columnspan=2)
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

        appName['font'] = activeBoldFont
        appName['background'] = 'yellow'
        # print(appName.config())
        fullName = Label(self, text="Yet Another Remote\nCOnnexion Manager")
        fullName['background'] = 'white'
        text = Label(self, text="Bla bla bla bla bla bla bla bla bla\nbla bla bla bla bla bla bla.", justify='left')
        text['background'] = 'coral'
        aboutText = Text(self)
        aboutText.tag_configure('bold', font=activeBoldFont)
        aboutText.tag_configure('normal', font=activeFont)

        aboutContent = "Yet Another Remote Connexion Manager"
        for word in aboutContent.split():
            for index in range(0, len(word)):
                if index == 0:
                    aboutText.insert(END, word[index], 'bold')
                else:
                    if word == 'Connexion' and index == 1:
                        aboutText.insert(END, word[index], 'bold')
                    else:
                        aboutText.insert(END, word[index], 'normal')
            aboutText.insert(END, ' ', 'normal')
        aboutText.configure(background='pink1', height=1, spacing3=2, relief=FLAT, state='disabled')
        print(aboutText.config())

        appName.grid(row=0, sticky='WE')
        # fullName.grid(row=1)
        aboutText.grid(row=1)
        text.grid(row=2)
        self.grid_columnconfigure(0, weight=1)

        self.resizable(FALSE, FALSE)


if __name__ == "__main__":
    windowTitle = "About..."
    appName = "YARCoM v0.1"
    helpWindow = HelpWindow(None, windowTitle, appName)
    helpWindow.mainloop()