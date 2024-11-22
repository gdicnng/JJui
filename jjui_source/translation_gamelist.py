# -*- coding: utf-8 -*-
import re

def read_translation_file( translation_file_name ,text_encoding='utf_8_sig'):
    
    translation_dict = {}
    # 内部子元素为 dict
        #   kof97
        #        translation : 拳皇97
    
    with open( translation_file_name , mode ='rt',encoding = text_encoding,errors='backslashreplace') as f:
        match_str = r'([^\t]+)\t([^\t]+)'
        p = re.compile(match_str)
        #s=r'10yard	十码大战 (世界版, 第 1 套)	十码大战 (世界版, 第 1 套)'
        
        for line in f:
            temp_str = line.strip()
            
            result = p.match( temp_str )
            
            if result:
                game_name   = result.group(1).strip().lower()
                translation = result.group(2).strip()
                if game_name and translation:
                    temp_dict={}
                    temp_dict["translation"] = translation
                    translation_dict[ game_name ] = temp_dict
    
    # 如果 python < 3.7
        # tkinter 字符不能超 U+0000-U+FFFF
        # 替换一下
        # 比如 𠀀 替换为 U+20000
        # 比如 𧉯 替换为 U+2726F
    if translation_dict:
        import sys
        if sys.version_info < (3, 7):
            replace_bigger_than_ffff = True
        else:
            replace_bigger_than_ffff = False
        
        if replace_bigger_than_ffff:
            print("")
            print("replace bigger than U+FFFF")
            
            s = r"[^\u0000-\uFFFF]"
            p = re.compile(s)
            
            def replace_func(m):
                c=m.group(0)
                #return str(  hex( ord(c) )  ) # 0xfff
                temp = format(ord(c), 'X') # FFF
                return r" U+" + temp + " "
            
            def replace_string_bigger_than_ffff(a_string):
                a_string,count = p.subn(replace_func,a_string)
                return a_string
            
            for game_name in translation_dict:
                if "translation" in translation_dict[game_name]:
                    temp_s = translation_dict[game_name]["translation"]
                    translation_dict[game_name]["translation"] = replace_string_bigger_than_ffff(temp_s)
    
    return translation_dict

# 同上，在 gamelist_dict 直接修改，不返回值了
def add_translation( translation_dict , gamelist_dict ,columns):
    
    # translation
    translation_index = None
    for n in range(len(columns)):
        if "translation" == columns[n]:
            translation_index=n
    
    # 'description'
    description_index = None
    for n in range(len(columns)):
        if "description" == columns[n]:
            description_index=n
    
    if description_index is None:
        print("")
        print("no description column")
        print("")
    else :
        if translation_index is None:
            # 如果翻译列不存在，添加一列
            
            print()
            print("add translation column")
            print()
            
            # 添加一列
            for game_name in gamelist_dict:
                gamelist_dict[ game_name ].append( gamelist_dict[ game_name ][ description_index ] )
            
            # 列 名称
            columns.append("translation")
            
            # 最后
            translation_index = -1
        
        
        print()
        print("start to translate")
        print()
        # 更新翻译
        for game_name in gamelist_dict:
            if game_name in translation_dict:
                # 翻译
                gamelist_dict[ game_name ][ translation_index ] = translation_dict[ game_name ][ "translation" ]
            else:
                # 清理，重置内容
                gamelist_dict[ game_name ][ translation_index ] = gamelist_dict[ game_name ][ description_index ]

if __name__ == "__main__" :
    pass
