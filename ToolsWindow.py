#!/usr/bin/python3
# coding=utf-8

from tkinter import *       # pylint disable=unused-wildcard-import
from tkinter import ttk     # pylint disable=unused-wildcard-import
from LoadConfig import LoadConfig

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
        lbl = Label(self.parent, text="Hello")
        lbl.grid(column=0, row=0)
        btn = Button(self.parent, text="Click me", command=self.OnButtonClick)
        btn.grid(column=0, row=1)

    def InitContextMenuWidget(self):
        self.popupMenu = Menu(self, tearoff=0)
        # print(toolsList)
        for tool in range(3):
            self.popupMenu.add_command(label="test 1",
                command=lambda arg=(tool): self.test(arg))
            self.popupMenu.add_command(label="test 2",
                command=lambda arg=(tool): self.test(arg))
            self.popupMenu.add_command(label="test 3",
                command=lambda arg=(tool): self.test(arg))

    def test(self, number):
        print(f'1.test {number}')

    def OnButtonClick(self):
        self.PopUp ()

    def PopUp(self, event):
        try:
            # self.popupMenu.selection = self.tree.identify_row(event.y)
            self.popupMenu.post(event.x_root+30, event.y_root)
        finally:
            self.popupMenu.grab_release()

if __name__ == "__main__":
    windowTitle = "Tools ..."
    appName = "YARCoM v0.1"
    config = LoadConfig('YARCoM.conf')
    toolsWindow = ToolsWindow(None, windowTitle, appName)
    equipmentList = config.LoadEquipments()
    toolsList = config.getTools()
    toolsWindow.mainloop()