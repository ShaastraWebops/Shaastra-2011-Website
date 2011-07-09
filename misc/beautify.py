#####################################
# 9 July 2011                       #
# Sujeet Gholap for shaastra webops #
#####################################

from BeautifulSoup import BeautifulSoup
import os
import sys

def parse_arguments (arguments) :
    if len (arguments) != 2 :
        print "usage   : python " + arguments[0] + " <absolute_path_to_the_base_directory>"
        print "example : python " + arguments[0] + " /home/sujeet/main_test/templates/"
        sys.exit(1)
    else :
        return arguments [1]
        

if __name__ == "__main__" :
    path_to_base_dir = parse_arguments (sys.argv)

    # make a list of all passible file with their full paths
    # which are inside the base directory.
    filepaths = []
    for root, dirs, file_names in os.walk(path_to_base_dir) :
        for file_name in file_names :
            if file_name[-3:] == "htm" or file_name[-3:] == "tml" :
                filepath = root + "/" + file_name
                filepaths.append(filepath)
        
    # now filepath has list of ALL the html files in the directory
    # even those in subdirs and all.
    for file_name in filepaths :
        src = file_name
        dest = file_name + "2"
        data = open(src).read()
        try :
            dest_file = open(dest,"w")
            dest_file.write( BeautifulSoup(data).prettify().__str__() )
            dest_file.close()
            os.rename(src, src + ".tidy.backup")
            os.rename(dest,src)
        except :
            print "ERROR : " + src + "could not be beautified :("
