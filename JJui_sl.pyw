# -*- coding: utf_8_sig-*-
import sys
import os
import builtins

gamelist_type="softwarelist" #  "mame"  #"softwarelist"

from jjui_source import global_variable # 最先导入这个包
# 记录
global_variable.gamelist_type = gamelist_type 

    # 翻译工具 gettext ，
        # 它用的 二进制 文件，麻烦
        # 它似乎推荐 在源代码里 用英文 ， 用中文不知道有问题没有，麻烦
    # 所以自定义一个翻译算了
    # 翻译符号 _ ，用和 gettext 一样的符号

#   要不要弄成全局的 ??
# 把翻译符号 _ ，作用范围弄到 全局里
# 也就是，照着 gettext 抄,把翻译符号 _ ，弄到 builtins 里

from jjui_source.translation_ui import translation_holder
#_=translation_holder.translation
builtins.__dict__['_'] = translation_holder.translation
#   要不要弄成全局的 ??

# 以下
#   在翻译 之前的 包，不应该使用 翻译 功能
#       首先读取 配置文件
#       再,根据 配置文件 内容，确定 翻译 文本 所在位置
#       再,读取 翻译文件


from jjui_source import global_static_filepath  as the_files
from jjui_source import read_user_config 



"""
    # A
    # 切换当前工作目录
        #1 以 python 脚本模式 运行 ，切换到主脚本所在文件夹
        #2 打包为 exe 后，运行，切换到 exe 所在文件夹
            打包方式 pyinstall 目录模式
            打包方式 Nuitka ？？？？？
            打包方式 其它  ？？？？？

    # B
    # 把翻译符号 _ 弄到 builtins 里 ,要不要弄进去？
        
        # √●×
        
        # 前提
        # 读取各 文件、文件夹 路径 
         √
        
        # 前提
        # 检查临时文件夹 .jjui
        #   如果临时文件夹不存在，建一个新的
         √
        
        # 前提
        # 读取配置文件 jjui.ini
        #   如果配置文件不存在，读取默认值，并建一个新的 jjui.ini
         √
        
        # 读取 ui 翻译
            #   从配置文件获得 翻译文件 位置
            √    读取 ui 翻译
            √    设置全局变量 _ 弄到 builtins 里

"""

####
####
####

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

print()
print("working directory")
print( os.getcwd() )

change_working_directory()

print()
print("change working directory if needed")
print( os.getcwd() )
print()

####


# 检查临时文件夹
def check_temporary_folder():
    """
    检查临时文件夹
    """
    folder_temporary  = the_files.folder_temporary
    # 如果存在同名文件，但不是文件夹，
    # 删除后，创建 目录
    if os.path.isfile(folder_temporary ):
        os.remove(folder_temporary )
        os.makedirs(folder_temporary )
    #   如果不存在，创建 目录
    if os.path.exists(folder_temporary ):
        pass
    else:
        os.makedirs(folder_temporary )

check_temporary_folder()

# 读取配置文件。如果不存在，创建一个新的
def read_configure_file():
    # return ini_data,ini_default,ini_order
    
    """
    读取配置文件
    如果不存在，创建一个新的
    """

    file_ini_configure = the_files.file_ini_configure

    
    ini_data    = {}
    ini_order   = []
    ini_default = {}
    
    flag = False # 文件存在标记
    if os.path.exists(file_ini_configure ):
        if os.path.isfile(file_ini_configure ):
            flag = True
    
    ini_order,ini_default = read_user_config.get_configure_file_default_value()
    
    if not flag : # 如果 配置文件 不存在
        # 新建文件
        read_user_config.write_ini(file_ini_configure,ini_default,ini_order)
        ini_data=ini_default

    if flag: # 如果 配置文件 存在
        ini_data = read_user_config.get_configure_file_value( file_ini_configure )
    #del flag
    return ini_data,ini_default,ini_order

(   global_variable.user_configure_data ,
    global_variable.user_configure_data_default ,
    global_variable.user_configure_data_order ,
        ) = read_configure_file()

configure_data = global_variable.user_configure_data



# 读取翻译文件
def get_ui_language_file_path(configure_data):
    language = configure_data["ui_language"]
    if language != "" :
        if os.path.isfile(language):
            pass
        else:
            language = ""
    return language

ui_language_file_path = get_ui_language_file_path(configure_data)

if ui_language_file_path == "" : # 原始 ，中文，不翻译
    pass
else: # 其它语言
    translation_holder.get_translation_dict_from_file( ui_language_file_path )


#####
#####
#####

from jjui_source import ui_main

ui_main.main()

