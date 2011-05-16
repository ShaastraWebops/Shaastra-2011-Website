#  find_n_replace.py
#  creates a list of ALL the files in the dierctory given by "path"
#  in each of the files in the list, finds "old" and replaces it with "new"

import os
import re

path =     #the root dir path eg. '/home/sujeet/userportal/templates'
old =      #the word to be replaced  
new =      #the new word

filepaths = []
for root, dirs, files in os.walk(path) :
    for fil in files :
        filepath = root + "/" + fil
        filepaths.append(filepath)
        
for fil in filepaths :
    print
    src = fil
    dest = fil + "2"
    o = open(dest,"w")
    data = open(src).read()
    o.write( re.sub(old,new,data) )
    o.close()
    os.rename(dest,src)