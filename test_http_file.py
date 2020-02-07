from pathlib import *
import logging, requests, os, json, sys
from urllib.parse import urlparse

# Prevent InsecureRequestWarning message from being displayed
logging.captureWarnings(True)

def openURL (myList, proxy=True):
    root = dict()
    mystring = ''
    for url in range(len(myList)):
        p = urlparse(myList[url])
        mystring += p.netloc
        print(f'{mystring}')
        if url < len(myList)-1:
            mystring += ';'

    if proxy == False:
        os.environ['NO_PROXY'] = mystring

    for url in urls:
        r = requests.get(url, verify=False)
        rep = r.text.splitlines()
        for l in rep:
            print(f'{l}')

def openFile (myList):
    root = dict()
    order = list()
    for file in myList:
        if Path(file).is_file():
            with open(file) as fp:
                tree = json.load(fp)
                order = MergeDict(root, tree, order)
                fp.close()
        else:
            print("No configuration loaded.")
    return root

def MergeDict(dict1, dict2, order):
        for index in dict2['ORDER']:
            order.append(index)
        dict1.update(dict2)
        dict1['ORDER'] = order
        return order

files=[['VOIP_mini.json',False],
    ['https://193.252.147.147/YARCoM/BBC_VOIP_mini.json', False]]

urls=['https://193.252.147.147/YARCoM/BBC_VOIP_mini.json']
file=['VOIP_mini.json']
openURL(urls, False)
myDict = openFile(file)
print(f'{json.dumps(myDict, indent=4)}')

for f in files:
    print(f'{f}')
    files = list()
    urls = list()
    if re.match(r'http',f[0]):
        print(f'{f}')

    # if Path(f).is_file():
    #     files.append(f)
    # p = urlparse(f)
    # if p.scheme() == 'http':
    #     urls.append()