# -*- coding: utf-8 -*-

import pickle
import os
import sys

def read(filename):
    if os.path.isfile(filename):
        try:
            file = open(filename, 'rb')
            temp = pickle.load( file )
            file.close()
            return temp
        except:
            print( "read pickle failed")
            print( filename )
            sys.exit()
    else:
        print( filename ,end='')
        print( "\t is not a file,can not be read")
        sys.exit()
