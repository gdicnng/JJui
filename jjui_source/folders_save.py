# -*- coding: utf-8 -*-
# import sys
# import os
# import re


def save(file_name,data):
    
    f = open(file_name, 'wt',encoding='utf_8_sig')
    
    print(r"[FOLDER_SETTINGS]",file=f)
    if "FOLDER_SETTINGS" in data:
        for x in sorted( data["FOLDER_SETTINGS"] ):
            print(x,file=f)
    print("",file=f)
    
    print(r"[ROOT_FOLDER]",file=f)
    if "ROOT_FOLDER" in data:
        for x in sorted( data["ROOT_FOLDER"] ) :
            print(x,file=f)
    print("",file=f)

    for x in sorted( data.keys() ):
        if x not in ("FOLDER_SETTINGS","ROOT_FOLDER"):
            temp = r"[" + x + r"]"
            print(temp,file=f)

            for y in sorted(data[x]):
                print(y,file=f)

            print("",file=f)
    
    f.close()
    

if __name__ == "__main__" :


    pass


