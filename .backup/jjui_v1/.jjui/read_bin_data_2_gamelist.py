# -*- coding: utf_8_sig-*-
import sys
import os

import pickle
def read(filename):
    f = open(filename, 'rb')
    temp = pickle.load(f)
    f.close()
    return temp

if __name__ == "__main__" :

    filename= r"data_2_gamelist.bin"

    temp = read(filename)
    
    flog1 = open('log_data_2_gamelist.txt', 'wt',encoding='utf_8_sig')
    
    for x in temp:
        print(temp[x],file=flog1)

    flog1.close()


