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
        self.InitWindow(self.parent)
        self.grid()
        self.minsize(600,400)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def InitWindow(self, parent):
        self.configTabs = ttk.Notebook(parent, padding=5)

        self.toolsFrame = ttk.Frame(self.configTabs, padding=5)
        self.configTabs.add(self.toolsFrame, text="Tools")
        self.toolsFrame.columnconfigure(0, weight=1)
        self.toolsFrame.rowconfigure(0, weight=1)
        self.InitTools(self.toolsFrame)

        self.filesFrame = ttk.Frame(self.configTabs, padding=5)
        self.configTabs.add(self.filesFrame, text="Files")
        self.filesFrame.columnconfigure(0, weight=1)
        self.filesFrame.rowconfigure(0, weight=1)
        self.InitFiles(self.filesFrame)

        self.configTabs.grid(column=0, row=0, sticky=(N, S, E, W))
        # see tuto https://tkdocs.com/tutorial/grid.html

    def InitTools(self, parent):
        self.tree = ttk.Treeview(parent)
        self.tree['columns'] = ("Name", "Path")
        self.tree.column('#0', width=30, stretch=FALSE)
        self.tree.heading('#0', text="#")
        self.tree.column('Name', width=50, stretch=TRUE, anchor='w')
        self.tree.heading('Name', text="Name")
        self.tree.column('Path', width=300, stretch=TRUE, anchor='w')
        self.tree.heading('Path', text="Path")
        self.tree.config(selectmode='browse')
        self.tree.grid(column=0, row=0, sticky=(N, S, E, W))

        self.buttonsFrame = ttk.Frame(parent, width=100, height=100, padding=5)
        self.buttonsFrame.grid(column=1, row=0)

        top = Button(self.buttonsFrame, text="Top",
                     command=lambda arg=("tool top"): self.test(arg))
        top.grid(row=0, sticky=(E, W))
        up = Button(self.buttonsFrame, text="Up",
                    command=lambda arg=("tool up"): self.test(arg))
        up.grid(row=1, sticky=(E, W))
        adding = Button(self.buttonsFrame, text="Add",
                        command=lambda arg=("tool add"): self.test(arg))
        adding.grid(row=2, sticky=(E, W))
        deleting = Button(self.buttonsFrame, text="Del",
                          command=lambda arg=("tool del"): self.test(arg))
        deleting.grid(row=3, sticky=(E, W))
        down = Button(self.buttonsFrame, text="Down",
                      command=lambda arg=("tool down"): self.test(arg))
        down.grid(row=4, sticky=(E, W))
        bottom = Button(self.buttonsFrame, text="Bottom",
                        command=lambda arg=("tool bottom"): self.test(arg))
        bottom.grid(row=5, sticky=(E, W))

    def InitFiles(self, parent):
        self.tree = ttk.Treeview(parent)
        self.tree['columns'] = ("File", "Args")
        self.tree.column('#0', width=30, stretch=FALSE)
        self.tree.heading('#0', text="#")
        self.tree.column('File', width=50, stretch=TRUE, anchor='w')
        self.tree.heading('File', text="File path")
        self.tree.column('Args', width=300, stretch=TRUE, anchor='w')
        self.tree.heading('Args', text="Args")
        self.tree.config(selectmode='browse')
        self.tree.grid(column=0, row=0, sticky=(N, S, E, W))

        self.buttonsFrame = ttk.Frame(parent, width=100, height=100, padding=5)
        self.buttonsFrame.grid(column=1, row=0)

        top = Button(self.buttonsFrame, text="Top",
                     command=lambda arg=("file top"): self.test(arg))
        top.grid(row=0, sticky=(E, W))
        up = Button(self.buttonsFrame, text="Up",
                    command=lambda arg=("file up"): self.test(arg))
        up.grid(row=1, sticky=(E, W))
        addurl = Button(self.buttonsFrame, text="Add URL",
                        command=lambda arg=("file add URL"): self.test(arg))
        addurl.grid(row=2, sticky=(E, W))
        addfile = Button(self.buttonsFrame, text="Add Local",
                          command=lambda arg=("file add local"): self.test(arg))
        addfile.grid(row=3, sticky=(E, W))
        deleting = Button(self.buttonsFrame, text="Del",
                          command=lambda arg=("file del"): self.test(arg))
        deleting.grid(row=4, sticky=(E, W))

        down = Button(self.buttonsFrame, text="Down",
                      command=lambda arg=("file down"): self.test(arg))
        down.grid(row=5, sticky=(E, W))
        bottom = Button(self.buttonsFrame, text="Bottom",
                        command=lambda arg=("file bottom"): self.test(arg))
        bottom.grid(row=6, sticky=(E, W))

    def test(self, arg):
        print(f'You clicked button "{arg}"')


if __name__ == "__main__":
    windowTitle = "Tools ..."
    appName = "YARCoM v0.1"
    config = LoadConfig('YARCoM.conf')
    toolsWindow = ToolsWindow(None, windowTitle, appName)
    equipmentList = config.LoadEquipments()
    toolsList = config.getTools()
    toolsWindow.mainloop()
    # print(f'{json.dumps(equipmentList, indent=4)}')
    # print(f'{json.dumps(toolsList, indent=4)}')
