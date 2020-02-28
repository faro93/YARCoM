#!/usr/bin/python3
# coding=utf-8

from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import filedialog
# from LoadConfig import LoadConfig
import json
import os
import logging
import requests
from pathlib import *
from urllib.parse import urlparse
from URLWindow import URLWindow


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
            self.toolsList = self.configuration['tools']
            self.filesList = self.configuration['files']

        self.appName = appName
        self.parent = parent
        self.title(windowTitle)
        self.appTitle = self.appName
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
        self.InitTools(self.toolsFrame)

        self.filesFrame = ttk.Frame(self.configTabs, padding=5)
        self.configTabs.add(self.filesFrame, text="Files")
        self.filesFrame.columnconfigure(0, weight=1)
        self.filesFrame.rowconfigure(0, weight=1)
        self.InitFiles(self.filesFrame)

        self.configTabs.grid(column=0, row=0, sticky=(N, S, E, W))

    def InitTools(self, parent):
        self.toolsTree = ttk.Treeview(parent)
        self.toolsTree['columns'] = ('Path')
        self.toolsTree.column('#0', width=50, stretch=TRUE, anchor='w')
        self.toolsTree.heading('#0', text="Name")
        self.toolsTree.column('Path', width=300, stretch=TRUE, anchor='w')
        self.toolsTree.heading('Path', text="Path")
        self.toolsTree.config(selectmode='browse')
        self.toolsTree.grid(column=0, row=0, sticky=(N, S, E, W), columnspan=3)

        self.buttonsFrame = ttk.Frame(parent, width=100, height=100, padding=5)
        self.buttonsFrame.grid(column=4, row=0)

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

        self.okFrame = ttk.Frame(parent, padding=5)
        self.okFrame.grid(column=2, row=1)
        self.cancelFrame = ttk.Frame(parent, padding=5)
        self.cancelFrame.grid(column=4, row=1)

        self.ok = Button(self.okFrame, text="OK", command=lambda arg=(
            "tool OK"): self.OnButtonClick(arg), width=5, padx=4, pady=4).grid(column=0, row=0)
        self.cancel = Button(self.cancelFrame, text="Cancel", command=lambda arg=(
            "tool CANCEL"): self.OnButtonClick(arg), width=5, padx=4, pady=4).grid(column=1, row=0)

        # print(f'Tools:')
        # print(f'{json.dumps(self.toolsList, indent=4)}')

        if self.configuration != False:
            for tool in self.toolsList:
                if not os.path.exists(tool[1]):
                    messagebox.showwarning("YARCoM warning", "Erasing tool "+tool[0] +
                                           " :\ndoes not exist")
                    self.toolsList.remove(tool)
                    # print(f'{json.dumps(self.toolsList, indent=4)}')
        if self.toolsList:
            self.GenerateTree('tools')
        else:
            print("toolsList est vide")

    def InitFiles(self, parent):
        self.filesTree = ttk.Treeview(parent)
        self.filesTree['columns'] = ('Path')
        self.filesTree.column('#0', width=50, stretch=TRUE, anchor='w')
        self.filesTree.heading('#0', text="Name")
        self.filesTree.column('Path', width=300, stretch=TRUE, anchor='w')
        self.filesTree.heading('Path', text="Path")
        self.filesTree.config(selectmode='browse')
        self.filesTree.grid(column=0, row=0, sticky=(N, S, E, W), columnspan=3)

        self.buttonsFrame = ttk.Frame(parent, height=100, padding=5)
        self.buttonsFrame.grid(column=4, row=0)

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

        self.okFrame = ttk.Frame(parent, padding=5)
        self.okFrame.grid(column=2, row=1)
        self.cancelFrame = ttk.Frame(parent, padding=5)
        self.cancelFrame.grid(column=4, row=1)

        self.ok = Button(self.okFrame, text="OK", command=lambda arg=(
            "file OK"): self.OnButtonClick(arg), width=5, padx=4, pady=4).grid(column=0, row=0)
        self.cancel = Button(self.cancelFrame, text="Cancel", command=lambda arg=(
            "file CANCEL"): self.OnButtonClick(arg), width=5, padx=4, pady=4).grid(column=1, row=0)

        # print(f'Files:')
        # print(f'{json.dumps(self.filesList, indent=4)}')

        if self.configuration:
            for f in self.filesList:

                if re.match(r'http', f[1]):
                    if f[2] == 'False':
                        f[2] = False
                    else:
                        f[2] = True
                    ok = self.checkURL(f[1], f[2])
                    if not ok:
                        self.filesList.remove(f)
                else:
                    if not os.path.exists(f[1]):
                        messagebox.showwarning("YARCoM warning", "1.Erasing file "+f[1] +
                                               " :\ndoes not exist")
                        self.filesList.remove(f)
                # print(f'{json.dumps(self.filesList, indent=4)}')
        if self.toolsList:
            self.GenerateTree('files')
        else:
            print("filesList est vide")

    def checkURL(self, file, proxy=None):
        # Prevent InsecureRequestWarning message from being displayed
        logging.captureWarnings(True)

        result = True
        myString = str()
        p = urlparse(file)
        myString += p.netloc

        if not proxy:
            if not 'NO_PROXY' in os.environ:
                os.environ['NO_PROXY'] = myString
            else:
                s = os.environ['NO_PROXY']
                l = s.split(';')
                if not myString in l:
                    os.environ['NO_PROXY'] += ';' + myString


        try:
            requests.get(file, verify=False)
        except requests.exceptions.ConnectionError as ce:
            messagebox.showwarning(
                "YARCoM warning", "Unable to load file "+str(file)+"\n"+str(ce))
            result = False
        except requests.exceptions.ConnectionRefusedError as cre:
            messagebox.showwarning(
                "YARCoM warning", "Unable to load file "+str(file)+"\n"+str(cre))
            result = False

        return result

    def GenerateTree(self, notebook):
        if re.search(r'^tools', notebook):
            myList = self.toolsList
            tree = self.toolsTree
        elif re.search(r'^files', notebook):
            myList = self.filesList
            tree = self.filesTree

        for index in myList:
            # print(f'name={index[0]}, bin={index[1]}, args={index[2]}')
            # print(f'index={index}')
            tree.insert('', 'end', index[0], text=index[0], values=[index[1], index[2]])

    def OnButtonClick(self, arg):
        print(f'You clicked button "{arg}"')
        if re.search(r'^tool', arg):
            self.ManageButtons(arg)
        elif re.search(r'^file', arg):
            self.ManageButtons(arg)
        else:
            print("This tab is not manage : does not exist !")

    def ManageButtons(self, arg):
        if re.search(r'^tool', arg):
            tree = self.toolsTree
            # print(f'listItem={self.toolsTree.get_children()}')
        elif re.search(r'^file', arg):
            tree = self.filesTree
            # print(f'listItem={self.filesTree.get_children()}')
            # for item in self.filesTree.get_children():
                # print(f'self.filesTree.item({item})={self.filesTree.item(item)}')

        item = tree.selection()
        if item:
            """item selected"""
            print(
                f'OnButtonClick: {tree.item(item, "text")} -> {tree.item(item, "values")}')
            if re.search(r'top$', arg):
                tree.move(item, '', 0)
            elif re.search(r'up$', arg):
                index = tree.index(item)
                tree.move(item, '', index-1)
            elif re.search(r'add$', arg):
                self.AddToList(arg, item=item)
            elif re.search(r'add URL$', arg):
                pass
            elif re.search(r'add local$', arg):
                self.AddToList(arg, item)
            elif re.search(r'del$', arg):
                tree.delete(item)
                # print(f'tree={tree.get_children()}')
            elif re.search(r'down$', arg):
                index = tree.index(item)
                tree.move(item, '', index+1)
            elif re.search(r'bottom$', arg):
                tree.move(item, '', 'end')
            elif re.search(r'CANCEL$', arg):
                self.Cancel(arg)
            elif re.search(r'OK$', arg):
                self.OK(arg)
        else:
            """no item selected"""
            print("No item selected")
            if re.search(r'add$', arg):
                self.AddToList(arg)
            elif re.search(r'add URL$', arg):
                urlWindow = URLWindow(self, "Add URL file ...", "YARCoM v0.1")
                self.wait_window(urlWindow)
                print(f'urlWindow.result={urlWindow.result}')
                self.AddToList(arg, result=urlWindow.result)
            elif re.search(r'add local$', arg):
                self.AddToList(arg)
            elif re.search(r'CANCEL$', arg):
                self.Cancel(arg)
            elif re.search(r'OK$', arg):
                self.OK(arg)

    def AddToList(self, arg, item=None, result=None):
        if re.search(r'^tool', arg):
            tree = self.toolsTree
            title = 'Select new tool'
        elif re.search(r'^file', arg):
            tree = self.filesTree
            title = 'Select new equipment file'

        if item is not None:
            index = tree.index(item)

        if re.search(r'^tool', arg):
            if not os.name == "posix":
                filename = filedialog.askopenfilename(title=title, filetypes=(
                    ("exe files", "*.exe"), ("all files", "*.*")))
            else:
                filename = filedialog.askopenfilename(title=title)
        elif re.search(r'^file', arg):
            if re.search(r'add local$', arg):
                filename = filedialog.askopenfilename(title=title, filetypes=(
                    ("json files", "*.json"), ("all files", "*.*")))
            elif re.search(r'add URL$', arg):
                # print(f'type(result)={type(result)}, result={result}')
                (filename, proxy) = (result[0], result[1])
                if proxy == 0:
                    proxy = False
                else:
                    proxy = True
                # print(f'filename={filename}, proxy={proxy}')

        if re.search(r'^tool', arg):
            if filename:
                p = filename.split("/")
                name = (p[-1].split(r'\.'))[0].capitalize()
                if os.name != "posix":
                    path = '\\'.join(p)
                    args = ''
                else:
                    path = filename
                    args = ''
                if item is not None:
                    tree.insert('', index+1, name, text=name,
                                values=[path, args])
                else:
                    tree.insert('', 'end', name, text=name,
                                values=[path, args])
            else:
                print(f'No file selected for tool')

        elif re.search(r'^file', arg):
            if filename:
                if re.search(r'http', filename):
                    path = filename
                    ok = self.checkURL(filename, proxy)
                    if ok:
                        p = urlparse(filename)
                        name = p.path.split(r'/')[-1]
                        if item is not None:
                            tree.insert('', index+1, name,
                                        text=name, values=[path, proxy])
                        else:
                            tree.insert('', 'end', name,
                                        text=name, values=[path, proxy])

                else:
                    p = filename.split("/")
                    name = p[-1]
                    if not os.name == "posix":
                        path = '\\'.join(p)
                        proxy = 'False'
                    else:
                        path = filename
                        proxy = 'False'
                    if item is not None:
                        tree.insert('', index+1, name,
                                    text=name, values=[path, proxy])
                    else:
                        tree.insert('', 'end', name, text=name, values=[path, proxy])
            else:
                print(f'No file selected file')
        # print(f'listItem={self.filesTree.get_children()}')

    def Cancel(self, arg):
        if re.search(r'^tool', arg):
            tree = self.toolsTree
            notebook = 'tools'
        elif re.search(r'^file', arg):
            tree = self.filesTree
            notebook = 'files'

        listTree = tree.get_children()
        for item in listTree:
            tree.delete(item)
        self.GenerateTree(notebook)
        self.destroy()

    def OK(self, arg):
        if re.search(r'^tool', arg):
            tree = self.toolsTree
            notebook = 'tools'
        elif re.search(r'^file', arg):
            tree = self.filesTree
            notebook = 'files'

        self.configuration[notebook].clear()
        for item in tree.get_children():
            name = tree.item(item, "text")
            if re.search(r'^tool', arg):
                (path, args) = tree.item(item, "values")
                self.configuration[notebook].append([name, path, args])
            elif re.search(r'^file', arg):
                (path, proxy) = tree.item(item, "values")
                self.configuration[notebook].append([name, path, proxy])

            with open(self.configurationFile, 'w', encoding='utf-8') as cf:
                json.dump(self.configuration, cf,
                          ensure_ascii=False, indent=4)
        self.destroy()


if __name__ == "__main__":
    windowTitle = "Preferences ..."
    appName = "YARCoM v0.1"
    confFile = "YARCoM.conf"
    prefsWindow = PrefsWindow(None, windowTitle, appName, confFile)
    prefsWindow.mainloop()
