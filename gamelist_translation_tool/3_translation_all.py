# -*- coding: utf_8_sig-*- 
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

# 整体翻译后，是否再 对 小分类 翻译
#type_of_tranlsation = "all"
type_of_tranlsation = "SL"
#type_of_tranlsation = "FBNeo"


id_english_text_file                = the_files.file__id_to_english

# 括号前的 翻译源，第一部分 英文 \t 中文
english_chinese_folder              = the_files.english_chinese_folder
# 括号后 翻译源，第二部分 英文 \t 中文
english_chinese_folder_second_part  = the_files.english_chinese_folder_second_part
# sl 、fbn 等，分类 再翻译
english_chinese_folder_specific=the_files.english_chinese_folder_for_single_xml

out_text_final_id_chinese               = the_files.file__translated_id_chinese
out_text_final_id_chinese_chinese       = the_files.file__translated_id_chinese_chinese
out_text_final_id_chinese_english       = the_files.file__translated_id_chinese_english
out_text_for_not_translated_id          = the_files.file__translated_for_not_translated_id
out_text_for_not_translated_id_english  = the_files.file__translated_for_not_translated_id_english
out_text_for_not_translated_english_lower     = the_files.file__translated_for_not_translated_english_lower
out_text_for_not_translated_2nd_part_english  = the_files.file__translated_for_not_translated_2nd_part_english



###########################

"""
    
    读取 原始文件： id \t 英文
    
    翻译
        英文两部分，括号前 与 括号后
        
        括号前
            读取 文件：英文 \t 中文
                在文件夹中搜索所有的 .txt 文件
        括号后
            读取 文件：英文 \t 中文
                在文件夹中搜索所有的 .txt 文件
"""

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


# id \t 英文
def read_id_english_file(file_name):

    gamelist_dict ={}
    # id 
        # 英文

    search_str = r'^([^\t]+)\t([^\t]+)'
    p=re.compile( search_str, )
    
    with open(file_name,mode="rt",encoding="utf_8_sig") as f:
        for line in f:
            #print(line)
            line=line.strip()
            
            m=p.search( line ) 
            if m:
                the_id  = m.group(1)
                english = m.group(2)
                
                gamelist_dict[ the_id ] = english
    
    return gamelist_dict

# 英文 \t 中文
def read_english_chinese_file(file_name):
    
    temp_dict ={}
    # 英文：中文

    search_str = r'^([^\t]+)\t([^\t]+)'
    p=re.compile( search_str, )
    
    with open(file_name,mode="rt",encoding="utf_8_sig") as f:
        for line in f:
            #print(line)
            line=line.strip()
            
            m=p.search( line ) 
            if m:
                english = m.group(1)
                chinese = m.group(2)
                
                if english == chinese:
                    continue
                if misc.is_ascii(chinese):
                    continue
                
                english_part_1,english_part_2 = split_string_to_two_part.main( english )
                
                # 处理
                english = the_first_part.main( english_part_1 )
                
                english = english.lower()
                
                chinese_part_1,chinese_part_2 = split_string_to_two_part.main_cn( chinese )
                
                chinese_part_1 = the_first_part.main_cn(chinese_part_1)
                
                if english and chinese_part_1:# 非空
                    temp_dict[ english ] = chinese_part_1
    
    return temp_dict

