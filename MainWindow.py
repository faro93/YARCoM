#!/usr/bin/python3
# coding=utf-8

from tkinter import *       # pylint disable=unused-wildcard-import
from tkinter import ttk     # pylint disable=unused-wildcard-import
from LoadConfig import LoadConfig
import subprocess
import shlex


class MainWindow (Tk):
    def __init__(self, parent, windowTitle):
        Tk.__init__(self, parent)
        self.parent = parent
        self.title(windowTitle)

    def InitWidgets(self, equipmentList, toolsList):
        self.equipmentList = equipmentList
        self.grid()
        self.InitTreeWidget()
        self.InitEntryWidget()
        self.InitButtonWidget()
        self.InitMenuWidget()
        self.InitContextMenuWidget(toolsList)

        self.tree.grid(row=0, column=0, columnspan=2, sticky='NS')
        self.entry.grid(row=1, column=0, sticky='EW')
        self.button.grid(row=1, column=1, sticky='EW')
        self.grid_rowconfigure(0, weight=1)
        self.resizable(FALSE, TRUE)

        self.InitTree(self.equipmentList, 0)

    def InitTreeWidget(self):
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

    def InitEntryWidget(self):
        self.entryVariable = StringVar()
        self.entry = Entry(self, textvariable=self.entryVariable)
        self.entry.bind("<Return>", self.EntryOnPressReturn)
        self.entryVariable.set('Equipment to search')
        self.entry.focus_set()
        self.entry.selection_range(0, END)

    def InitButtonWidget(self):
        self.button = Button(self, text="Search", padx=0,
                             pady=0, command=self.OnButtonClick)

    def InitMenuWidget(self):
        self.menuBar = Menu(self)
        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="Configure")
        self.fileMenu.add_separator()
        self.config(menu=self.menuBar)
        self.fileMenu.add_command(label="Exit", command=self.quit)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)

        self.helpMenu = Menu(self.menuBar, tearoff=0)
        self.helpMenu.add_command(label="About...")
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)

    def InitContextMenuWidget(self, toolsList):
        self.popupMenu = Menu(self, tearoff=0)
        # print(toolsList)
        for tool in sorted(toolsList):
            self.popupMenu.add_command(label=str(tool) + '.' + toolsList[tool]['name'],
                                       command=lambda arg=(toolsList[tool]): self.RunTool(arg))

    def RunTool(self, toolList):
        item = self.popupMenu.selection
        if self.tree.exists(item):
            # print(f"{item}")
            # self.tree.selection_set(item)
            print("item: {}, tool= {}".format(self.tree.item(item), toolList))
            if len(self.tree.item(item)['values']) != 0:
                ip = self.tree.item(item)['values'][0]
                myArgs = ' '.join([toolList['bin'], toolList['args'], ip])
                subprocess.Popen(myArgs, shell=True)
            else:
                print("Not only one IP in list !")

    def PopUp(self, event):
        try:
            self.popupMenu.selection = self.tree.identify_row(event.y)
            self.popupMenu.post(event.x_root+30, event.y_root)
        finally:
            self.popupMenu.grab_release()

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
            if item_value != "":
                for value in item_value:
                    print("{} -> {}".format(item_text, value))
            else:
                self.tree.selection_remove(item)

    def TreeOnKeyPress(self, event):
        pass

    def TreeOnDoubleClick(self, event):
        # self.popupMenu.add_command(label=toolsList[tool]['name'])
        #             # command=subprocess.run([toolsList[tool]['bin'],"10.5.3.244",toolsList[tool]['args']]))
        pass

    def TreeOnRightClick(self, event):
        self.bind("<Button-3>", self.PopUp)

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
    toolsList = config.getTools()
    mainWindow = MainWindow(None, windowTitle)
    mainWindow.InitWidgets(equipmentList, toolsList)
    mainWindow.mainloop()
