#!/usr/bin/python3
# coding=utf-8

from tkinter import *       # pylint disable=unused-wildcard-import
from tkinter import ttk     # pylint disable=unused-wildcard-import
from tkinter import PhotoImage     # pylint disable=unused-wildcard-import
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
        self.minsize(600, 400)
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

        self.pToolsTop = PhotoImage(file="icon_top.png")
        self.pToolsUp = PhotoImage(file="icon_up.png")
        self.pToolsAdd = PhotoImage(file="icon_toolbox.png")
        self.pToolsDel = PhotoImage(file="icon_trash.png")
        self.pToolsDown = PhotoImage(file="icon_down.png")
        self.pToolsBottom = PhotoImage(file="icon_bottom.png")

        self.top = Button(self.buttonsFrame, text="Top", image=self.pToolsTop, command=lambda arg=(
            "tool top"): self.test(arg)).grid(row=0, sticky=(E, W))
        self.up = Button(self.buttonsFrame, text="Up", image=self.pToolsUp, command=lambda arg=(
            "tool up"): self.test(arg)).grid(row=1, sticky=(E, W))
        self.adding = Button(self.buttonsFrame, text="Add", image=self.pToolsAdd, command=lambda arg=(
            "tool add"): self.test(arg), width=4).grid(row=2, sticky=(E, W))
        self.deleting = Button(self.buttonsFrame, text="Del", image=self.pToolsDel, command=lambda arg=(
            "tool del"): self.test(arg), width=4).grid(row=3, sticky=(E, W))
        self.down = Button(self.buttonsFrame, text="Down", image=self.pToolsDown, command=lambda arg=(
            "tool down"): self.test(arg), width=4).grid(row=4, sticky=(E, W))
        self.bottom = Button(self.buttonsFrame, text="Bottom", image=self.pToolsBottom, command=lambda arg=(
            "tool bottom"): self.test(arg), width=4).grid(row=5, sticky=(E, W))

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

        self.pFilesTop = PhotoImage(file="icon_top.png")
        self.pFilesUp = PhotoImage(file="icon_up.png")
        self.pFilesAddL = PhotoImage(file="icon_addlink.png")
        self.pFilesAddF = PhotoImage(file="icon_addfile.png")
        self.pFilesDel = PhotoImage(file="icon_trash.png")
        self.pFilesDown = PhotoImage(file="icon_down.png")
        self.pFilesBottom = PhotoImage(file="icon_bottom.png")

        self.top = Button(self.buttonsFrame, text="Top", image=self.pFilesTop, command=lambda arg=(
            "file top"): self.test(arg)).grid(row=0, sticky=(E, W))
        up = Button(self.buttonsFrame, text="Up", image=self.pFilesUp, command=lambda arg=(
            "file up"): self.test(arg)).grid(row=1, sticky=(E, W))
        addurl = Button(self.buttonsFrame, text="Add URL", image=self.pFilesAddL, command=lambda arg=(
            "file add URL"): self.test(arg)).grid(row=2, sticky=(E, W))
        addfile = Button(self.buttonsFrame, text="Add Local", image=self.pFilesAddF, command=lambda arg=(
            "file add local"): self.test(arg)).grid(row=3, sticky=(E, W))
        deleting = Button(self.buttonsFrame, text="Del", image=self.pFilesDel, command=lambda arg=(
            "file del"): self.test(arg)).grid(row=4, sticky=(E, W))
        down = Button(self.buttonsFrame, text="Down", image=self.pFilesDown, command=lambda arg=(
            "file down"): self.test(arg)).grid(row=5, sticky=(E, W))
        bottom = Button(self.buttonsFrame, text="Bottom", image=self.pFilesBottom, command=lambda arg=(
            "file bottom"): self.test(arg)).grid(row=6, sticky=(E, W))

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