def translate(id_english_dict,english_chinese_dict,english_chinese_dict_second_part=None):
    
    if english_chinese_dict_second_part is None:
        english_chinese_dict_second_part = dict()
    
    separators = set( the_variables.string_separators_for_second_part )
    
    id_translated_dict = {}

    for game_id,english in id_english_dict.items():
        
        english_part_1,english_part_2 = split_string_to_two_part.main(english)
        
        # 之间的空格
        # 翻译后，加回去
        space_between = ""
        if english_part_1.endswith(" "):
            space_between=" "
        
        # 括号前的部分
        the_string_need_to_be_translate = the_first_part.main( english_part_1 )
        
        the_string_need_to_be_translate = the_string_need_to_be_translate.lower()
        
        if the_string_need_to_be_translate in english_chinese_dict:
            
            # 第一部分有翻译，再操作第二部分
            second_part_translated_flag = False
            if english_chinese_dict_second_part and english_part_2:
                english_part_2 = english_part_2.strip()
                if english_part_2:
                    the_split_english_list = the_second_part.split( english_part_2 , keep_separator = True )
                    
                    for n in range( len(the_split_english_list) ):
                        
                        temp_string = the_split_english_list[n]
                        
                        # 记录 左 右 的空格，翻译后，把空格加回去,基本保持原有格式
                        empty_left  = ""
                        empty_right = ""
                        if temp_string.startswith(" ") : empty_left  =" "
                        if temp_string.endswith(" ")   : empty_right =" "
                        
                        temp_string = temp_string.strip()#
                        
                        if not temp_string : # 空字符
                            continue
                        
                        temp_string = multi_space_to_single.main( temp_string )
                        
                        if len(temp_string) == 1 :# 单字符，不译
                            continue
                        
                        temp_string = temp_string.lower() # 全转小写
                        
                        if temp_string in english_chinese_dict_second_part:
                            second_part_translated_flag = True
                            the_split_english_list[n] = "".join(
                                        [
                                        empty_left,
                                        english_chinese_dict_second_part[temp_string],
                                        empty_right,
                                        ]
                                            )
                    
                    if second_part_translated_flag:
                        english_part_2="".join( the_split_english_list )
            
            id_translated_dict[game_id] = english_chinese_dict[the_string_need_to_be_translate] + space_between + english_part_2
        else:
            pass
    
    return id_translated_dict

def write_to_text__id_chinese(
            out_text_file_name,
            id_translated_dict,
            double_chinese=False,
            id_english_dict=None,
            english=False
            ):
    
    if id_english_dict is None:
        id_english_dict=dict()
    
    with open(out_text_file_name,mode="wt",encoding="utf_8_sig") as f:
        for game_id in sorted( id_translated_dict.keys() ):
            translated_string = id_translated_dict[game_id]
            f.write(game_id)
            f.write("\t")
            f.write(translated_string)
            if double_chinese:
                f.write("\t")
                f.write(translated_string)
            if english:
                f.write("\t")
                f.write(id_english_dict.get(game_id,""))
            f.write("\n")



# id english dict
id_english_dict = read_id_english_file( id_english_text_file )

# english chinese dict
english_chinese_dict = dict()
the_txt_file_list = misc.search_txt_files_in_a_folder( english_chinese_folder )
for a_txt_file in the_txt_file_list:
    print()
    print("\t",a_txt_file)
    temp = read_english_chinese_file( a_txt_file )
    english_chinese_dict.update( temp )
del the_txt_file_list

# english chinese dict
# second part
english_chinese_dict_second_part = dict()
the_txt_file_list = misc.search_txt_files_in_a_folder( english_chinese_folder_second_part )
for a_txt_file in the_txt_file_list:
    print()
    print("\t",a_txt_file)
    temp = read_english_chinese_file( a_txt_file )
    english_chinese_dict_second_part.update( temp )
del the_txt_file_list

# id_translated_dict
id_translated_dict = translate(
        id_english_dict,
        english_chinese_dict,
        english_chinese_dict_second_part)

