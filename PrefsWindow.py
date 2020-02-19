#!/usr/bin/python3
# coding=utf-8

from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import filedialog
# from LoadConfig import LoadConfig
import json, os
from pathlib import *


class PrefsWindow (Tk):
    def __init__(self, parent, windowTitle, appName, file):
        Toplevel.__init__(self, parent)
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
        self.InitWindow(self.configuration)
        self.grid()
        self.minsize(600, 400)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def InitWindow(self, configuration):
        self.configTabs = ttk.Notebook(self, padding=5)

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

    def InitTools(self, parent, toolsList):
        self.toolsTree = ttk.Treeview(parent)
        self.toolsTree['columns'] = ('Path')
        self.toolsTree.column('#0', width=50, stretch=TRUE, anchor='w')
        self.toolsTree.heading('#0', text="Name")
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
        print(f'{json.dumps(toolsList, indent=4)}')
        
        if self.configuration != False:
            for tool in toolsList:
                if not os.path.exists(tool[1]):
                    messagebox.showwarning("YARCoM warning", "Erasing tool "+tool[0] +
                                           " :\ndoes not exist")
                    toolsList.remove(tool)
                    # print(f'{json.dumps(toolsList, indent=4)}')
        if toolsList:
            for tool in toolsList:
                # print(f'tool={tool}\nname={tool[0]}, bin={tool[1]}, args={tool[2]}')
                self.toolsTree.insert('', 'end', tool[0], text=tool[0], values=[tool[1], tool[2]])
        else:
            print("toolsTree est vide")

    def OnButtonClick(self, arg):
        print(f'You clicked button "{arg}"')
        if re.search(r'^tool', arg):
            item = self.toolsTree.selection()
            if item:
                print(f'OnButtonClick: {self.toolsTree.item(item, "text")} -> {self.toolsTree.item(item, "values")}')
                if re.search(r'top$', arg):
                    self.toolsTree.move(item, '', 0)
                elif re.search(r'up$', arg):
                    index = self.toolsTree.index(item)
                    self.toolsTree.move(item, '', index-1)
                elif re.search(r'add$', arg):
                    pass
                elif re.search(r'del$', arg):
                    self.toolsTree.delete(item)
                    # print(f'tree={self.toolsTree.get_children()}')
                elif re.search(r'down$', arg):
                    index = self.toolsTree.index(item)
                    self.toolsTree.move(item, '', index+1)
                elif re.search(r'bottom$', arg):
                    self.toolsTree.move(item, '', 'end')
            else:
                print("No item selected")
                if re.search(r'add$', arg):
                    pass
                    # filename = filedialog.askopenfilename()
                    # print(f'filename={filename}')
                    # addToolWindow = Toplevel(self)
                    # l1 : label + entry -> name
                    # l2 : entry + button browse (askopenfile)
                    # l3 : label + entry -> args
                    # l4 : 2 boutons (OK-CANCEL)

                    # entryToolWindow = Toplevel(self)
                    # self.entryVariable = StringVar()
                    # self.entry = Entry(entryToolWindow, textvariable=self.entryVariable)
                    # self.entry.bind("<Return>", self.EntryOnPressReturn)
                    # self.entryVariable.set("Application's name")
                    # self.entry.focus_set()
                    # self.entry.selection_range(0, END)
                    # self.entry.grid()

        if re.search(r'^file', arg):
            print("In FILE statement")

    # def EntryOnPressReturn(self, event):
    #     if self.entryVariable.get() != "Equipment to search" and self.entryVariable.get() != "":
    #         print("1."+self.entryVariable.get()+".")
    #     else:
    #         self.entryVariable.set("What's up dude ?!")
    #         self.entry.focus_set()
    #     self.entry.focus_set()
    #     self.entry.selection_range(0, END)

    def InitFiles(self, parent, filesTree):
        self.filesTree = ttk.Treeview(parent)
        self.filesTree['columns'] = ("File", "Args")
        self.filesTree.column('#0', width=30, stretch=FALSE)
        self.filesTree.heading('#0', text="#")
        self.filesTree.column('File', width=50, stretch=TRUE, anchor='w')
        self.filesTree.heading('File', text="File path")
        self.filesTree.column('Args', width=300, stretch=TRUE, anchor='w')
        self.filesTree.heading('Args', text="Proxy")
        self.filesTree.config(selectmode='browse')
        self.filesTree.grid(column=0, row=0, sticky=(N, S, E, W))

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
    prefsWindow = PrefsWindow(None, windowTitle, appName, confFile)
    prefsWindow.mainloop()
