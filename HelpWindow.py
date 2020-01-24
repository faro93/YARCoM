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
        self.geometry('500x400')

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

        appName = Label(self, text=self.appTitle)
        appName['font'] = activeBoldFont

        description = (
            'YARCoM is an application that loads one or many description files of your network (hostnames and IPs) '
            'as an ordered tree. Then, you can select a machine and run which command you defined from a context '
            'menu or the default one by double clicking it.'
            '\nThere are 2 files type :'
            '\n- YARCoM.conf : containing the configuration'
            '\n- *.json : files describing your networks.'
            '\n\nYARCoM.conf is a JSON file containing :'
            '\n- a list of networks files'
            '\n- a dictionnary of tools'
            '\n{\n  \'files\':[\'file1.json\', \'file2.json\'],'
            '\n  \'tools\': {\n    \'1\': {\n      \'name\':<name1>,\n      \'bin\': <first executable\'s binary path>,\n      \'args\': <arguments>'
            '\n    }'
            '\n    \'2\': {\n      \'name\':<name2>,\n      \'bin\': <second executable\'s binary path>,\n      \'args\': <arguments>'
            '\n    }'
            '\n  }'
            '\n}'
            '\n\nJSONs contains :'
            '\n- dictionnaries'
            '\n- a list'
            '\n{\n  \'NETWORK1\': {\n    \'MACHINE1\': {\'IP\':<IP>}\n    \'MACHINE2\': {\'IP\':<IP>}\n  }\n'
            '\n  \'NETWORK2\': {\n    \'MACHINE1\': {\'IP\':<IP>}\n    \'MACHINE2\': {\'IP\':<IP>}\n  }'
            '\n  \'ORDER\':[\'NETWORK2\', \'NETWORK1\']'
            '\n}'
            '\nEach dictionnary can also contain nested dictionnaries containing sub-networks of machines. '
            'Each sub-network must have its own ORDER list. Lists at the same level will be merged.'
            )
        text = Text(self)
        text.tag_configure('bold', font=activeBoldFont)
        text.tag_configure('normal', font=activeFont)
        text.insert(END, description, 'normal')
        text.configure(height=19, spacing3=2, relief=FLAT, state='disabled')

        helpText = Text(self)
        helpText.tag_configure('bold', font=activeBoldFont)
        helpText.tag_configure('normal', font=activeFont)

        helpContent = "Yet Another Remote Connexion Manager"
        for word in helpContent.split():
            for index in range(0, len(word)):
                if index == 0:
                    helpText.insert(END, word[index], 'bold')
                else:
                    if word == 'Connexion' and index == 1:
                        helpText.insert(END, word[index], 'bold')
                    else:
                        helpText.insert(END, word[index], 'normal')
            helpText.insert(END, ' ', 'normal')
        helpText.configure(height=1, spacing3=2, relief=FLAT, state='disabled')
        # print(aboutText.config())

        appName.grid(row=0, sticky='WE')
        # fullName.grid(row=1)
        helpText.grid(row=1, sticky='WE')
        text.grid(row=2,sticky='WE')
        self.grid_columnconfigure(0, weight=1)

        # self.resizable(FALSE, FALSE)


if __name__ == "__main__":
    windowTitle = "Help..."
    appName = "YARCoM v0.1"
    helpWindow = HelpWindow(None, windowTitle, appName)
    helpWindow.mainloop()