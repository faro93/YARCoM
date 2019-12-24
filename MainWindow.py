#!/usr/bin/python3
# coding=utf-8

import json
import re
from tkinter import *       # pylint disable=unused-wildcard-import
from tkinter import ttk     # pylint disable=unused-wildcard-import
from LoadConfig import LoadConfig


class MainWindow (Tk):
    def __init__(self, parent, windowTitle):
        Tk.__init__(self, parent)
        self.parent = parent
        self.title(windowTitle)

    def initialize(self, equipmentList):
        self.equipmentList = equipmentList
        self.grid()

        self.tree = ttk.Treeview(self)
        self.tree['columns'] = ("IP")
        self.tree.column('#0', width=140, stretch=FALSE)
        self.tree.heading('#0', text="Equipments")
        self.tree.column('IP', width=120, stretch=FALSE, anchor='center')
        self.tree.heading('IP', text="IPs")
        self.tree.config(height=20, selectmode='browse')

        self.tree.bind('<<TreeviewSelect>>', self.TreeOnSelect)
        self.tree.bind('<Key>', self.TreeOnKeyPress)
        self.tree.bind('<Double-Button-1>', self.TreeOnDoubleClick)
        self.tree.bind('<Button-3>', self.TreeOnRightClick)
        self.InitTree(self.equipmentList, 0)

        self.entryVariable = StringVar()
        self.entry = Entry(self, textvariable=self.entryVariable)
        self.entry.bind("<Return>", self.EntryOnPressReturn)
        self.entryVariable.set('Equipment to search')

        self.button = Button(self, text="Search", padx=0,
                             pady=0, command=self.OnButtonClick)

        self.tree.grid(row=0, column=0, columnspan=2, sticky='NS')
        self.entry.grid(row=1, column=0, sticky='EW')
        self.button.grid(row=1, column=1, sticky='EW')

        self.grid_rowconfigure(0, weight=1)
        self.resizable(FALSE, TRUE)
        self.entry.focus_set()
        self.entry.selection_range(0, END)

    def InitTree(self, equipmentList, pad, myParent=None):
        padding = ""
        for i in range(pad):    # pylint: disable=unused-variable
            padding += "   "
        for key in equipmentList['ORDER']:
            print("{}{}".format(padding, key))
            if pad == 0:
                self.tree.insert('', 'end', key, text=key)
                pad += 1
                self.BrowseDict(equipmentList[key], key, pad)
                pad -= 1
            else:
                self.tree.insert(myParent, 'end', myParent+'.'+key, text=key)
                pad += 1
                self.BrowseDict(equipmentList[key], myParent+'.'+key, pad)
                pad -= 1

    def BrowseDict(self, myDict, myParent, pad):
        padding = ""
        for i in range(pad):    # pylint: disable=unused-variable
            padding += "   "
        if 'ORDER' in myDict:
            pad += 1
            self.InitTree(myDict, pad, myParent)
            pad -= 1
        else:
            for (key, value) in myDict.items():
                if type(value) == dict:
                    if 'IP' in myDict[key]:
                        print("{}{}.{} : {}".format(padding,
                                                    myParent, key, myDict[key]['IP']))
                        self.tree.insert(myParent, 'end', myParent+'.'+key,
                                         text=key, values=myDict[key]['IP'])
                    else:
                        pad += 1
                        self.tree.insert(
                            myParent, 'end', myParent+'.'+key, text=key)
                        self.BrowseDict(value, myParent+'.'+key, pad)
                        pad -= 1

    def TreeOnSelect(self, event):
        for item in self.tree.selection():
            item_text = self.tree.item(item, "text")
            item_value = self.tree.item(item, "value")
            for value in item_value:
                print("{} -> {}".format(item_text, value))
            print("Evènement sélection")
            for index in self.equipmentList['ORDER']:
                if item_text == index:
                    self.tree.selection_remove(item)

    def TreeOnKeyPress(self, event):
        pass

    def TreeOnDoubleClick(self, event):
        pass

    def TreeOnRightClick(self, event):
        pass

    def EntryOnPressReturn(self, event):
        if self.entryVariable.get() != "Equipment to search" and self.entryVariable.get() != "":
            print("1."+self.entryVariable.get()+".")
        else:
            self.entryVariable.set("What's up dude ?!")
            self.entry.focus_set()
        self.entry.focus_set()
        self.entry.selection_range(0, END)

    def OnButtonClick(self):
        if self.entryVariable.get() != "Equipment to search" and self.entryVariable.get() != "":
            print("2."+self.entryVariable.get()+".")
        else:
            self.entryVariable.set("What's up dude ?!")
            self.entry.focus_set()
        self.entry.selection_range(0, END)


if __name__ == "__main__":
    config = LoadConfig('YARCoM.conf')
    equipmentList = config.LoadEquipments()
    windowTitle = "YARCoM v0.1"
    mainWindow = MainWindow(None, windowTitle)
    mainWindow.initialize(equipmentList)
    mainWindow.mainloop()
