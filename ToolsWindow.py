#!/usr/bin/python3
# coding=utf-8

from tkinter import *       # pylint disable=unused-wildcard-import
from tkinter import ttk     # pylint disable=unused-wildcard-import
from tkinter import PhotoImage     # pylint disable=unused-wildcard-import
from tkinter import messagebox
# from LoadConfig import LoadConfig
import json, os
from pathlib import *


class ToolsWindow (Tk):
    def __init__(self, parent, windowTitle, appName, file):
        Tk.__init__(self, parent)
        self.configurationFile = file
        if Path(self.configurationFile).is_file():
            with open(self.configurationFile) as cf:
                self.configuration = json.load(cf)
                cf.close()
                print("Configuration file "+file+" loaded.")
        else:
            print("File "+file+" does not exists")
            print("Create file "+file+" !")
            self.configuration = False

        if self.configuration != False:
            print(f'{json.dumps(self.configuration, indent=4)}')

        self.parent = parent
        self.title(windowTitle)
        self.appTitle = appName
        self.InitWindow(self.parent, self.configuration)
        self.grid()
        self.minsize(600, 400)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def InitWindow(self, parent, configuration):
        self.configTabs = ttk.Notebook(parent, padding=5)

        self.toolsFrame = ttk.Frame(self.configTabs, padding=5)
        self.configTabs.add(self.toolsFrame, text="Tools")
        self.toolsFrame.columnconfigure(0, weight=1)
        self.toolsFrame.rowconfigure(0, weight=1)
        self.InitTools(self.toolsFrame, configuration['tools'])

        self.filesFrame = ttk.Frame(self.configTabs, padding=5)
        self.configTabs.add(self.filesFrame, text="Files")
        self.filesFrame.columnconfigure(0, weight=1)
        self.filesFrame.rowconfigure(0, weight=1)
        self.InitFiles(self.filesFrame, configuration['files'])

        self.configTabs.grid(column=0, row=0, sticky=(N, S, E, W))

    def InitTools(self, parent, toolsTree):
        self.toolsTree = ttk.Treeview(parent)
        self.toolsTree['columns'] = ("Name", "Path")
        self.toolsTree.column('#0', width=30, stretch=FALSE)
        self.toolsTree.heading('#0', text="#")
        self.toolsTree.column('Name', width=50, stretch=TRUE, anchor='w')
        self.toolsTree.heading('Name', text="Name")
        self.toolsTree.column('Path', width=300, stretch=TRUE, anchor='w')
        self.toolsTree.heading('Path', text="Path")
        self.toolsTree.config(selectmode='browse')
        self.toolsTree.grid(column=0, row=0, sticky=(N, S, E, W))

        self.buttonsFrame = ttk.Frame(parent, width=100, height=100, padding=5)
        self.buttonsFrame.grid(column=1, row=0)

        self.pToolsTop = PhotoImage(file="icon_top.png")
        self.pToolsUp = PhotoImage(file="icon_up.png")
        self.pToolsAdd = PhotoImage(file="icon_toolbox.png")
        self.pToolsDel = PhotoImage(file="icon_trash.png")
        self.pToolsDown = PhotoImage(file="icon_down.png")
        self.pToolsBottom = PhotoImage(file="icon_bottom.png")

        self.top = Button(self.buttonsFrame, text="Top", image=self.pToolsTop, command=lambda arg=(
            "tool top"): self.OnButtonClick(arg)).grid(row=0, sticky=(E, W))
        self.up = Button(self.buttonsFrame, text="Up", image=self.pToolsUp, command=lambda arg=(
            "tool up"): self.OnButtonClick(arg)).grid(row=1, sticky=(E, W))
        self.adding = Button(self.buttonsFrame, text="Add", image=self.pToolsAdd, command=lambda arg=(
            "tool add"): self.OnButtonClick(arg), width=4).grid(row=2, sticky=(E, W))
        self.deleting = Button(self.buttonsFrame, text="Del", image=self.pToolsDel, command=lambda arg=(
            "tool del"): self.OnButtonClick(arg), width=4).grid(row=3, sticky=(E, W))
        self.down = Button(self.buttonsFrame, text="Down", image=self.pToolsDown, command=lambda arg=(
            "tool down"): self.OnButtonClick(arg), width=4).grid(row=4, sticky=(E, W))
        self.bottom = Button(self.buttonsFrame, text="Bottom", image=self.pToolsBottom, command=lambda arg=(
            "tool bottom"): self.OnButtonClick(arg), width=4).grid(row=5, sticky=(E, W))

        print(f'Tools:')
        print(f'{json.dumps(toolsTree, indent=4)}')
        
        if self.configuration != False:
            for tool in sorted(toolsTree):
                if not os.path.exists(toolsTree[tool]['bin']):
                    messagebox.showwarning("YARCoM warning", "Erasing tool "+str(toolsTree[tool]['name']) +
                                           " :\ndoes not exist")
                    del (toolsTree[tool])
                    print(f'{json.dumps(toolsTree, indent=4)}')
        if toolsTree:
            for key in sorted(toolsTree.keys()):
                self.toolsTree.insert('', 'end', key, text=key, values=(toolsTree[key]['name'],toolsTree[key]['bin']))
        else:
            print("toolsTree est vide")

    def OnButtonClick(self, arg):
        print(f'You clicked button "{arg}"')
        if re.match(r'^tool', arg):
            item = self.toolsTree.selection()
            if item:
                print("1.ToolsTreeOnSelect: {} -> {}".format(self.toolsTree.item(item, "text"), self.toolsTree.item(item, "values")))
                print(f'2."{arg}"')
                if re.match(r'tool top', arg):
                    self.toolsTree.move(item, '', 0)
                    self.toolsTree.item(item, text="1")
                    index = 1
                    while (item != ''):
                        item = self.toolsTree.next(item)
                        index +=1
                        self.toolsTree.item(item, text=str(index))
                elif re.match(r'up', arg):
                    pass
                elif re.match(r'add', arg):
                    pass
                elif re.match(r'del', arg):
                    pass
                elif re.match(r'down', arg):
                    pass
                elif re.match(r'bottom', arg):
                    pass
            else:
                print("No item selected")
            # for item in self.toolsTree.selection():
            #     item_text = self.toolsTree.item(item, "text")
            #     item_values = self.toolsTree.item(item, "values")
            #     if item_values != "":
            #         for value in item_values:
            #             print("2.ToolsTreeOnSelect: {} -> {}".format(item_text, value))
            #             if re.match(r'top$', arg):
            #                 print(f'item{item}')
            #             elif re.match(r'up', arg):
            #                 pass
            #             elif re.match(r'add', arg):
            #                 pass
            #             elif re.match(r'del', arg):
            #                 pass
            #             elif re.match(r'down', arg):
            #                 pass
            #             elif re.match(r'bottom', arg):
            #                 pass
                # else:
                #     self.toolsTree.selection_remove(item)
        if re.match(r'file', arg):
            print("In FILE statement")

    def InitFiles(self, parent, filesTree):
        self.tree = ttk.Treeview(parent)
        self.tree['columns'] = ("File", "Args")
        self.tree.column('#0', width=30, stretch=FALSE)
        self.tree.heading('#0', text="#")
        self.tree.column('File', width=50, stretch=TRUE, anchor='w')
        self.tree.heading('File', text="File path")
        self.tree.column('Args', width=300, stretch=TRUE, anchor='w')
        self.tree.heading('Args', text="Proxy")
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
            "file top"): self.OnButtonClick(arg)).grid(row=0, sticky=(E, W))
        up = Button(self.buttonsFrame, text="Up", image=self.pFilesUp, command=lambda arg=(
            "file up"): self.OnButtonClick(arg)).grid(row=1, sticky=(E, W))
        addurl = Button(self.buttonsFrame, text="Add URL", image=self.pFilesAddL, command=lambda arg=(
            "file add URL"): self.OnButtonClick(arg)).grid(row=2, sticky=(E, W))
        addfile = Button(self.buttonsFrame, text="Add Local", image=self.pFilesAddF, command=lambda arg=(
            "file add local"): self.OnButtonClick(arg)).grid(row=3, sticky=(E, W))
        deleting = Button(self.buttonsFrame, text="Del", image=self.pFilesDel, command=lambda arg=(
            "file del"): self.OnButtonClick(arg)).grid(row=4, sticky=(E, W))
        down = Button(self.buttonsFrame, text="Down", image=self.pFilesDown, command=lambda arg=(
            "file down"): self.OnButtonClick(arg)).grid(row=5, sticky=(E, W))
        bottom = Button(self.buttonsFrame, text="Bottom", image=self.pFilesBottom, command=lambda arg=(
            "file bottom"): self.OnButtonClick(arg)).grid(row=6, sticky=(E, W))

        # print(f'Files:')
        # print(f'{json.dumps(filesTree, indent=4)}')



if __name__ == "__main__":
    windowTitle = "Preferences ..."
    appName = "YARCoM v0.1"
    confFile = "YARCoM.conf"
    toolsWindow = ToolsWindow(None, windowTitle, appName, confFile)
    # equipmentList = config.LoadEquipments()
    toolsWindow.mainloop()