# 以上为 整体
###################
###################
# 以下为 SL ，是否再 使用 每一个 子分类，翻译
if type_of_tranlsation == "SL":
    print()
    
    def sl_get_xml_name(id_english_dict):
        xml_name_set = set()
        
        for the_id in id_english_dict:
            the_id = the_id.strip()
            
            if " " in the_id:
                xml_name = the_id.split(" ",maxsplit=1)[0]
                xml_name_set.add(xml_name)
        
        return xml_name_set
    
    xml_name_set = sl_get_xml_name(id_english_dict)
    
    # 分类翻译的文件夹
    # english_chinese_folder_specific
    xml_translation_resource_folder_dict = dict()
    # xml_name : folder_path
    if os.path.isdir( english_chinese_folder_specific ):
        
        if os.path.isdir( english_chinese_folder_specific ):
        
            the_folder = os.path.abspath( english_chinese_folder_specific )
            
            (dirpath, dirnames, filenames) = next( os.walk( the_folder ) )
            
            for folder_name in dirnames:
                xml_name = folder_name.lower()
                if xml_name in xml_name_set:
                    xml_translation_resource_folder_dict[xml_name]=os.path.join( dirpath , folder_name )
    
    # 对 每个 sl 的 xml 文件夹
    if xml_translation_resource_folder_dict:
        for xml_name,folder_path in xml_translation_resource_folder_dict.items():
            print(xml_name,":")
            print("\t:",folder_path)
            
            # 翻译范围
            id_english_dict_specific = dict()
            temp = xml_name + " " # id 为 xml 加空格 开头
            for the_id,english in id_english_dict.items():
                if the_id.startswith(temp):
                    id_english_dict_specific[the_id]=english
            
            # 翻译资源
            english_chinese_dict_specific = dict()
            the_txt_file_list = misc.search_txt_files_in_a_folder( folder_path )
            for a_txt_file in the_txt_file_list:
                print()
                print(xml_name,":","\t",a_txt_file)
                temp = read_english_chinese_file( a_txt_file )
                english_chinese_dict_specific.update( temp )
            
            # 翻译结果
            id_translated_dict_specific = translate(
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
write_to_text__id_chinese( out_text_final_id_chinese,         id_translated_dict , )
write_to_text__id_chinese( out_text_final_id_chinese_chinese ,id_translated_dict ,
        double_chinese=True )
write_to_text__id_chinese( out_text_final_id_chinese_english ,id_translated_dict ,
        id_english_dict = id_english_dict,english=True )

# 写出，没翻译的 id
with open(out_text_for_not_translated_id,mode="wt",encoding="utf_8_sig",) as f:
    for the_id in sorted(id_english_dict):
        if the_id not in id_translated_dict:
            f.write(the_id)
            f.write("\n")

# 写出，没翻译的 id \t english
with open(out_text_for_not_translated_id_english,mode="wt",encoding="utf_8_sig",) as f:
    for the_id in sorted(id_english_dict):
        if the_id not in id_translated_dict:
            f.write(the_id)
            f.write("\t")
            f.write(id_english_dict[the_id])
            f.write("\n")

# 写出，没翻译的 id \t english  --- 小写，
#   怎么 排序，数量多的排前面？
with open(out_text_for_not_translated_english_lower,mode="wt",encoding="utf_8_sig",) as f:
    
    english_lower_counter = dict()
    
    id_list = [] # 未翻译的
    for the_id in id_english_dict:
        if the_id not in id_translated_dict:
            id_list .append( the_id )
    
    # english_lower_counter
    for the_id in id_list:
        english = id_english_dict[ the_id ]
        english_part_1,english_part_2 = split_string_to_two_part.main( english )
        
        # 括号前的部分，处理
        english_part_1 = the_first_part.main( english_part_1 )
        # lower case
        english_part_1 = english_part_1.lower()
        
        if english_part_1:
            if english_part_1 in english_lower_counter:
                english_lower_counter[ english_part_1 ] += 1
            else:
                english_lower_counter[ english_part_1 ] = 1
    
    
    for english_lower,number in sorted(
            english_lower_counter.items(),
            key=lambda x:x[1],
            reverse=True,
                ):
        f.write( english_lower )
        f.write( "\t")
        f.write( str(number) )
        f.write( "\n")

# 写出 ,第二部分，没有翻译的 ，English
# 小写，按数量，排列
dict_for_second_part_english_counter = misc.get_second_part_english_counter_lower_case( id_english_dict )
#out_text_for_not_translated_2nd_part_english
with open(out_text_for_not_translated_2nd_part_english,mode="wt",encoding="utf_8_sig",) as f:
    for english,count in sorted(
                dict_for_second_part_english_counter.items(),
                key=lambda x:x[1],
                reverse=True,
                ):
        if english not in english_chinese_dict_second_part:# 排除已翻译的
            f.write(english)
            f.write("\t")
            f.write(str(count))
            f.write("\n")

