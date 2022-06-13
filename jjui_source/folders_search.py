# -*- coding: utf_8_sig-*-
import sys
import os

import glob

def search_ini(path,file_extension=".ini"):
    
    # 扩展名
    ext = r'*' + file_extension
        # *.ini
        # *.sl_ini
    
    
    search_str = os.path.join(path, ext)
    #print( search_str )
    
    result = glob.glob( search_str )
    #print( result )
    
    temp_dict ={ }
    
    #os.path.basename(path)
    #去掉路径，只显示文件名
    for n in range( len(result) ):
        path_and_name = result[n] 
        basename = os.path.basename( result[n] )
        temp_dict[path_and_name] = {} # 新建一个 dict
        temp_dict[path_and_name] = basename

    # temp_dict 的键值为 文件名 （不含路径）
    # 每一个素中
    # { xxx\yyy\z.ini : z.ini}
    # 可能是相对路径，可能是绝对路径
    return temp_dict
    

if __name__ == "__main__":
    
    folder_path = r'..\folders' 
    
    a = search_ini( folder_path )
    
    for x in a:
        print( x )
        print( a[x] )
        print( )
    


