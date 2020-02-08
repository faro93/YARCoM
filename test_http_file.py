from pathlib import *
import logging, requests, os, json, sys, re
from urllib.parse import urlparse

# Prevent InsecureRequestWarning message from being displayed
logging.captureWarnings(True)

def openURL (file, proxy=True):
    tree = dict()
    mystring = str()
    p = urlparse(file)
    mystring += p.netloc

    if proxy == False:
        if not 'NO_PROXY' in os.environ:
            os.environ['NO_PROXY'] = mystring
        else:
            os.environ['NO_PROXY'] += ';' + mystring

    r = requests.get(file, verify=False)
    if r.reason == 'OK':
        tree = json.loads(r.content)
        return tree
    else:
        print(f'Unable to get response from {file}')

def openLocal (file):
    tree = dict()
    if Path(file).is_file():
        with open(file) as fp:
            tree = json.load(fp)
            fp.close()
    else:
        print("No configuration loaded.")
    return tree

def MergeDict(dict1, dict2, order):
        for index in dict2['ORDER']:
            order.append(index)
        dict1.update(dict2)
        dict1['ORDER'] = order
        return order

files=[
    ['VOIP_mini.json', False],
    ['https://193.252.147.147/YARCoM/BBC_VOIP_mini.json', False],
    ['other1.json', False]]

root = dict()
order = list()
for file in files:
    tree = dict()
    print(f'{file}')
    if re.match(r'http',file[0]):
        # print(f'{file[0]} est un fichier distant')
        tree = openURL(file[0], file[1])
        # print(f'{json.dumps(tree, indent=4)}')
    else:
        # print(f'{file[0]} est un fichier local')
        tree = openLocal(file[0])
        # print(f'{json.dumps(tree, indent=4)}')
    if 'ORDER' in tree:
        order = MergeDict(root, tree, order)
    else:
        print("tree has no key 'ORDER'")

print("## root:")
print(f'{json.dumps(root, indent=4)}')
