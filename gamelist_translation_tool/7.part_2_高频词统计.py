# -*- coding: utf_8_sig-*- 
import sys
import os
import re
import string

from source_py_some_scripts import misc
from source_py_some_scripts import the_files


file_id_to_english = the_files.file__id_to_english
out_file           = the_files.file__word_frequency_in_part_2

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


id_english_file = misc.read_id_english_file( file_id_to_english )
counter_dict    = misc.get_second_part_english_counter(id_english_file)
with open(out_file,mode="wt",encoding="utf-8",) as f:
    for english_word ,count in sorted(
            counter_dict.items(),
            key=lambda x : x[1],
            reverse = True,
    ):
        f.write(english_word)
        f.write("\t")
        f.write(str(count))
        f.write("\n")