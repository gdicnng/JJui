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

    filename= r"data_1.bin"

    temp = read(filename)
    
    flog1 = open('log_gamelist.txt', 'wt',encoding='utf_8_sig')
    flog2 = open('log_mame_version.txt', 'wt',encoding='utf_8_sig')
    flog3 = open('log_set_data.txt', 'wt',encoding='utf_8_sig')
    flog4 = open('log_dict_dat.txt', 'wt',encoding='utf_8_sig')
    
    print()
    
    print("data type")
    print( type(temp))
    print()
    
    print("data.kyes()")
    print( temp.keys() )
    print()

    
    if "machine_dict" in temp:
        print("machine_dict")
        n = 0
        for x in temp["machine_dict"]:
            n += 1
            print(n,end='')
            print('\t',end='')
            print(x.ljust(30),end='')
            print('\r',end='')
            print(temp["machine_dict"][x],file=flog1)
        print()


    if "mame_version" in temp:
        print( )
        print( "mame_version" )
        print( "mame_version",file=flog2 )
        print( temp["mame_version"] )
        print( temp["mame_version"] ,file=flog2)
        print()
        
    if "set_data" in temp:
        print()
        print()
        set_data = temp["set_data"]
        print( "set_data")
        print( set_data.keys() )
        for x in set_data:
            print(x,end='')
            print('\t',end='')
            print( len(set_data[x]) )
            
            for y in set_data[x]:
                print( x+ ':'+y ,file=flog3 )
                
    if "dict_data" in temp:
        print()
        print()
        dict_data = temp["dict_data"]
        print( "dict_data")
        print( dict_data.keys() )
        for x in dict_data :
            print(x)
            # dict_data["clone_to_parent"] 
            # dict_data["parent_to_clone"] 
            for y in dict_data[x]:
                print(x+':'+y+':',end='',file=flog4)
                print(dict_data[x][y],file=flog4)
        
        


    flog1.close()
    flog2.close()
    flog3.close()
    flog4.close()

