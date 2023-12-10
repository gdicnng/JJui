# -*- coding: utf_8_sig-*-
import sys
import os
import pickle
import re
import time

def read_translation_file( translation_file_name ,text_encoding='utf_8_sig'):
    f = open( translation_file_name , 'rt',encoding = text_encoding)

    translation_dict = {}
    # 内部子元素为 dict
    # {  }
    #   name : kof97
    #   translation : 拳皇97

    p = r'^([^\t ]+)\t([^\t]+)'
    prog = re.compile(p)
    #s=r'10yard	十码大战 (世界版, 第 1 套)	十码大战 (世界版, 第 1 套)'
    #result = re.match(p, s)

    temp_str = f.readline()

    while temp_str :
        result = prog.match( temp_str )
        if result:
            temp_dict = {}
            temp_dict["name"] = result.group(1)
            temp_dict["translation"] = result.group(2)
            translation_dict[ result.group(1) ] = temp_dict
            #print(result.group(1),end='\t')
            #print(result.group(2),)
        temp_str = f.readline()

    f.close()
    return translation_dict

# 加上翻译
#   "translation" : xxxxxxxxx,
# 原数据元素：
#    { 'name': 'kof97', 'description': "The King of Fighters '97 (NGM-2320)", ...... }
# 新数据元素：
#    { 'name': 'kof97', 'description': "The King of Fighters '97 (NGM-2320)", 'translation': "拳皇 '97 (NGM-2320)",.......}
def add_translation( translation_dict , gamelist_dict ):

    ######
    # 翻译

    for game_name in gamelist_dict:
        if game_name in translation_dict:
            gamelist_dict[ game_name ][ "translation" ] = translation_dict[ game_name ][ "translation" ]
        else: 
            # 如果没有翻译，则补上原文内容
            gamelist_dict[ game_name ][ "translation" ] = gamelist_dict[ game_name ][ "description" ] 
    ######

    return gamelist_dict



if __name__ == "__main__" :

    # 翻译 文件
    translation_file_name = r'translation.txt'
    
    # gamelist 数据 文件
    gamelist_file_name = r'cache_data_2_gamelist.bin' # pickle file
    
    if os.path.isfile(gamelist_file_name):
        if os.path.isfile(translation_file_name):
            # 读取翻译
            print("")
            print("读取翻译")
            print("read translation file")
            translation_dict = read_translation_file( translation_file_name )
            l = len(translation_dict)
            print( l )
            
            if l > 0:
                
                # 读取 gamelist 数据
                print("")
                print("读取 游戏列表文件")
                print("read game list file")
                f1 = open( gamelist_file_name , 'rb')
                data = pickle.load( f1 )
                f1.close()
                
                # 添加翻译内容
                print("")
                print("添加翻译内容")
                print("add translation")            
                new_data = add_translation( translation_dict = translation_dict , 
                                            gamelist_dict = data )
                
                # gamelist 数据，重新写入
                print("")
                print("写入文件")
                print("write to file")              
                f2 = open( gamelist_file_name , 'wb')
                pickle.dump( new_data , f2 )
                f2.close
                
                print("")
                print("完成")
                print("finish")
                
                time.sleep(2)

