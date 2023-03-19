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
from source_py_some_scripts import windows_file_name


folder_for_rename_files = "files_to_rename"
log_file = "log_file_rename.txt"

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
    
    读取 原始文件夹： （英文）原文件名    \t     文件名（去后缀）
    
    翻译
        英文两部分，括号前 与 括号后
        
        括号前
            读取 文件：英文 \t 中文
                在文件夹中搜索所有的 .txt 翻译原文件 
        括号后
            读取 文件：英文 \t 中文
                在文件夹中搜索所有的 .txt 翻译原文件
"""

#############
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

######################

# id \t 英文
def get_id_english_dict_from_folder(the_folder):
    
    id_english_dict ={}
    # id 
        # 英文
    
    (dirpath, dirnames, filenames) = next(  os.walk(the_folder)  )
    
    filenames = sorted(filenames)
    
    for a_file_name in filenames:
        
        the_id = a_file_name
        
        english = os.path.splitext( the_id )[0]
        
        id_english_dict[the_id] = english
    
    return id_english_dict

# id english dict
id_english_dict = get_id_english_dict_from_folder( folder_for_rename_files )

#for x,y in id_english_dict.items():
#    print()
#    print(x)
#    print("\t",end="")
#    print(y)

# english chinese dict
english_chinese_dict = dict()
the_txt_file_list = misc.search_txt_files_in_a_folder( english_chinese_folder )
for a_txt_file in the_txt_file_list:
    print()
    print("\t",a_txt_file)
    temp = misc.read_english_chinese_file( a_txt_file )
    english_chinese_dict.update( temp )
del the_txt_file_list

# english chinese dict
# second part
english_chinese_dict_second_part = dict()
the_txt_file_list = misc.search_txt_files_in_a_folder( english_chinese_folder_second_part )
for a_txt_file in the_txt_file_list:
    print()
    print("\t",a_txt_file)
    temp = misc.read_english_chinese_file( a_txt_file )
    english_chinese_dict_second_part.update( temp )
del the_txt_file_list

# id_translated_dict
id_translated_dict = misc.translate(
        id_english_dict,
        english_chinese_dict,
        english_chinese_dict_second_part)


##################
##################
# 以下为翻译后，结果写出

# 结果
misc.write_to_text__id_chinese( out_text_final_id_chinese,         id_translated_dict , )
misc.write_to_text__id_chinese( out_text_final_id_chinese_chinese ,id_translated_dict ,
        double_chinese=True )
misc.write_to_text__id_chinese( out_text_final_id_chinese_english ,id_translated_dict ,
        id_english_dict = id_english_dict,english=True )

# 写出，没翻译的 id
with open(out_text_for_not_translated_id,mode="wt",encoding="utf_8_sig",errors='backslashreplace') as f:
    for the_id in sorted(id_english_dict):
        if the_id not in id_translated_dict:
            f.write(the_id)
            f.write("\n")

# 写出，没翻译的 id \t english
with open(out_text_for_not_translated_id_english,mode="wt",encoding="utf_8_sig",errors='backslashreplace') as f:
    for the_id in sorted(id_english_dict):
        if the_id not in id_translated_dict:
            f.write(the_id)
            f.write("\t")
            f.write(id_english_dict[the_id])
            f.write("\n")

# 写出，没翻译的 id \t english  --- 小写，
#   怎么 排序，数量多的排前面？
with open(out_text_for_not_translated_english_lower,mode="wt",encoding="utf_8_sig",errors='backslashreplace') as f:
    
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
with open(out_text_for_not_translated_2nd_part_english,mode="wt",encoding="utf_8_sig",errors='backslashreplace') as f:
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

########################
########################
########################
########################
#翻译
######
#id_translated_dict
#译名部分先加上 文件名 后缀
#如果有非法文件名字符，替换
print()
print("file name rename ")
number = len(id_translated_dict)
print(number)

#list_file_not_translated = []
list_file_renamed = []
list_file_rename_failed = []

fail_counter = 0
for file_name,chinese in id_translated_dict.items():
    
    ext = os.path.splitext(file_name)[1]
    
    new_name = chinese + ext #译名部分先加上 文件名 后缀
    
    new_name = windows_file_name.replace_reserved_characters(new_name)#如果有非法文件名字符，替换
    
    if os.path.isfile( os.path.join(folder_for_rename_files, file_name )):
        try:
            os.rename(
                    os.path.join(folder_for_rename_files, file_name ),
                    os.path.join(folder_for_rename_files, new_name ),
                    )
            list_file_renamed.append( (file_name,new_name), )
        except:
            fail_counter += 1
            print()
            print("rename failed : ",end="")
            print(file_name,"\t",new_name)
            list_file_rename_failed.append( (file_name,new_name), )

# 没有翻译的
list_file_no_translation = []
for the_id in id_english_dict:
    if the_id not in id_translated_dict:
        list_file_no_translation.append( the_id )

with open(log_file,mode="wt",encoding="utf_8_sig") as f:
    # 没有翻译的
    count = 0
    if list_file_no_translation:
        for file_name in list_file_no_translation:
            
            count += 1
            
            f.write("文件没有翻译 (not translate) ")
            f.write(str(count))
            f.write(":")
            f.write("\n")
            
            f.write("\t")
            f.write(file_name)
            
            f.write("\n")
            f.write("\n")
    
    # 翻译，重命命名成功
    count = 0
    if list_file_renamed:
        for file_name,new_name in list_file_renamed:
            
            count += 1
            
            f.write("文件重命名 (file rename) ")
            f.write(str(count))
            f.write(":")
            f.write("\n")
            
            f.write("\t")
            f.write(file_name)
            f.write("\n")
            
            f.write("\t")
            f.write(new_name)
            f.write("\n")
            
            f.write("\n")
    
    # 翻译，重命命名失败
    count=0
    if list_file_rename_failed:
        for file_name,new_name in list_file_rename_failed:
            
            count += 1
            
            f.write("文件重命名失败 (file rename failed) ")
            f.write(str(count))
            f.write(":")
            f.write("\n")
            
            f.write("\t")
            f.write(file_name)
            f.write("\n")
            f.write("\t")
            f.write(new_name)
            f.write("\n")
            f.write("\n")
    
    
    #######
    #######
    
    if list_file_no_translation:
        f.write("未匹配到翻译，数量：")
        f.write(str(len(list_file_no_translation)))
        f.write("\n")
        
        f.write("没有翻译的文件列表，见文件：")
        f.write("\n")
        f.write("out_translated__not_translated__id.txt")
        f.write("\n")
        f.write("out_translated__not_translated__id_english.txt")
        f.write("\n")
        f.write("\n")
    
    
    if list_file_renamed:
        f.write("匹配到翻译，重命名成功，数量：")
        f.write(str(len(list_file_renamed)))
        f.write("\n")
        f.write("\n")
    
    if list_file_rename_failed:
        f.write("匹配到翻译，但，重命名失败，数量：")
        f.write(str(len(list_file_rename_failed)))
        f.write("\n")
        f.write("重命名失败，很有可能是因为，两个 游戏，翻译成了相同的中文")
        f.write("\n")
        f.write("\n")
    
    
    f.write("括号后面的部分，如果有还未翻译的词条，见文件（已转小写，按数量排序）：")
    f.write("\n")
    f.write("out_translated__not_translated__2nd_part_englsih.txt")
