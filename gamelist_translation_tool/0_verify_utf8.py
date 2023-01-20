# -*- coding: utf_8_sig-*-
import os
import sys

from source_py_some_scripts import the_files

the_folder_list = []
the_folder_list.append( the_files.english_chinese_folder )
the_folder_list.append( the_files.english_chinese_folder_for_single_xml )
the_folder_list.append( the_files.english_chinese_folder_second_part )


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


error_file_list = []
count = 0
for the_folder in the_folder_list:
    
    # 未找到
    if not os.path.isdir(the_folder):
        #print("")
        #print("not found the folder :",the_folder)
        continue
    
    print("search .txt files in this folder :",the_folder)
    
    for (dirpath, dirnames, filenames) in sorted( os.walk( the_folder ) ):
        for file_name  in sorted(filenames):
            if file_name.lower().endswith(".txt"):
                count += 1
                
                file_path =  os.path.join(dirpath,file_name)
                
                #print()
                #print( file_path )
                
                with open(file_path,mode="rb") as binary_file:
                    is_utf8 = True
                    for line in binary_file:
                        try :
                            line.decode(encoding='utf_8_sig', errors='strict')
                        except:
                            is_utf8 = False
                            break
                    if not is_utf8:
                        error_file_list.append( file_path )



if not error_file_list:
    print()
    print("ALL OK")
else:
    print()
    print("error files :")
    for file_name in error_file_list:
        print("error file :",file_name)
    print()
    print("error .txt file :" ,len(error_file_list))        

print()
print("all .txt file :",count)
print()

