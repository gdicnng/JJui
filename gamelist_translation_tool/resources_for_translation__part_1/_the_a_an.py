# -*- coding: utf_8_sig-*-
import os
import sys
import re 

"""
    注：
    有大量 a 或 an 或 the 开头的，被倒装了，
    需要调整一下顺序


    xxx yyy, the
    xxx yyy, a
    xxx yyy, an

    调整为：

    the xxx yyy
    a xxx yyy
    an xxx yyy


    正则
    ^(.*),\s*(an?|the)\b(.*)$

"""

the_folder = "."
out_file = "_the_a_an.txt"
# 删文件先
try:
    os.remove(out_file)
except:
    pass

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

# python 3.4.4
#   命令行模式时，print 函数 兼容，超过 字符集 问题
#   窗口模式，不用管
if sys.version_info < (3, 6):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors= 'backslashreplace',line_buffering=True)
        #print("less than 3.6")
    except:
        pass


def search_txt_files_in_a_folder( the_folder ):
    """
        搜索一个文件夹中的 .txt 文件
        返回文件列表
        顺序排列
    """
    txt_file_list = []
    
    if os.path.isdir( the_folder ):
        
        the_folder = os.path.abspath( the_folder )
        
        for (dirpath, dirnames, filenames) in sorted( os.walk( the_folder ) ):
            for file_name  in sorted(filenames):
                if file_name.lower().endswith(".txt"):
                    txt_file_list.append( os.path.join(dirpath,file_name) )
    
    return txt_file_list


search_string=r"^(.*),\s*(an?|the)\b(.*)$"
#search_string=r"abc"
p = re.compile( search_string ,flags=re.IGNORECASE) # 大小写

def find_and_string_in_a_file( file_name ):
    temp_list = []
    
    if not os.path.isfile(file_name):
        print()
        print("file not found:",file_name)
    
    with open(file_name,mode="rt",encoding="utf_8_sig",errors='backslashreplace') as f:
        for line in f:
            line = line.strip()
            
            if not line:
                continue
            
            m=p.search(line)
            
            if m:
                #print()
                #print(m.group(0))
                #print(m.group(1))
                #print(m.group(2))
                #print(m.group(3))
                new_string = m.group(2) + " " + m.group(1) + m.group(3)
                print()
                print(line)
                print(new_string)
                #input()
                temp_list.append(new_string)
    
    return temp_list

txt_file_list = search_txt_files_in_a_folder(  the_folder  )
for x in txt_file_list:
    print(x)

with open(out_file,mode="wt",encoding="utf_8_sig",errors='backslashreplace') as f:
    
    for file_name in txt_file_list:
        temp_list = find_and_string_in_a_file(file_name)
        
        try:
            rel_file_name = os.path.relpath(file_name)
        except:
            rel_file_name = file_name
        
        if temp_list:
            
            f.write("\n")
            f.write(" ")
            f.write(rel_file_name)
            f.write("\n")
            f.write("\n")
            
            for line in temp_list:
                line = line.strip()
                f.write(line)
                f.write("\n")



