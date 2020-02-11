#!/usr/bin/python3
# coding=utf-8

from tkinter import *       # pylint disable=unused-wildcard-import
from tkinter import ttk     # pylint disable=unused-wildcard-import
from LoadConfig import LoadConfig
import json


class ToolsWindow (Tk):
    def __init__(self, parent, windowTitle, appName):
        Tk.__init__(self, parent)
        self.parent = parent
        self.title(windowTitle)
        self.appTitle = appName
        self.InitWindow()

    def InitWindow(self):
        self.grid()
        self.geometry('500x400')

        self.tree = ttk.Treeview(self)
        self.tree['columns'] = ("Name", "Path")
        self.tree.column('#0', width=30, stretch=FALSE)
        self.tree.heading('#0', text="#")
        self.tree.column('Name', width=80, stretch=FALSE, anchor='w')
        self.tree.heading('Name', text="Name")
        self.tree.column('Path', width=300, stretch=FALSE, anchor='w')
        self.tree.heading('Path', text="Path")
        self.tree.config(selectmode='browse')
        self.tree.grid(row=0, column=0, rowspan=6, sticky='EW')

        top = Button(self, text="Click me",
                     command=lambda arg=(1): self.test(arg))
        top.grid(row=0, column=1)
        up = Button(self, text="Click me",
                    command=lambda arg=(2): self.test(arg))
        up.grid(row=1, column=1)
        adding = Button(self, text="Click me",
                        command=lambda arg=(3): self.test(arg))
        adding.grid(row=2, column=1)
        deleting = Button(self, text="Click me",
                          command=lambda arg=(4): self.test(arg))
        deleting.grid(row=3, column=1)
        down = Button(self, text="Click me",
                      command=lambda arg=(5): self.test(arg))
        down.grid(row=4, column=1)
        bottom = Button(self, text="Click me",
                        command=lambda arg=(6): self.test(arg))
        bottom.grid(row=5, column=1)

    def test(self, number):
        print(f'1.Button {number}')


if __name__ == "__main__":
    windowTitle = "Tools ..."
    appName = "YARCoM v0.1"
    config = LoadConfig('YARCoM.conf')
    toolsWindow = ToolsWindow(None, windowTitle, appName)
    equipmentList = config.LoadEquipments()
    toolsList = config.getTools()
    toolsWindow.mainloop()
    print(f'{json.dumps(equipmentList, indent=4)}')
    print(f'{json.dumps(toolsList, indent=4)}')
