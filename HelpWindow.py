#!/usr/bin/python3
# coding=utf-8

from tkinter import *       # pylint disable=unused-wildcard-import
from tkinter import ttk     # pylint disable=unused-wildcard-import

class HelpWindow (Tk):
    def __init__(self, parent, windowTitle):
        Tk.__init__(self, parent)
        self.parent = parent
        self.title(windowTitle)
        self.InitWindow()
    
    def InitWindow(self):
        self.grid()
        text = Text(self)
        text.insert(INSERT, "Bla")
        text.pack()
        pass
        # self.tree.grid(row=0, column=0, columnspan=2, sticky='NS')
        # self.entry.grid(row=1, column=0, sticky='EW')
        # self.button.grid(row=1, column=1, sticky='EW')
        # self.grid_rowconfigure(0, weight=1)
        self.resizable(FALSE, FALSE)


if __name__ == "__main__":
    windowTitle = "About..."
    helpWindow = HelpWindow(None, windowTitle)
    helpWindow.mainloop()