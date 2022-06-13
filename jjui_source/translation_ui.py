# -*- coding: utf_8_sig-*-
"""
    翻译文件编码用 utf_8_sig
    
    Translation 不分类
        格式为 dict
            子元素：Translation[原文] = 译文
            
"""
import os
import re

class Translation_Dict():

    def __init__(       self,
                        translation_file=None ,
                        translation_dict=None ,
                        ):
        
        self.translation_dict={} # 初始化
        
        if translation_file is not None:
            if os.path.exists(translation_file):
                if os.path.isfile(translation_file):
                    self.get_translation_dict_from_file(translation_file)

        if type(translation_dict)==dict:
            if translation_dict:
                self.get_translation_dict_from_dict(translation_dict)

    def get_translation_dict_from_file(self,file_name):
        
        def read_a_text(file_name):
            lines = []
            with open( file_name ,mode = 'rt',encoding = 'utf_8_sig' ) as file:
                lines = file.readlines()
            return lines
        
        # 不分类
        def convert(file_name):
            # 原文 \t 译文     r'^(.+)\t(.+)$'

            content = read_a_text( file_name )
            
            temp_dict = {}
                # 元素为 原文 译文

            # 内容  原文 \t 译文
            search_str_2 = r'^(.+)\t(.+)$'
            p2=re.compile( search_str_2, )
            
            # 空行
            search_str_empty =r'^\s*$'
            p_empty = re.compile( search_str_empty , )

            ##### 正则
            for line in content:
            
                # 空行测试
                m=p_empty.search( line ) 
                if m : 
                    continue
                
                # 内容行
                m=p2.search( line )
                if m:
                    temp_dict[m.group(1)]=m.group(2)

            return temp_dict
        
        translation_dict = convert(file_name)
        
        self.translation_dict =  translation_dict

    def get_translation_dict_from_dict(self,temp_dict):
        self.translation_dict = temp_dict

    def return_translation_dict(self,):
        return self.translation_dict
    
    def translation(self,key):
        if key in self.translation_dict:
            return self.translation_dict[key]
        else:
            return key

translation_holder = Translation_Dict()



if __name__ == "__main__" :

    file_name = "lang_test.txt"
    #translation_holder
    
    translation_holder.get_translation_dict_from_file(file_name)
    
    for k,v in translation_holder.translation_dict.items():
        print()
        print(k)
        print(v)
    
    
    _ = translation_holder.translation
    print(_(""))
    print(_("abc"))
    print(_("bbc"))
    print(_("test"))