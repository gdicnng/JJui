# -*- coding: utf_8_sig-*- 

mame_exe_path = r"c:\MAME\mame0252b_64bit\mame.exe"

import os
import sys
import subprocess
#import xml.etree.ElementTree

#from source_py_some_scripts import the_first_part 
#from source_py_some_scripts import the_second_part 
#from source_py_some_scripts import split_string_to_two_part 
#from source_py_some_scripts import multi_space_to_single 
from source_py_some_scripts import misc 
from source_py_some_scripts import the_files 

temp_xml_file_name = the_files.file__roms_sl_xml




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

############

if not os.path.isfile(mame_exe_path):
    print("mame exe path is not right")
    print("exit")
    sys.exit()

mame_exe_path = os.path.abspath(mame_exe_path)
mame_folder = os.path.dirname( mame_exe_path )
print()
print(mame_exe_path)
print(mame_folder)

# -getsoftlist
    # -getsoftlist
def get_info_from_mame(xml_file_name,mame_exe_path,mame_folder,):
    print()
    print("get info from mame")
    print("write to :",xml_file_name)
    print("wait for a while ......")
    
    command_list=[]
    command_list.append(mame_exe_path)
    #command_list.append("-help")
    command_list.append("-getsoftlist")

    file_object=open(xml_file_name,mode="wb",)
    
    p=subprocess.Popen( args   = command_list,
                            # command = "-listxml"
                        shell  = True, 
                        stdout = file_object ,
                        stderr = subprocess.PIPE,
                        stdin  = subprocess.PIPE,
                        cwd    = mame_folder,
                        )
    p.wait()
    
    file_object.close()


get_info_from_mame( temp_xml_file_name,mame_exe_path,mame_folder )
