# -*- coding: utf-8 -*-

import pickle
import sys

def save(data,filename):
    try:
        file = open( filename , 'wb' )
        pickle.dump( data , file )
        file.close(  )
        return 0
    except:
        print( "save pickle failed")
        print( "save to ")
        print( filename )
        sys.exit()

