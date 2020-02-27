#!/usr/bin/python3
# coding=utf-8

from tkinter import *
from tkinter import ttk


class URLWindow (Tk):
    def __init__(self, parent, windowTitle, appName):
        Toplevel.__init__(self, parent)

        self.parent = parent
        self.title(windowTitle)
        self.appTitle = appName
        self.InitWindow()
        self.columnconfigure(0, weight=1)
        self.resizable(TRUE, FALSE)
        self.minsize(210, 1)
        self.grid()
        self.result = None

    def InitWindow(self):
        fmain = ttk.Frame(self, padding=5)
        fmain.columnconfigure(0, weight=1)

        fURL = ttk.Frame(fmain, padding=5)
        fURL.columnconfigure(0, weight=1)

        fbtn = ttk.Frame(fmain, padding=5)

        self.entryVariable = StringVar()
        self.entryVariable.set('Copy URL here')
        self.entry = Entry(fURL, textvariable=self.entryVariable)
        self.entry.focus_set()
        self.entry.selection_range(0, END)

        self.checkVar = IntVar()
        self.check = Checkbutton(fURL, text="PROXY", variable=self.checkVar)

        self.okBtn = Button(fbtn, text="OK", command=self.OK,
                            width=5, padx=4, pady=4)
        self.cancelBtn = Button(fbtn, text="CANCEL", command=self.destroy,
                                width=5, padx=4, pady=4)

        self.entry.grid(column=0, row=0, columnspan=2, sticky=(N, S, W, E))
        self.check.grid(column=0, row=1, sticky=(N, S, W, E))
        fURL.grid(columnspan=2, column=0, row=0, sticky=(W, E))

        fbtn.grid(columnspan=2, column=0, row=1)
        self.okBtn.grid(column=0, row=1)
        self.cancelBtn.grid(column=1, row=1)

        fmain.grid(sticky=(W, E))

    def OK(self):
        # print(f'checkVar={self.checkVar.get()}')
        # print(f'entry={self.entry.get()}')
        self.result = (self.entry.get(), self.checkVar.get())
        self.destroy()


if __name__ == "__main__":
    windowTitle = "Add URL file ..."
    appName = "YARCoM v0.1"
    urlWindow = URLWindow(None, windowTitle, appName)
    urlWindow.mainloop()
    print(f'urlWindow.result={urlWindow.result}')
