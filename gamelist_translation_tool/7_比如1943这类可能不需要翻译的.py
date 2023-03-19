# -*- coding: utf_8_sig-*- 

# 整体翻译后，是否再 对 小分类 翻译
type_of_tranlsation = "SL"
#type_of_tranlsation = "FBNeo"
#type_of_tranlsation = "other"
# "SL" ,翻译后，再搜索 resources_for_translation__part_1__specific 文件夹，对子分类，翻译
# "FBNeo" ,翻译后，再搜索 resources_for_translation__part_1__specific 文件夹，对子分类，翻译

"""
    上一步，翻译后，
    没有翻译的项目，记录在
        out_translated__not_translated__id_english.txt
    
    对于没有翻译的条目，
    再追加一些
    比如 
        1943 (????)
            这种纯数字，括号前，其实不用翻译也能看，
            括号后的部分，翻译一下版本信息，将就
        其它的，比如只有一个字母的
    
    结果：
    out_translated_more__id_chinese.txt
    out_translated_more__id_chinese_chinese.txt
    out_translated_more__id_chinese_english.txt
    好像很少
    
"""

import sys
import os
import re

from source_py_some_scripts import misc
from source_py_some_scripts import the_files
from source_py_some_scripts import the_variables
from source_py_some_scripts import the_first_part
from source_py_some_scripts import the_second_part
from source_py_some_scripts import split_string_to_two_part
from source_py_some_scripts import multi_space_to_single

###########
id_english_text_file                = the_files.file__translated_for_not_translated_id_english

# 括号前的 翻译源，第一部分 英文 \t 中文
english_chinese_folder              = the_files.english_chinese_folder
# 括号后 翻译源，第二部分 英文 \t 中文
english_chinese_folder_second_part  = the_files.english_chinese_folder_second_part
# sl 、fbn 等，分类 再翻译
english_chinese_folder_specific=the_files.english_chinese_folder_for_single_xml

# 往里面追加内容
out_text_final_id_chinese               = the_files.file__translated_more_id_chinese
out_text_final_id_chinese_chinese       = the_files.file__translated_more_id_chinese_chinese
out_text_final_id_chinese_english       = the_files.file__translated_more_id_chinese_english


###########################
misc.for_print_error_python34()

# 切换工作目录
def change_working_directory():

    if getattr(sys, "frozen", False):
        # cx_Freeze 打包 忘了
        # pyinstall 打包 目录模式
        
        # The application is frozen
        executable_path = os.path.dirname(sys.executable)
        executable_path = os.path.abspath(executable_path)
        os.chdir( executable_path )
    else:
        # 以 python 脚本模式 运行
        
        # The application is not frozen
        # Change this bit to match where you store your data files:
        the_script_path = os.path.dirname(__file__)
        the_script_path = os.path.abspath(the_script_path)
        os.chdir( the_script_path )

change_working_directory()

################

# id english dict
id_english_dict = misc.read_id_english_file( id_english_text_file )

# english chinese dict
english_chinese_dict = dict()
the_txt_file_list = misc.search_txt_files_in_a_folder( english_chinese_folder )
for a_txt_file in the_txt_file_list:
    print()
    try:temp=os.path.relpath(a_txt_file)
    except:temp=a_txt_file
    print("\t",temp)
    temp = misc.read_english_chinese_file( a_txt_file )
    english_chinese_dict.update( temp )
del the_txt_file_list

# english chinese dict
# second part
english_chinese_dict_second_part = dict()
the_txt_file_list = misc.search_txt_files_in_a_folder( english_chinese_folder_second_part )
for a_txt_file in the_txt_file_list:
    print()
    try:temp=os.path.relpath(a_txt_file)
    except:temp=a_txt_file
    print("\t",temp)
    temp = misc.read_english_chinese_file( a_txt_file )
    english_chinese_dict_second_part.update( temp )
del the_txt_file_list

# id_translated_dict
id_translated_dict = misc.translate_only_part_2(
        id_english_dict,
        english_chinese_dict,
        english_chinese_dict_second_part)

# 以上为 整体
###################
###################
# 以下为 SL ，是否再 使用 每一个 子分类，翻译
if type_of_tranlsation == "SL" or type_of_tranlsation == "FBNeo":
    
    print()
    
    if type_of_tranlsation == "SL":
        print("SL")
        separator_character = " "
    elif type_of_tranlsation == "FBNeo":
        print("FBNeo")
        separator_character = r"_" # _
    
    # xml 名称，nes 、gba 、…… 等，用于查找 对应的文件夹
    def sl_get_xml_name(id_english_dict):
        xml_name_set = set()
        
        for the_id in id_english_dict:
            the_id = the_id.strip()
            
            if separator_character in the_id:
                xml_name = the_id.split(separator_character,maxsplit=1)[0]
                xml_name_set.add(xml_name)
        
        return xml_name_set
    
    xml_name_set = sl_get_xml_name(id_english_dict)
    #print(xml_name_set)
    
    
    xml_translation_resource_folder_dict = dict()
        # xml_name : folder_path
            # nes : (文件夹路径)?????\nes
    if os.path.isdir( english_chinese_folder_specific ):
        
        #if os.path.isdir( english_chinese_folder_specific ):
        
        the_folder = os.path.abspath( english_chinese_folder_specific )
        
        (dirpath, dirnames, filenames) = next( os.walk( the_folder ) )
        
        for folder_name in dirnames:
            xml_name = folder_name.lower()
            if xml_name in xml_name_set:
                xml_translation_resource_folder_dict[xml_name]=os.path.join( dirpath , folder_name )
    
    # 对 每个 sl 的 xml 文件夹
    if xml_translation_resource_folder_dict:
        for xml_name,folder_path in xml_translation_resource_folder_dict.items():
            print()
            print(xml_name,":: ",end="")
            try:# 相对路径
                temp = os.path.relpath(folder_path)
            except:
                temp = folder_path
            print("folder ::",temp)
            
            # 翻译范围
            id_english_dict_specific = dict()
            temp = xml_name + separator_character # id 为 xml 加空格 开头 #FBN id_
            for the_id,english in id_english_dict.items():
                if the_id.startswith(temp):
                    id_english_dict_specific[the_id]=english
            
            # 翻译资源
            english_chinese_dict_specific = dict()
            the_txt_file_list = misc.search_txt_files_in_a_folder( folder_path )
            for a_txt_file in the_txt_file_list:
                print()
                
                try:temp = os.path.relpath(a_txt_file) # 相对路径
                except:temp = a_txt_file
                
                print(xml_name,":","\t",temp)
                temp = misc.read_english_chinese_file( a_txt_file )
                english_chinese_dict_specific.update( temp )
            
            # 翻译结果
            id_translated_dict_specific = misc.translate_only_part_2(
                    id_english_dict_specific,
                    english_chinese_dict_specific,
                    english_chinese_dict_second_part)
            
            # 更新 到 总体翻译
            id_translated_dict.update( id_translated_dict_specific )
#####################
#####################


##################
##################
# 以下为翻译后，结果写出

# 结果
misc.write_to_text__id_chinese( out_text_final_id_chinese,         id_translated_dict , )
misc.write_to_text__id_chinese( out_text_final_id_chinese_chinese ,id_translated_dict ,
        double_chinese=True )
misc.write_to_text__id_chinese( out_text_final_id_chinese_english ,id_translated_dict ,
        id_english_dict = id_english_dict,english=True )
