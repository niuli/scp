import os
path='./data'
for dirpath,dirnames,filenames in os.walk(path):
    for file in filenames:
            fullpath=os.path.join(dirpath,file)
            print fullpath

