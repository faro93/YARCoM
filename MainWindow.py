#!/usr/bin/python3
# coding=utf-8

from tkinter import *
from tkinter import ttk
from LoadConfig import LoadConfig
from HelpWindow import HelpWindow
from AboutWindow import AboutWindow
# from FilesWindow import FilesWindow
from PrefsWindow import PrefsWindow
import subprocess
import json
# import shlex


class MainWindow (Tk):
    def __init__(self, parent, windowTitle):
        Tk.__init__(self, parent)
        self.parent = parent
        self.title(windowTitle)
        self.windowTitle = windowTitle

    def InitWidgets(self, equipmentList, toolsList):
        self.toolList = toolsList
        self.equipmentList = equipmentList
        self.grid()
        self.InitTreeWidget()
        self.InitEntryWidget()
        self.InitButtonWidget()
        self.InitMenuWidget()
        self.InitContextMenuWidget(self.toolList)

        self.tree.grid(row=0, column=0, columnspan=2, sticky='NS')
        self.entry.grid(row=1, column=0, sticky='EW')
        self.button.grid(row=1, column=1, sticky='EW')
        self.grid_rowconfigure(0, weight=1)
        self.resizable(FALSE, TRUE)
        self.minsize(1, 200)

        if self.equipmentList != {}:
            # print(f'equipmentList={json.dumps(self.equipmentList, indent=4)}')
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
        self.tree.bind('<Return>', self.TreeOnKeyPress)
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
        self.configMenu = Menu(self.menuBar, tearoff=0)
        self.configMenu.add_command(label="Preferences", command=self.Prefs)
        self.configMenu.add_separator()
        self.config(menu=self.menuBar)
        self.configMenu.add_command(label="Exit", command=self.quit)
        self.menuBar.add_cascade(label="Configure", menu=self.configMenu)

        self.helpMenu = Menu(self.menuBar, tearoff=0)
        self.helpMenu.add_command(label="Help...", command=self.Help)
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label="About...", command=self.About)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)

    def Prefs(self):
        prefsWindowTitle = "Preferences ..."
        prefsWindow = PrefsWindow(
            None, prefsWindowTitle, self.windowTitle, "YARCoM.conf")
        self.wait_window(prefsWindow)
        config = LoadConfig('YARCoM.conf')
        self.equipmentList = config.LoadEquipments()
        eqplist = config.LoadEquipments()
        for item in self.tree.get_children():
            self.tree.delete(item)
        if eqplist != {}:
            self.InitTree(eqplist, 0)
        self.toolList = config.getTools()
        self.InitContextMenuWidget(self.toolList)

    def Help(self):
        helpWindowTitle = "Help..."
        print("Help menu " + helpWindowTitle+' '+self.windowTitle)
        helpWindow = HelpWindow(None, helpWindowTitle, self.windowTitle)

    def About(self):
        aboutWindowTitle = "About..."
        aboutWindow = AboutWindow(None, aboutWindowTitle, self.windowTitle)

    def InitContextMenuWidget(self, toolList):
        self.popupMenu = Menu(self, tearoff=0)
        # print(toolsList)
        for tool in toolList:
            self.popupMenu.add_command(label=tool[0],
                                       command=lambda arg=(tool): self.RunToolFromContextMenu(arg))

    def RunToolFromContextMenu(self, tool):
        # print(f'tool={tool}')
        item = self.popupMenu.selection
        if self.tree.exists(item):
            # print(f"{item}")
            self.tree.selection_set(item)
            # print("item: {}, tool= {}".format(self.tree.item(item), tool))
            if len(self.tree.item(item)['values']) != 0:
                ip = self.tree.item(item)['values'][0]
                if (tool[2] == ''):
                    subprocess.Popen([tool[1], ip], shell=True)
                else:
                    subprocess.Popen(
                        [tool[1], tool[2], ip], shell=True)
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
            for (key, value) in sorted(myDict.items()):
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
                    print("TreeOnSelect: {} -> {}".format(item_text, value))
            else:
                self.tree.selection_remove(item)

    def TreeOnKeyPress(self, event):
        self.RunToolFromTree()

    def TreeOnDoubleClick(self, event):
        self.RunToolFromTree()

    def RunToolFromTree(self):
        if self.toolList != {}:
            defaultTool = self.toolList[0]
            print(defaultTool)
            for item in self.tree.selection():
                item_text = self.tree.item(item, "text")
                item_value = self.tree.item(item, "value")
                if item_value != "":
                    for value in item_value:
                        print("TreeOnDoubleClick: {} -> {}".format(item_text, value))
                        ip = value
                        if (defaultTool[2] == ''):
                            subprocess.Popen([defaultTool[1], ip], shell=True)
                        else:
                            subprocess.Popen(
                                [defaultTool[1], defaultTool[2], ip], shell=True)
                else:
                    self.tree.selection_remove(item)

    def TreeOnRightClick(self, event):
        self.PopUp(event)

    def getFullItem(self, item, tree=None):
        # for key in self.tree.get_children():
        #     name = key+'.'+item
        #     NAME = key+'.'+item.upper()
        #     if self.tree.exists(name):
        #         print(f'find name={name}')
        #         return name
        #     elif self.tree.exists(NAME):
        #         print(f'find NAME={NAME}')
        #         return NAME
        #     else:
        #         print(f'did not find name={name} neither NAME={NAME}')
        #         # item = self.getFullItem(name)
        print(f'item={item}')
        myKeys = self.tree.get_children()
        print(f'myKeys={myKeys}')
        for val in myKeys:
            print(f'val={val}')
            if not re.search(rf'{item}', val, re.IGNORECASE):
                print(f'essayer avec {val}.{item}')
        return 1

    def EntryOnPressReturn(self, event):
        if self.entryVariable.get() != "Equipment to search" and self.entryVariable.get() != "":
            item = self.entryVariable.get()
            print("1."+item+".")
            # for key in self.tree.get_children():
            #     print(f'key={key}')
            item = self.getFullItem(item)
            print(f'1.item={item}')
            # if self.tree.exists(item):
            #     print("1."+item+" exists.")
            # else:
            #     print("1."+item+" does not exist.")
        else:
            self.entryVariable.set("What's up dude ?!")
            self.entry.focus_set()
        self.entry.focus_set()
        self.entry.selection_range(0, END)

    def OnButtonClick(self):
        if self.entryVariable.get() != "Equipment to search" and self.entryVariable.get() != "":
            item = self.entryVariable.get()
            print("2."+item+".")
            if self.tree.exists(item):
                print("2."+item+" exists.")
            else:
                print("2."+item+" does not exist.")
        else:
            self.entryVariable.set("What's up dude ?!")
            self.entry.focus_set()
        self.entry.selection_range(0, END)


if __name__ == "__main__":
    windowTitle = "YARCoM v0.1"
    config = LoadConfig('YARCoM.conf')
    mainWindow = MainWindow(None, windowTitle)
    equipmentList = config.LoadEquipments()
    toolsList = config.getTools()
    mainWindow.InitWidgets(equipmentList, toolsList)
    mainWindow.mainloop()
