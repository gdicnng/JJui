# -*- coding: utf_8_sig-*- 
import os
import sys
import xml.etree.ElementTree

from source_py_some_scripts import the_files
from source_py_some_scripts import misc
#from source_py_some_scripts import the_first_part
from source_py_some_scripts import the_second_part
from source_py_some_scripts import split_string_to_two_part
from source_py_some_scripts import multi_space_to_single

temp_xml_file_name = the_files.file__roms_sl_xml

out_file__id_to_english                 = the_files.file__id_to_english
out_file__second_part_english           = the_files.file__second_part_english


##############

misc.for_print_error_python34()

# 切换工作目录
# 切换工作目录
    # 到 主 py 脚本所在 文件夹
    # 或者 ，如查 pyinstaller 打包 的 exe ，到主exe所在文件夹
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
    
    print()
    print("now ,working directory is :")
    print(os.getcwd())

change_working_directory()

###############


def get_gamelist_from_xml_sl(xml_file_name):
    print()
    print("parse xml")
    print(xml_file_name)
    print("wait for while ......")    
    temp_dict = dict()
        #id
        #   description
    for (event, elem) in xml.etree.ElementTree.iterparse(xml_file_name,events=("end",) ) :#"start"
        if elem.tag=="softwarelist":
            xml_name        = elem.attrib.get("name","").strip().lower()
            
            for child in elem:
                if child.tag=="software" :
                    software_name = child.attrib["name"].strip().lower()
                    
                    software_id   = "".join( ( xml_name," ",software_name ) )
                    
                    for grand_child  in child:
                        # description
                        if   grand_child.tag == "description":
                            temp_dict[software_id]=grand_child.text
                            
                            if temp_dict[software_id] is None:
                                temp_dict[software_id]=""
            
            
            elem.clear()
    
    return temp_dict


# 获取 
#   id : description
# 解析 xml
id_english_dict = get_gamelist_from_xml_sl( temp_xml_file_name )


# 写出
print("")
print("write id English")
print(out_file__id_to_english)
with open(out_file__id_to_english,mode="wt",encoding="utf_8_sig") as f:
    
    # 排序
    # 第一部分，英文小写，并且 处理过空格
    def func_for_sort(english):
        english_first , english_last = split_string_to_two_part.main(english)
        english_first = english_first.strip()
        english_first = multi_space_to_single.main( english_first )
        english_first = english_first.lower()
        return english_first
    
    for the_id,english in sorted(
                id_english_dict.items() ,
                key = lambda x : func_for_sort(x[1]),
                ):
        f.write(the_id)
        f.write("\t")
        f.write(english)
        f.write("\n")


# 括号后的 字符串 ，切割，得到需要翻译的 小片段

# 第二部分的 需要 翻译的词条，计数的 dict
dict_for_second_part_english_counter = misc.get_second_part_english_counter( id_english_dict )

# 写出
def write__second_part_english(file_name,dict_for_second_part_english_counter):
    with open(file_name,mode="wt",encoding="utf_8_sig") as f:
        temp_list = list( dict_for_second_part_english_counter.keys() )
        temp_list.sort(key=lambda x : x.lower() )
        for temp_string in temp_list :
            f.write(temp_string)
            f.write("\n")

print("write :",out_file__second_part_english)
write__second_part_english(out_file__second_part_english,dict_for_second_part_english_counter)
